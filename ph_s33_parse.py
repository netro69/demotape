"""Session 33 — parse fetched underground sources for Prozac+."""
import glob
import json
import re

BASE = "/home/ubuntu/Projects/demotape/research_output/"


def read(name):
    with open(BASE + name, encoding="utf-8") as f:
        return f.read()


# --- TPB results ---
def parse_tpb(name):
    html = read(name)
    results = []
    # tpb.party search results: links to /torrent/<id>/<slug>.html
    for m in re.finditer(r'href="(/torrent/(\d+)/[^"]+)"[^>]*>([^<]+)</a>', html):
        slug, tid, title = m.group(1), m.group(2), m.group(3)
        results.append({"id": tid, "title": title.strip(), "url": "https://thepiratebay.org" + slug})
    return results


for f in ["s33_tpb_prozacplus.txt", "s33_tpb_acido_acida.txt", "s33_tpb_testa_plastica.txt"]:
    res = parse_tpb(f)
    print("=== %s: %d results ===" % (f, len(res)))
    for r in res[:20]:
        print("  - [%s] %s" % (r["id"], r["title"][:100]))

# --- IA results ---
for f in ["s33_ia_prozac_acido.txt", "s33_ia_acido_acida.txt", "s33_ia_testa_plastica_1996.txt",
          "s33_ia_prozac_pordenone.txt", "s33_ia_vox_pop_pordenone.txt"]:
    try:
        j = json.loads(read(f))
        docs = j.get("response", {}).get("docs", [])
        print("=== %s: %d hits ===" % (f, len(docs)))
        for d in docs[:10]:
            print("  - %s | %s" % (d.get("identifier"), (d.get("title") or "")[:80]))
    except Exception as e:
        print("=== %s: parse error %s ===" % (f, e))

# --- Invidious (41 bytes = error, check) ---
sample = read("s33_yt_prozacplus_acido_acida.txt")
print("=== Invidious sample (41b): %r ===" % sample[:100])
