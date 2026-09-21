# Created-by: forge | Date: 2026-09-21
#!/usr/bin/env python3
"""
Level-3 Link Integrity Checker.

For each Link at verification_level < 3:
  1. HTTP liveness check (HEAD request, proper UA, retry, timeout)
  2. Band-identity check: fetch page, look for city/label/member-name anchors
  3. Name-collision detection: check against data/name_collisions.json
  4. Promote to Level 3 if checks pass, or flag with notes if ambiguous

Writes results back to Link records. Produces a per-run report.

Usage:
    python link_verifier.py --dry-run --limit 10
    python link_verifier.py --limit 50
    python link_verifier.py --report-only
"""

import os
import sys
import json
import time
import argparse
import re
from datetime import datetime
from urllib.parse import urlparse

# ── Django setup ──────────────────────────────────────────────────────────────
DEMOTAPE_DIR = os.path.expanduser("~/Projects/demotape")
sys.path.insert(0, DEMOTAPE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
import django
django.setup()

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from apps.core.models import Band, Link, Release

# ── Config ───────────────────────────────────────────────────────────────────
COLLISION_FILE = os.path.join(DEMOTAPE_DIR, "data", "name_collisions.json")
USER_AGENT = "Mozilla/5.0 (compatible; Demotape-Verifier/1.0)"
HTTP_TIMEOUT = 15
MAX_RETRIES = 2
RETRY_BACKOFF = 1.5
RATE_LIMIT_SLEEP = 1.0  # seconds between requests
PAGE_FETCH_LIMIT = 5000  # chars of page text to analyze
BATCH_SIZE_DEFAULT = 50

# Domains that return 405 on HEAD — use GET with Range instead
GET_ONLY_DOMAINS = [
    "youtube.com", "www.youtube.com", "youtu.be",
    "bandcamp.com", "soundcloud.com",
    "facebook.com", "www.facebook.com",
    "instagram.com", "www.instagram.com",
]

# Italian words for language heuristic
ITALIAN_WORDS = {
    "il", "lo", "la", "i", "gli", "le", "un", "uno", "una",
    "di", "del", "della", "dei", "degli", "delle",
    "e", "ed", "o", "od",
    "in", "nel", "nella", "nei", "negli", "nelle",
    "con", "col", "coi",
    "per", "dal", "dalla", "dai", "dagli", "dalle",
    "su", "sul", "sulla", "sui", "sugli", "sulle",
    "da", "al", "alla", "ai", "agli", "alle",
    "band", "gruppo", "musica", "rock", "punk", "live",
    "concerto", "disco", "album", "singolo", "ep",
    "etichetta", "label", "membri", "componenti",
    "citta", "città", "paese", "regione",
    "biografia", "storia", "contatti", "link",
    "ufficiale", "sito", "web", "pagina",
    "ascolta", "guarda", "leggi", "scopri",
    "nuovo", "nuovi", "vecchio", "vecchi",
    "primo", "prima", "secondo", "seconda",
    "grande", "piccolo", "piccola",
    "buono", "buona", "cattivo", "cattiva",
    "primo", "ultimo", "ultima",
}


# ── Functions ─────────────────────────────────────────────────────────────────

def load_collision_registry():
    """Load the name-collision registry from data/name_collisions.json."""
    try:
        with open(COLLISION_FILE) as f:
            data = json.load(f)
        return data.get("collisions", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def is_get_only_domain(url):
    """Check if URL is on a domain that requires GET (not HEAD)."""
    try:
        parsed = urlparse(url)
        return parsed.hostname in GET_ONLY_DOMAINS
    except Exception:
        return False


def check_http_liveness(url):
    """
    Check if a URL is alive.

    Returns:
        tuple: (alive: bool, status_code: int|None, error: str|None)
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    headers = {"User-Agent": USER_AGENT}

    # Try HEAD first (unless domain requires GET)
    if is_get_only_domain(url):
        return _check_with_get(session, headers, url)

    try:
        resp = session.head(
            url, headers=headers, timeout=HTTP_TIMEOUT,
            allow_redirects=True
        )
        # Some servers return 405 on HEAD — fall back to GET
        if resp.status_code == 405:
            return _check_with_get(session, headers, url)
        alive = 200 <= resp.status_code < 400
        return (alive, resp.status_code, None)
    except requests.exceptions.Timeout:
        return (False, None, "Timeout")
    except requests.exceptions.ConnectionError as e:
        return (False, None, f"Connection error: {str(e)[:100]}")
    except requests.exceptions.RequestException as e:
        return (False, None, f"Request error: {str(e)[:100]}")


def _check_with_get(session, headers, url):
    """Fallback GET check with Range header to minimize data transfer."""
    try:
        get_headers = {**headers, "Range": "bytes=0-0"}
        resp = session.get(
            url, headers=get_headers, timeout=HTTP_TIMEOUT,
            allow_redirects=True, stream=True
        )
        # Consume minimal data
        _ = resp.raw.read(1024) if resp.raw else None
        resp.close()
        alive = 200 <= resp.status_code < 400
        return (alive, resp.status_code, None)
    except requests.exceptions.Timeout:
        return (False, None, "Timeout (GET fallback)")
    except requests.exceptions.ConnectionError as e:
        return (False, None, f"Connection error (GET): {str(e)[:100]}")
    except requests.exceptions.RequestException as e:
        return (False, None, f"Request error (GET): {str(e)[:100]}")


def fetch_page_text(url, max_chars=PAGE_FETCH_LIMIT):
    """
    Fetch page content and return first N chars of text.

    Returns:
        str: Page text content, or empty string on failure.
    """
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=HTTP_TIMEOUT,
            allow_redirects=True,
        )
        if resp.status_code >= 400:
            return ""
        # Get text content
        text = resp.text[:max_chars * 2]  # Extra for HTML stripping
        # Simple HTML tag stripping
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_chars]
    except Exception:
        return ""


def is_english_page(text):
    """
    Heuristic: check if page text is in English (not Italian).

    Returns:
        bool: True if page appears to be in English.
    """
    if not text:
        return True  # Default to English if we can't tell

    words = re.findall(r'[a-zA-Z]+', text.lower())
    if not words:
        return True

    # Check ASCII ratio
    ascii_count = sum(1 for c in text if ord(c) < 128)
    ascii_ratio = ascii_count / len(text) if text else 1.0

    # Count Italian words
    italian_count = sum(1 for w in words if w in ITALIAN_WORDS)
    italian_ratio = italian_count / len(words) if words else 0

    # If >80% ASCII and few Italian words, consider it English
    return ascii_ratio > 0.8 and italian_ratio < 0.05


def check_band_identity(link, collision_registry):
    """
    Fetch the page and check if it matches the band's identity.

    Returns:
        tuple: (is_same_band: bool|None, evidence: list[str], confidence: str)
    """
    band = link.band
    evidence = []

    # Gather band identity anchors
    city = (band.city or "").strip()
    member_names = []

    # Extract member names from bio/notes
    bio_text = f"{band.bio or ''} {band.bio_en or ''}"
    # Simple name extraction: look for capitalized words that look like names
    potential_names = re.findall(r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b', bio_text)
    member_names.extend(potential_names)

    # Get labels from releases
    labels = set()
    for release in Release.objects.filter(band=band).exclude(label=''):
        labels.add(release.label.strip())

    # Fetch page text
    page_text = fetch_page_text(link.url)
    if not page_text:
        return (None, ["Could not fetch page content"], "low")

    page_lower = page_text.lower()

    # Check for city name in page
    city_match = False
    if city and len(city) > 2:
        if city.lower() in page_lower:
            city_match = True
            evidence.append(f"City '{city}' found on page")

    # Check for label names in page
    label_matches = []
    for label in labels:
        if label and len(label) > 2 and label.lower() in page_lower:
            label_matches.append(label)
            evidence.append(f"Label '{label}' found on page")

    # Check for member names in page
    member_matches = []
    for name in member_names:
        if name and len(name) > 3 and name.lower() in page_lower:
            member_matches.append(name)
            evidence.append(f"Member '{name}' found on page")

    # Check collision registry
    band_name_lower = band.name.lower()
    in_collision_registry = False
    for collision in collision_registry:
        if collision.get("name", "").lower() == band_name_lower:
            in_collision_registry = True
            break

    # If in collision registry and page is English, flag as ambiguous
    if in_collision_registry:
        if is_english_page(page_text):
            evidence.append("Band in name-collision registry + English page")
            return (None, evidence, "ambiguous")
        else:
            evidence.append("Band in collision registry but non-English page")

    # Determine confidence based on evidence
    total_evidence = len(evidence)
    if city_match and (label_matches or member_matches):
        confidence = "high"
        is_same = True
    elif city_match or label_matches or member_matches:
        confidence = "medium"
        is_same = True
    elif total_evidence > 0:
        confidence = "low"
        is_same = True
    else:
        confidence = "low"
        is_same = None  # Can't determine

    return (is_same, evidence, confidence)


def verify_link(link, collision_registry, dry_run=False):
    """
    Verify a single link: HTTP liveness + band identity.

    Returns:
        dict: Result for reporting.
    """
    result = {
        "link_id": link.id,
        "band": link.band.name,
        "url": link.url,
        "action": "none",
        "status": "unknown",
        "notes": "",
    }

    # Step 1: HTTP liveness
    alive, status_code, error = check_http_liveness(link.url)

    if not alive:
        notes = f"HTTP {status_code}: {error}" if status_code else f"HTTP error: {error}"
        result["action"] = "flag_dead"
        result["status"] = "dead"
        result["notes"] = notes
        if not dry_run:
            link.verification_notes = notes
            link.save(update_fields=["verification_notes"])
        return result

    # Step 2: Band identity
    is_same, evidence, confidence = check_band_identity(link, collision_registry)

    if confidence == "ambiguous":
        notes = f"Ambiguous: {'; '.join(evidence)}"
        result["action"] = "flag_ambiguous"
        result["status"] = "ambiguous"
        result["notes"] = notes
        if not dry_run:
            link.verification_notes = notes
            link.save(update_fields=["verification_notes"])
        return result

    if is_same and confidence in ("high", "medium"):
        # Promote to Level 3
        evidence_str = "; ".join(evidence) if evidence else "HTTP alive + basic match"
        notes = f"Auto-verified: {evidence_str}"
        result["action"] = "promote"
        result["status"] = "promoted"
        result["notes"] = notes
        if not dry_run:
            link.verification_level = 3
            link.verified_at = datetime.now()
            link.verified_by = "auto-checker"
            link.verification_notes = notes
            link.save(update_fields=["verification_level", "verified_at", "verified_by", "verification_notes"])
        return result

    # Low confidence or no match — flag for review
    evidence_str = "; ".join(evidence) if evidence else "No strong identity anchors found"
    notes = f"Low confidence: {evidence_str}"
    result["action"] = "flag_review"
    result["status"] = "review"
    result["notes"] = notes
    if not dry_run:
        link.verification_notes = notes
        link.save(update_fields=["verification_notes"])
    return result


def run_verification(batch_size=BATCH_SIZE_DEFAULT, dry_run=False, limit=None):
    """
    Main verification loop.

    Args:
        batch_size: Number of links to process per batch.
        dry_run: If True, don't write changes to DB.
        limit: Max number of links to process (None for all).

    Returns:
        dict: Summary of results.
    """
    collision_registry = load_collision_registry()

    # Query links below Level 3
    queryset = Link.objects.filter(verification_level__lt=3).order_by("id")
    if limit:
        queryset = queryset[:limit]

    total_count = queryset.count()
    print(f"  Links to verify: {total_count}")
    if dry_run:
        print("  🔍 DRY RUN — no changes will be saved")

    results = []
    processed = 0
    promoted = 0
    flagged_dead = 0
    flagged_ambiguous = 0
    flagged_review = 0
    errors = 0

    for link in queryset.iterator():
        processed += 1
        try:
            result = verify_link(link, collision_registry, dry_run=dry_run)
            results.append(result)

            if result["action"] == "promote":
                promoted += 1
            elif result["action"] == "flag_dead":
                flagged_dead += 1
            elif result["action"] == "flag_ambiguous":
                flagged_ambiguous += 1
            elif result["action"] == "flag_review":
                flagged_review += 1

            # Progress output every 10 links
            if processed % 10 == 0 or processed == total_count:
                print(f"  Progress: {processed}/{total_count} "
                      f"(promoted={promoted}, dead={flagged_dead}, "
                      f"ambiguous={flagged_ambiguous}, review={flagged_review})")

        except Exception as e:
            errors += 1
            print(f"  ❌ Error on link #{link.id}: {e}")
            results.append({
                "link_id": link.id,
                "band": link.band.name,
                "url": link.url,
                "action": "error",
                "status": "error",
                "notes": str(e),
            })

        # Rate limiting
        time.sleep(RATE_LIMIT_SLEEP)

    summary = {
        "total_checked": processed,
        "promoted": promoted,
        "flagged_dead": flagged_dead,
        "flagged_ambiguous": flagged_ambiguous,
        "flagged_review": flagged_review,
        "errors": errors,
        "dry_run": dry_run,
        "timestamp": datetime.now().isoformat(),
    }

    return summary, results


def generate_report(summary, results):
    """
    Generate a markdown report of the verification run.

    Args:
        summary: Dict from run_verification.
        results: List of result dicts.

    Returns:
        str: Markdown report.
    """
    lines = [
        f"# Level-3 Link Verification Report",
        f"",
        f"**Generated:** {summary['timestamp']}",
        f"**Dry run:** {'Yes' if summary['dry_run'] else 'No'}",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total checked | {summary['total_checked']} |",
        f"| Promoted to Level 3 | {summary['promoted']} |",
        f"| Dead links | {summary['flagged_dead']} |",
        f"| Ambiguous (collision) | {summary['flagged_ambiguous']} |",
        f"| Flagged for review | {summary['flagged_review']} |",
        f"| Errors | {summary['errors']} |",
        f"",
    ]

    # Flagged links detail
    flagged = [r for r in results if r["action"] in ("flag_dead", "flag_ambiguous", "flag_review")]
    if flagged:
        lines.append("## Flagged Links")
        lines.append("")
        for r in flagged:
            lines.append(f"- **[{r['status'].upper()}]** {r['band']}: {r['url'][:80]}")
            lines.append(f"  - {r['notes']}")
        lines.append("")

    # Promoted links
    promoted = [r for r in results if r["action"] == "promote"]
    if promoted:
        lines.append("## Promoted Links")
        lines.append("")
        for r in promoted:
            lines.append(f"- ✅ {r['band']}: {r['url'][:80]}")
        lines.append("")



    return "\n".join(lines)


def append_verification_report(results, qa_log_path):
    """Append verification results to the QA log.

    Args:
        results: Dict with keys 'checked', 'promoted', 'flagged', 'dead', 'flagged_links'.
        qa_log_path: Path to the QA log file.
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"\n## {ts} — Link Verification Run"]
    lines.append(f"- **Checked:** {results.get('checked', 0)}")
    lines.append(f"- **Promoted to L3:** {results.get('promoted', 0)}")
    lines.append(f"- **Flagged:** {results.get('flagged', 0)}")
    lines.append(f"- **Dead:** {results.get('dead', 0)}")

    flagged_links = results.get("flagged_links", [])
    if flagged_links:
        lines.append("\n### Flagged for Review")
        for link in flagged_links[:10]:
            lines.append(f"- [{link.get('band', '?')}] {link.get('url', '')[:60]} — {link.get('reason', '')}")
        if len(flagged_links) > 10:
            lines.append(f"- …and {len(flagged_links) - 10} more")

    with open(qa_log_path, "a") as f:
        f.write("\n".join(lines) + "\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Level-3 Link Integrity Checker")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run without saving changes")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max links to process")
    parser.add_argument("--report-only", action="store_true",
                        help="Only generate a report (no verification)")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE_DEFAULT,
                        help=f"Batch size (default: {BATCH_SIZE_DEFAULT})")
    parser.add_argument("--output", type=str, default=None,
                        help="Output file for report")
    args = parser.parse_args()

    print("=" * 55)
    print("  LEVEL-3 LINK INTEGRITY CHECKER")
    print("=" * 55)

    if args.report_only:
        # Just show current state
        total = Link.objects.count()
        l1 = Link.objects.filter(verification_level=1).count()
        l2 = Link.objects.filter(verification_level=2).count()
        l3 = Link.objects.filter(verification_level=3).count()
        l4 = Link.objects.filter(verification_level=4).count()
        print(f"\n  Current state:")
        print(f"  Total links: {total}")
        print(f"  Level 1 (Discovered): {l1}")
        print(f"  Level 2 (Cross-Ref):  {l2}")
        print(f"  Level 3 (Auto-Verif): {l3}")
        print(f"  Level 4 (Admin):      {l4}")
        return

    print(f"\n  Starting verification (batch_size={args.batch_size}, "
          f"limit={args.limit or 'all'}, dry_run={args.dry_run})")
    print()

    summary, results = run_verification(
        batch_size=args.batch_size,
        dry_run=args.dry_run,
        limit=args.limit,
    )

    report = generate_report(summary, results)
    print()
    print(report)

    # Save report to file
    output_path = args.output or os.path.join(
        DEMOTAPE_DIR, "data",
        f"verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\n  Report saved to: {output_path}")

    # Print final state
    total = Link.objects.count()
    l3 = Link.objects.filter(verification_level=3).count()
    print(f"\n  Final state: {total} total, {l3} at Level 3")


if __name__ == "__main__":
    main()
