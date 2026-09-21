"""Session 30 — parse TPB results + check archive.org item + 1337x."""
import re
import html
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"__FETCH_ERROR__ {e}"


print("=" * 20, "TPB search: massimo volume", "=" * 20)
raw = open("/tmp/tpb.html", encoding="utf-8", errors="ignore").read()
rows = re.findall(r'<a href="(/torrent/\d+/[^"]+)"[^>]*class="detLink".*?>(.*?)</a>', raw, flags=re.S)
if not rows:
    # try alternate structure
    links = re.findall(r'href="(//thepiratebay\.org/torrent/\d+/[^"]+)"[^>]*>([^<]+)<', raw)
    for u, t in links:
        print("TPB:", html.unescape(t), "| https:" + u)
    if not links:
        print("[no torrent rows matched; page head:]")
        print(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw))[:600])
else:
    for u, t in rows:
        print("TPB:", html.unescape(re.sub(r"<[^>]+>", "", t)), "| https://thepiratebay.org" + u)

print()
print("=" * 20, "Archive.org item: massimo-volume-vittoria-burattini", "=" * 20)
j = fetch("https://archive.org/metadata/massimo-volume-vittoria-burattini")
if j.startswith("__FETCH_ERROR__"):
    print(j)
else:
    import json
    try:
        meta = json.loads(j)
        print("title:", meta.get("metadata", {}).get("title"))
        print("desc:", str(meta.get("metadata", {}).get("description"))[:300])
        for f in meta.get("files", [])[:15]:
            print("file:", f.get("name"), f.get("size"), f.get("format"))
    except Exception as e:
        print("parse error:", e)

print()
print("=" * 20, "Archive.org search: massimo volume (all items)", "=" * 20)
j2 = fetch("https://archive.org/advancedsearch.php?q=%22massimo+volume%22&fl%5B%5D=identifier&fl%5B%5D=title&rows=20&output=json")
if j2.startswith("__FETCH_ERROR__"):
    print(j2)
else:
    import json
    try:
        docs = json.loads(j2).get("response", {}).get("docs", [])
        for d in docs:
            print("IA:", d.get("identifier"), "|", d.get("title"))
    except Exception as e:
        print("parse error:", e)

print()
print("=" * 20, "1337x search", "=" * 20)
x = fetch("https://1337x.to/search/massimo+volume/1/")
if x.startswith("__FETCH_ERROR__"):
    print(x)
else:
    names = re.findall(r'<a href="/torrent/(\d+)/[^"]+">([^<]+)</a>', x)
    if names:
        for i, t in names:
            print("1337x:", html.unescape(t), "| https://1337x.to/torrent/" + i + "/")
    else:
        print("[no results]")
