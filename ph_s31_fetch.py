"""Session 31 — fetch underground sources for Massimo Volume (round 2)."""
import json
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
OUT = "/tmp/s31_%s.txt"


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


# 1. TPB via apibay static API
for q in ["massimo volume", "massimo+volume"]:
    raw = fetch("https://apibay.org/q.php?q=" + urllib.parse.quote(q))
    with open(OUT % ("apibay_" + q.replace(" ", "_").replace("+", "_")), "w") as f:
        f.write(raw)
    print("apibay", q, len(raw))

# 2. IA metadata for interesting identifiers
for ident in ["massimo-volume-vittoria-burattini", "42IlNuotatoreCheever",
              "la_citta_futura-5-6_2000", "Roxyto2406.04.2011"]:
    j = fetch("https://archive.org/metadata/" + ident)
    with open(OUT % ("iameta_" + ident[:24].replace(".", "_")), "w") as f:
        f.write(j)
    print("iameta", ident, len(j))

# 3. Invidious (user-shared instance) — YouTube rips search
for q in ["massimo volume demo nero", "massimo volume stanze full album",
          "massimo volume lungo i bordi", "massimo volume live 1993"]:
    u = "https://yt.chocolatemoo53.com/api/v1/search?q=" + urllib.parse.quote(q) + "&type=video"
    j = fetch(u)
    with open(OUT % ("yt_" + q.replace(" ", "_")), "w") as f:
        f.write(j)
    print("yt", q, len(j))

# 4. Google Groups / Usenet
u = "https://groups.google.com/g/alt.rock/search?q=" + urllib.parse.quote('"massimo volume"')
raw = fetch(u)
with open(OUT % "ggroups", "w") as f:
    f.write(raw)
print("ggroups", len(raw))

# 5. Blog posts (Demo Nero rips)
for name, url in [
    ("radiomolotov", "https://radiomolotov.blogspot.com/2009/08/massimo-volume-demo-nero-1992.html"),
    ("breakfastjumpers", "https://breakfastjumpers.blogspot.com/2010/09/massimo-volume-registrazione-del-10-11.html"),
]:
    raw = fetch(url)
    with open(OUT % name, "w") as f:
        f.write(raw)
    print(name, len(raw))

print("done")
