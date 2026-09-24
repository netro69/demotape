#!/usr/bin/env python3
"""
Fisherman Loop — One-band-at-a-time research dispatcher.
Queries the DB for the most under-researched band, spawns a subagent to research it,
and exits. The cron job re-runs this script to pick up the next band.

Exit codes:
  0 = researched a band (cron should re-run)
  1 = no bands need research (cron can stop)
  2 = error
"""

import subprocess
import sys
import json
import os
import re
import urllib.request

DEMOTAPE_DIR = os.path.expanduser("~/Projects/demotape")
COMPANY_ID = "9b1bb8a3-192f-4c4e-a406-9449c442a8e9"
FISHERMAN_AGENT_ID = "28788729-94d9-4d1c-a0d2-fdd1ea48ac72"
PAPERCLIP_API = "http://43.157.13.93:3100/api"


def run_shell(cmd, timeout=30):
    """Run a shell command in the Demotape venv."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=DEMOTAPE_DIR,
        timeout=timeout,
        executable="/bin/bash",
        env={**os.environ, "PATH": f"{DEMOTAPE_DIR}/.venv/bin:{os.environ.get('PATH', '')}"}
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def get_open_research_bands():
    """Fetch all open [AUTO] Research band issues for The Fisherman and return a set of band names."""
    try:
        token = os.environ.get("PAPERCLIP_API_KEY", "")
        if not token:
            # Try reading from file
            token_path = os.path.expanduser("~/.paperclip/api_key.txt")
            if os.path.exists(token_path):
                with open(token_path) as f:
                    token = f.read().strip()
            else:
                # Fallback: read from adapter token
                adapter_path = os.path.expanduser("~/.paperclip/adapter-token")
                if os.path.exists(adapter_path):
                    with open(adapter_path) as f:
                        token = f.read().strip()

        if not token:
            print("WARNING: No Paperclip token found — cannot check for open issues", file=sys.stderr)
            return set()

        url = f"{PAPERCLIP_API}/companies/{COMPANY_ID}/issues?status=todo&limit=100"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            todo_issues = json.loads(resp.read().decode())

        url2 = f"{PAPERCLIP_API}/companies/{COMPANY_ID}/issues?status=in_progress&limit=100"
        req2 = urllib.request.Request(url2, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req2, timeout=15) as resp:
            in_progress_issues = json.loads(resp.read().decode())

        all_open = todo_issues + in_progress_issues

        # Filter to only The Fisherman's [AUTO] Research band issues
        band_names = set()
        pattern = re.compile(r'^\[AUTO\] Research band:\s*(.+)$')
        for issue in all_open:
            if issue.get("assigneeAgentId") != FISHERMAN_AGENT_ID:
                continue
            match = pattern.match(issue.get("title", ""))
            if match:
                band_names.add(match.group(1).strip().lower())

        print(f"Open Fisherman research issues for: {band_names}")
        return band_names

    except Exception as e:
        print(f"WARNING: Failed to fetch open issues: {e}", file=sys.stderr)
        return set()  # If we can't check, proceed (don't block the loop)


def find_next_band(exclude_names=None):
    """Query DB for the most under-researched band, excluding names in exclude_names (case-insensitive)."""
    exclude_clause = ""
    if exclude_names:
        # Case-insensitive exclude using Lower() annotation
        safe_list = ", ".join(f"'{n.replace(chr(39), chr(39)*2)}'" for n in exclude_names)
        exclude_clause = f".annotate(_lname=Lower('name')).exclude(_lname__in=[{safe_list}])"

    template = """
import django, os, sys, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from django.db.models import Count, Q
from django.db.models.functions import Lower
from apps.core.models import Band, Link, BandConnection

bands = Band.objects.annotate(
    link_count=Count('links', distinct=True),
    conn_count=Count('connections_from', distinct=True) + Count('connections_to', distinct=True),
).order_by('link_count', 'conn_count', '-id')

priority = bands.filter(
    Q(link_count__lt=8) | Q(conn_count__lt=8)
).exclude(slug__in=['ghost-records']).exclude(status='flagged')__EXCLUDE_CLAUSE__

if not priority.exists():
    print('NO_BANDS')
else:
    band = priority.first()
    print(json.dumps({
        'id': band.id,
        'name': band.name,
        'slug': band.slug,
        'description': band.bio or '',
        'link_count': band.link_count,
        'conn_count': band.conn_count
    }))
"""
    script = template.replace("__EXCLUDE_CLAUSE__", exclude_clause)
    script_path = "/tmp/find_band.py"
    with open(script_path, 'w') as f:
        f.write(script)
    
    out, err, rc = run_shell(f"source .venv/bin/activate && python {script_path}")
    if rc != 0:
        print(f"DB query failed: {err}", file=sys.stderr)
        return None
    
    lines = [l for l in out.split('\n') if l.strip().startswith('{')]
    if lines:
        try:
            return json.loads(lines[-1])
        except json.JSONDecodeError as e:
            print(f"Parse failed: {e}", file=sys.stderr)
            return None
    return None


def spawn_fisherman(band):
    """Create a Paperclip issue for Fisherman to research one band."""
    title = f"[AUTO] Research band: {band['name']}"
    body = f"""Automated research task for Demotape.

