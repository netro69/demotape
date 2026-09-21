"""Session 37 — check MTV Alternative Nation IA items for Scisma track; YouTube search via Invidious; oembed verify."""
import json
import re
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


# 1. MTV Alternative Nation items — search contents for Scisma
print("=== MTV Alternative Nation items: full-text grep for Scisma ===")
for ident in [
    "mtv-alternative-nation-last-show",
    "2025-04-02-mtv-alternative-nation",
    "mtv-germany-alternative-nation-november-20a-2024",
    "2025-08-06-mtv-alternative-nation",
]:
    try:
        d = json.loads(get(f"https://archive.org/metadata/{ident}"))
        desc = d.get("description", "")
        files = " ".join(f.get("name", "") for f in d.get("files", []))
        blob = (desc + " " + files).lower()
        if "scisma" in blob or "plexiglas" in blob:
            print(f"\n-- {ident}: SCISMA FOUND")
            for m in re.finditer(r"[^.\n]*(?:scisma|plexiglas)[^.\n]*", blob, re.I):
                print("   ...", m.group(0)[:200])
        else:
            print(f"-- {ident}: no scisma mention (desc {len(desc)} chars, {len(d.get('files', []))} files)")
    except Exception as e:
        print(f"-- {ident} FAILED: {e}")

# 2. YouTube search via Invidious instance (yt.chocolatemoo53.com shared by user)
print("\n=== YouTube search via Invidious ===")
Q = ["scisma", "scisma armstrong", "scisma tungsteno", "scisma l'innocenza", "scisma centro", "scisma vive le roi", "scisma live"]
for q in Q:
    try:
        raw = get("https://yt.chocolatemoo53.com/api/v1/search?q=" + urllib.parse.quote(q) + "&type=video")
        vids = json.loads(raw)
        print(f"\n-- {q}: {len(vids)} results")
        for v in vids[:8]:
            print("   ", v.get("videoId"), "|", str(v.get("title"))[:75], "|", str(v.get("author"))[:40], "|", v.get("lengthSeconds"))
    except Exception as e:
        print(f"-- {q} FAILED: {e}")
