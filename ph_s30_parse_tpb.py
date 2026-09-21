"""Session 30 — parse TPB via apibay API + full IA results."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


# 1. apibay (TPB backend) — search all categories for "massimo volume"
for q in ["massimo volume", "massimo%20volume"]:
    u = "https://apibay.org/q.php?q=%s&cat=100" % q  # cat 100 = audio
    r = fetch(u)
    print("=== apibay audio '%s' ===" % q)
    print(r[:1500])
    print()
    u = "https://apibay.org/q.php?q=%s&cat=200" % q  # cat 200 = video
    r = fetch(u)
    print("=== apibay video '%s' ===" % q)
    print(r[:1500])
    print()

# 2. Full IA search results
print("=== IA 'massimo volume' full docs ===")
raw = open("/tmp/s30_ia_search.txt", encoding="utf-8", errors="ignore").read()
try:
    docs = json.loads(raw).get("response", {}).get("docs", [])
    for d in docs:
        print(d.get("identifier"), "|", d.get("title"))
except Exception as e:
    print("parse error:", e)

# 3. IA search for related terms
for q in ["demo nero", "santo niente", "umberto palazzo"]:
    qe = urllib.parse.quote('"%s"' % q)
    j = fetch("https://archive.org/advancedsearch.php?q=%s&fl%%5B%%5D=identifier&fl%%5B%%5D=title&rows=10&output=json" % qe)
    print()
    print("=== IA '%s' ===" % q)
    if j.startswith("__FETCH_ERROR__"):
        print(j)
    else:
        try:
            docs = json.loads(j).get("response", {}).get("docs", [])
            print("numFound:", json.loads(j)["response"]["numFound"])
            for d in docs:
                print(d.get("identifier"), "|", d.get("title"))
        except Exception as e:
            print("parse error:", e)