## Target Band
- **Name:** {band['name']}
- **Slug:** {band['slug']}
- **ID:** {band['id']}
- **Current links:** {band['link_count']}
- **Current connections:** {band['conn_count']}

## Hard Constraints (READ FIRST)
- **90% ITALIAN BANDS ONLY.** Foreign bands ONLY if directly related to Italian scene (collaborations, tours, label-mates, shared members with Italian bands).
- **Time period:** Strictly **1985-2000** era. No post-2000 bands unless they evolved from an active pre-2000 band.
- **Priority:** Small, obscure, forgotten bands. Wikipedia links for famous bands only.
- **Magazine sources:** Always search "[band name] Rockerilla" and "[band name] Rumore" — these are key Italian underground music magazines.

## Instructions
1. **SEARCH FOR NEW BANDS FIRST:**
   - Search Italian Wikipedia categories: "Categoria:Gruppi musicali italiani", "Categoria:Gruppi punk italiani", "Categoria:Gruppi new wave italiani", "Categoria:Gruppi post-punk italiani"
   - Search Rockerilla magazine archives for band mentions
   - Search Rumore magazine archives for band mentions
   - Search Il Mucchio / Il Mucchio Selvaggio archives
   - Search Trippa Shake fanzine archives
   - Search Discogs for Italian bands 1985-2000
   - Search old forums: RadioChitarra, DeBaser, Italian newsgroups
   - Search YouTube for "Italian underground 80s", "Italian punk 80s", "Italian new wave 80s"
2. **FAMOUS BANDS** (Negrita, Marlene Kuntz, Afterhours, CCCP, etc.): Just add a Wikipedia link if missing → move on. Do NOT deep-research.
3. **OBSCURE BANDS** (under-researched, zero links): Deep research — **search Italian Wikipedia FIRST** (it.wikipedia.org/wiki/[band_name]), then Rockerilla magazine, Rumore magazine, Discogs, English Wikipedia, Metal-Archives, old newsgroups, official sites, BBS archives.
4. **Italian Wikipedia is the best source for Italian bands** — more detailed than English Wikipedia for local/obscure acts. Always search it.wikipedia.org first.
5. **Magazine sources:** Always search "[band name] Rockerilla", "[band name] Rumore", "[band name] Il Mucchio", "[band name] Il Mucchio Selvaggio", and fanzines like "[band name] Trippa Shake" — these are key Italian underground music magazines and fanzines that documented small bands.
6. Add any found URLs as Link objects (link_type: video, website, social, purchase, streaming, archive, other)
7. **TRACK FANZINES:** If a review or mention appears in a fanzine (Rockerilla, Rumore, Il Mucchio, Trippa Shake, etc.), add it as a Fanzine and FanzineReview object. This preserves the critical connection between band and publication.
8. Find related bands and create BandConnection objects
9. Update the band's bio if you find more info
10. Do NOT add duplicate Links

## Database
```bash
cd ~/Projects/demotape && source .venv/bin/activate && python manage.py shell -c "<python>"
```

## Save Progress
Append findings to ~/Documents/Obsidian/Vault/projects/demotape-research-log.md
"""
    
    payload = json.dumps({
        "title": title,
        "description": body,
        "status": "todo",
        "priority": "medium",
        "assigneeAgentId": "28788729-94d9-4d1c-a0d2-fdd1ea48ac72"  # The Fisherman
    })
    cmd = (
        f'BT=$(cat ~/.paperclip/adapter-token) && '
        f'curl -s -X POST "http://localhost:3100/api/companies/{COMPANY_ID}/issues" '
        f'-H "Authorization: Bearer $BT" '
        f'-H "Content-Type: application/json" '
        f'-d {json.dumps(payload)}'
    )
    out, err, rc = run_shell(cmd)
    # curl exit 0 does NOT mean the API accepted it — verify the response body
    if rc != 0:
        print(f"Dispatch curl failed: {err}", file=sys.stderr)
        return False
    if '"error"' in out or '"id"' not in out:
        print(f"Dispatch rejected by API: {out[:200]}", file=sys.stderr)
        return False
    return True


def main():
    print("=" * 50)
    print("FISHERMAN LOOP — checking for un researched bands...")

    # Fetch open Fisherman research issues to skip bands already in the queue
    open_bands = get_open_research_bands()
    if open_bands:
        print(f"⏸ Skipping bands already in research queue: {open_bands}")

    band = find_next_band(exclude_names=open_bands)
    if band is None:
        print("✅ No bands need research. Queue is dry.")
        sys.exit(1)

    print(f"🎯 Next target: {band['name']} (id={band['id']}, links={band['link_count']}, conns={band['conn_count']})")

    if spawn_fisherman(band):
        print(f"✅ Fisherman dispatched for {band['name']}")
        print("⏰ Cron will re-run to pick up the next band")
        sys.exit(0)
    else:
        print("❌ Failed to spawn Fisherman")
        sys.exit(2)


if __name__ == "__main__":
    main()
