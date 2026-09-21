"""Session 37 — YouTube search via yt-dlp ytsearch (bypasses Invidious 403)."""
import json
import subprocess

YTDLP = "/home/ubuntu/.hermes/hermes-agent/venv/bin/yt-dlp"

QUERIES = [
    "scisma armstrong",
    "scisma tungsteno",
    "scisma l'innocenza",
    "scisma centro",
    "scisma vive le roi",
    "scisma benvegnu live",
    "scisma rosemary plexiglas full album",
    "scisma 1998",
]

for q in QUERIES:
    print(f"\n=== ytsearch8: {q} ===")
    try:
        out = subprocess.run(
            [YTDLP, f"ytsearch8:{q}", "--dump-json", "--flat-playlist", "--no-warnings"],
            capture_output=True, text=True, timeout=120,
        )
        if out.returncode != 0:
            print("FAILED:", out.stderr[:300])
            continue
        for line in out.stdout.strip().splitlines():
            try:
                d = json.loads(line)
                print("  ", d.get("id"), "|", str(d.get("title"))[:80], "|", str(d.get("channel") or d.get("uploader"))[:40], "|", d.get("duration"))
            except Exception:
                pass
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
