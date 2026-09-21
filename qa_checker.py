# Created-by: agent | Date: 2026-09-16
# Session: automated
#!/usr/bin/env python3
"""
QA Checker — periodic verification of Fisherman's output (links & connections).

Runs every 30 minutes via Hermes cron (separate from Fisherman's 3-min loop).
Appends results to ~/Documents/Obsidian/Vault/projects/demotape-qa-log.md
and creates Paperclip issues for new errors.

Checks:
  1. Duplicate URLs (same band, same URL)
  2. Self-referencing connections (from_band == to_band)
  3. Invalid link_type / connection_type values
  4. Malformed URLs (no scheme or netloc)
  5. Orphaned connections (FK integrity — shouldn't happen but verify)
  6. Spot-check recent URLs for 404s (rate-limited to 5/run)

Exit codes:
  0 = clean
  1 = warnings only
  2 = errors found (or script failure)
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from urllib.parse import urlparse
from collections import defaultdict

# ── Django setup ──────────────────────────────────────────────────────────────
DEMOTAPE_DIR = os.path.expanduser("~/Projects/demotape")
sys.path.insert(0, DEMOTAPE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
import django
django.setup()

from django.db import models
from django.db.models import Count
from apps.core.models import Band, Link, BandConnection

# Import link_verifier for Level-3 verification integration
try:
    from link_verifier import run_verification as _run_l3_verification
except ImportError:
    _run_l3_verification = None

# ── Config ───────────────────────────────────────────────────────────────────
COMPANY_ID = "9b1bb8a3-192f-4c4e-a406-9449c442a8e9"
PC_API = "http://localhost:3100"
QA_LOG = os.path.expanduser("~/Documents/Obsidian/Vault/projects/demotape-qa-log.md")
STATE_FILE = os.path.expanduser("~/Projects/demotape/qa_state.json")
MAX_URL_CHECKS = 5          # Per-run cap on external HTTP checks
RECENT_WINDOW_MIN = 30      # Look at links created in last N minutes
URL_CHECK_TIMEOUT = 10       # Seconds per HTTP request

os.makedirs(os.path.dirname(QA_LOG), exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def run_shell(cmd, timeout=30):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        cwd=DEMOTAPE_DIR, timeout=timeout, executable="/bin/bash",
        env={**os.environ, "PATH": f"{DEMOTAPE_DIR}/.venv/bin:{os.environ.get('PATH', '')}"}
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"checked_urls": {}, "reported_issues": {}}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def check_url_status(url):
    """HEAD request a URL, return (status_code, ok_bool)."""
    req = urllib.request.Request(url, method="HEAD")
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; Demotape-QA/1.0)")
    try:
        resp = urllib.request.urlopen(req, timeout=URL_CHECK_TIMEOUT)
        return resp.status, True
    except urllib.error.HTTPError as e:
        return e.code, False
    except Exception:
        return None, False


def create_paperclip_issue(title, body):
    """Create a Paperclip issue using --data @file pattern."""
    import tempfile
    payload = json.dumps({"title": title, "description": body})
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(payload)
        tmppath = f.name
    try:
        cmd = (
            'BT=$(cat ~/.paperclip/adapter-token) && '
            f'curl -s -X POST "{PC_API}/api/companies/{COMPANY_ID}/issues" '
            '-H "Authorization: Bearer $BT" '
            '-H "Content-Type: application/json" '
            f'-d @{tmppath}'
        )
        out, err, rc = run_shell(cmd, timeout=10)
        if rc == 0 and out:
            try:
                return json.loads(out).get("id")
            except json.JSONDecodeError:
                pass
    finally:
        os.unlink(tmppath)
    return None


# ── Individual checks ────────────────────────────────────────────────────────

def check_duplicate_urls():
    """Same URL on same band more than once."""
    issues = []
    dupes = (
        Link.objects.values("band_id", "url")
        .annotate(cnt=Count("id"))
        .filter(cnt__gt=1)
    )
    for d in dupes:
        band = Band.objects.filter(id=d["band_id"]).first()
        links = Link.objects.filter(band_id=d["band_id"], url=d["url"]).order_by("id")
        issues.append({
            "type": "duplicate_url",
            "severity": "warning",
            "band": band.name if band else "Unknown",
            "url": d["url"],
            "count": d["cnt"],
            "link_ids": [l.id for l in links],
            "auto_fixable": True,
            "description": f"Same URL added {d['cnt']}× for band '{band.name if band else 'Unknown'}': {d['url'][:80]}",
        })
    return issues


def check_self_connections():
    """Connection where from_band == to_band."""
    issues = []
    for c in BandConnection.objects.filter(from_band=models.F("to_band")):
        issues.append({
            "type": "self_connection",
            "severity": "error",
            "band": c.from_band.name,
            "connection_type": c.connection_type,
            "connection_id": c.id,
            "auto_fixable": False,
            "description": f"Band '{c.from_band.name}' connected to itself ({c.connection_type})",
        })
    return issues


def check_invalid_types():
    """link_type / connection_type not in model choices."""
    issues = []
    valid_link = [t[0] for t in Link.LINK_TYPES]

    for l in Link.objects.exclude(link_type__in=valid_link):
        issues.append({
            "type": "invalid_link_type",
            "severity": "error",
            "band": l.band.name,
            "link_id": l.id,
            "link_type": l.link_type,
            "valid_types": valid_link,
            "auto_fixable": False,
            "description": f"Invalid link_type '{l.link_type}' on link #{l.id} (band: {l.band.name})",
        })

    valid_conn = [t[0] for t in BandConnection._meta.get_field("connection_type").choices]
    for c in BandConnection.objects.exclude(connection_type__in=valid_conn):
        issues.append({
            "type": "invalid_connection_type",
            "severity": "error",
            "from_band": c.from_band.name,
            "to_band": c.to_band.name,
            "connection_type": c.connection_type,
            "connection_id": c.id,
            "auto_fixable": False,
            "description": f"Invalid connection_type '{c.connection_type}' on conn #{c.id} ({c.from_band.name} → {c.to_band.name})",
        })
    return issues


def check_malformed_urls():
    """URLs with no scheme or netloc."""
    issues = []
    for link in Link.objects.all():
        try:
            p = urlparse(link.url)
            if not p.scheme or not p.netloc:
                issues.append({
                    "type": "malformed_url",
                    "severity": "warning",
                    "band": link.band.name,
                    "link_id": link.id,
                    "url": link.url,
                    "auto_fixable": False,
                    "description": f"Malformed URL on '{link.band.name}': '{link.url[:80]}'",
                })
        except Exception as e:
            issues.append({
                "type": "malformed_url",
                "severity": "error",
                "band": link.band.name,
                "link_id": link.id,
                "url": link.url,
                "error": str(e),
                "auto_fixable": False,
                "description": f"URL parse error on link #{link.id}: {e}",
            })
    return issues


def check_recent_urls(state):
    """Spot-check recently added URLs for 404s. Rate-limited."""
    issues = []
    cutoff = datetime.now() - timedelta(minutes=RECENT_WINDOW_MIN)
    recent = Link.objects.filter(created_at__gte=cutoff).order_by("-created_at")

    checked = state.get("checked_urls", {})
    runs = 0

    for link in recent:
        if runs >= MAX_URL_CHECKS:
            break
        url = link.url
        if url in checked:          # Already checked, skip
            continue
        runs += 1
        status, ok = check_url_status(url)
        checked[url] = {"status": status, "checked_at": datetime.now().isoformat(), "link_id": link.id}

        if status and 400 <= status < 500:
            issues.append({
                "type": "url_404",
                "severity": "warning",
                "band": link.band.name,
                "link_id": link.id,
                "url": url,
                "status_code": status,
                "auto_fixable": False,
                "description": f"URL returned {status} for '{link.band.name}': {url[:80]}",
            })

    state["checked_urls"] = checked
    return issues


def check_verification_levels():
    """Run Level-3 verification on links below Level 3. Returns issues for failed links."""
    if _run_l3_verification is None:
        return []

    print("\n  Running Level-3 link verification...")
    summary, results = _run_l3_verification(batch_size=50, dry_run=False, limit=50)

    issues = []
    for r in results:
        if r["action"] == "flag_dead":
            issues.append({
                "type": "l3_dead_link",
                "severity": "warning",
                "band": r["band"],
                "link_id": r["link_id"],
                "url": r["url"],
                "description": f"Level-3 check: dead link for '{r['band']}': {r['url'][:80]}",
                "auto_fixable": False,
            })
        elif r["action"] == "flag_ambiguous":
            issues.append({
                "type": "l3_ambiguous_link",
                "severity": "warning",
                "band": r["band"],
                "link_id": r["link_id"],
                "url": r["url"],
                "description": f"Level-3 check: ambiguous link for '{r['band']}': {r['url'][:80]}",
                "auto_fixable": False,
            })

    # Store summary in state for report
    return issues, summary


def check_orphaned_fks():
    """Connections referencing deleted bands (FK integrity)."""
    issues = []
    for c in BandConnection.objects.all():
        try:
            _ = c.from_band
            _ = c.to_band
        except Band.DoesNotExist:
            issues.append({
                "type": "orphaned_connection",
                "severity": "error",
                "connection_id": c.id,
                "from_band_id": c.from_band_id,
                "to_band_id": c.to_band_id,
                "auto_fixable": False,
                "description": f"Connection #{c.id} references deleted band (from={c.from_band_id}, to={c.to_band_id})",
            })
    return issues


def check_verification_progress():
    """Report verification progress: counts per level, recently promoted/flagged."""
    total = Link.objects.count()
    by_level = dict(
        Link.objects.values_list("verification_level")
        .annotate(cnt=Count("id"))
        .order_by("verification_level")
    )

    level_1 = by_level.get(1, 0)
    level_2 = by_level.get(2, 0)
    level_3 = by_level.get(3, 0)
    level_4 = by_level.get(4, 0)

    flagged = Link.objects.filter(
        verification_notes__contains="Ambiguous"
    ).count()

    issues = []
    if flagged > 0:
        issues.append({
            "type": "flagged_links",
            "severity": "warning",
            "auto_fixable": False,
            "description": f"{flagged} links flagged by Level-3 verifier for manual review",
        })

    return {
        "total": total,
        "level_1": level_1,
        "level_2": level_2,
        "level_3": level_3,
        "level_4": level_4,
        "flagged": flagged,
        "issues": issues,
    }


# ── Report ───────────────────────────────────────────────────────────────────

def append_to_log(issues, l3_summary=None, verification_summary=None):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"\n## {ts} — QA Run", f"- **Issues:** {len(issues)}"]

    # Level-3 verification summary section (from link_verifier run)
    if l3_summary:
        lines.append("")
        lines.append("### Level-3 Verification Summary")
        lines.append(f"- Links checked: {l3_summary.get('total_checked', 0)}")
        lines.append(f"- Promoted to Level 3: {l3_summary.get('promoted', 0)}")
        lines.append(f"- Dead links: {l3_summary.get('flagged_dead', 0)}")
        lines.append(f"- Ambiguous (collision): {l3_summary.get('flagged_ambiguous', 0)}")
        lines.append(f"- Flagged for review: {l3_summary.get('flagged_review', 0)}")

    # Verification progress summary (per-level counts)
    if verification_summary:
        lines.append("")
        lines.append("### Verification Summary")
        lines.append(f"- Total links: {verification_summary['total']}")
        lines.append(f"- Level 1 (Discovered): {verification_summary.get('level_1', 0)}")
        lines.append(f"- Level 2 (Cross-Referenced): {verification_summary.get('level_2', 0)}")
        lines.append(f"- Level 3 (Auto-Verified): {verification_summary.get('level_3', 0)}")
        lines.append(f"- Level 4 (Admin Confirmed): {verification_summary.get('level_4', 0)}")
        lines.append(f"- Flagged for review: {verification_summary.get('flagged', 0)}")

    for i in issues:
        lines.append(f"- **[{i['severity'].upper()}]** {i['description']}")
    if not issues:
        lines.append("- ✅ Clean — no issues found.")
    with open(QA_LOG, "a") as f:
        f.write("\n".join(lines) + "\n")


def create_issues(all_issues, state):
    """Create Paperclip issues for new errors — clustered, capped at 3 per run."""
    MAX_ISSUES_PER_RUN = 3
    MAX_LOGGED_PER_CLUSTER = 5
    reported = state.get("reported_issues", {})
    new = []

    # Group issues by type, keeping the first few as examples
    clusters = {}
    for issue in all_issues:
        if issue["severity"] != "error":
            continue
        itype = issue["type"]
        if itype not in clusters:
            clusters[itype] = []
        clusters[itype].append(issue)

    for itype, issues in sorted(clusters.items()):
        if len(new) >= MAX_ISSUES_PER_RUN:
            print(f"  ⚠️  Issue cap reached ({MAX_ISSUES_PER_RUN}); remaining clusters logged only.")
            break
        key = f"cluster:{itype}"
        if key in reported:
            continue
        examps = issues[:MAX_LOGGED_PER_CLUSTER]
        desc_lines = [f"- {e['description']}" for e in examps]
        if len(issues) > MAX_LOGGED_PER_CLUSTER:
            desc_lines.append(f"- …and {len(issues)-MAX_LOGGED_PER_CLUSTER} more")
        title = f"[QA] {len(issues)}× {itype.replace('_', ' ').title()}"
        body = (f"Automated QA check found **{len(issues)}** issues of type `{itype}`.\n\n"
                f"Examples:\n" + "\n".join(desc_lines) + "\n")
        issue_id = create_paperclip_issue(title, body)
        if issue_id:
            reported[key] = issue_id
            new.append(issue_id)
            print(f"  📋 Paperclip issue created: {issue_id} ({len(issues)} issues)")

    state["reported_issues"] = reported
    return new


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  QA CHECKER — demotape link/connection verification")
    print("=" * 55)

    state = load_state()
    all_issues = []
    l3_summary = None

    verification_summary = None
    checks = [
        ("duplicate_urls",      check_duplicate_urls),
        ("self_connections",    check_self_connections),
        ("invalid_types",       check_invalid_types),
        ("malformed_urls",      check_malformed_urls),
        ("orphaned_fks",        check_orphaned_fks),
        ("recent_url_404s",     lambda: check_recent_urls(state)),
        ("verification_progress", check_verification_progress),
    ]

    for name, fn in checks:
        try:
            found = fn()
            if name == "verification_progress":
                # found is a dict with 'issues' key
                verification_summary = found
                found_issues = found.get("issues", [])
                all_issues.extend(found_issues)
                if found_issues:
                    print(f"  ⚠️  {name}: {len(found_issues)} issue(s)")
                else:
                    print(f"  ✅ {name}: clean — total={found.get('total', 0)} links")
            else:
                all_issues.extend(found)
                if found:
                    print(f"  ⚠️  {name}: {len(found)} issue(s)")
                else:
                    print(f"  ✅ {name}: clean")
        except Exception as e:
            print(f"  ❌ {name}: ERROR — {e}")

    # Level-3 link verification
    try:
        l3_result = check_verification_levels()
        if isinstance(l3_result, tuple):
            l3_issues, l3_summary = l3_result
        else:
            l3_issues = l3_result
        all_issues.extend(l3_issues)
        if l3_issues:
            print(f"  ⚠️  verification_levels: {len(l3_issues)} issue(s)")
        else:
            print(f"  ✅ verification_levels: clean")
    except Exception as e:
        print(f"  ❌ verification_levels: ERROR — {e}")

    errors   = [i for i in all_issues if i["severity"] == "error"]
    warnings = [i for i in all_issues if i["severity"] == "warning"]

    if not all_issues:
        print(f"\n  ✅ QA CHECK PASSED — 0 issues.")
    else:
        print(f"\n  ⚠️  QA CHECK: {len(errors)} error(s), {len(warnings)} warning(s).")

    append_to_log(all_issues, l3_summary=l3_summary, verification_summary=verification_summary)
    create_issues(all_issues, state)
    save_state(state)

    if errors:
        sys.exit(2)
    elif all_issues:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
