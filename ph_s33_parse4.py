"""Session 33 — TPB torrent relevance check + Usenet (Google Groups) attempt."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
BASE = "/home/ubuntu/Projects/demotape/research_output/"


def read(name):
    with open(BASE + name, encoding="utf-8") as f:
        return f.read()


def fetch(url, timeout=30, extra=None):
    try:
        h = {"User-Agent": UA, "Accept": "application/json"}
        if extra:
            h.update(extra)
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


# --- TPB relevance: filter torrent slugs for the Italian band ---
BAND_KEYS = ["acido", "acida", "testa_plastica", "testa plastica", "pordenone", "vox_pop"]
MEMBER_KEYS = ["accusani", "imelio", "mangoni"]
for fname in ["s33_tpb_prozacplus.txt", "s33_tpb_acido_acida.txt", "s33_tpb_testa_plastica.txt"]:
    html = read(fname)
    slugs = sorted(set(re.findall(r"/torrent/(\d+)/([^\"<#]*)", html)))
    hits = [(tid, s) for tid, s in slugs if any(k in s.lower() for k in BAND_KEYS + MEMBER_KEYS)]
    print("=== %s — %d torrents, %d band-relevant ===" % (fname, len(slugs), len(hits)))
    for tid, s in hits:
        print("  *** [%s] %s | https://thepiratebay.org/torrent/%s" % (tid, s, tid))

# --- Usenet: Google Groups search (was 429 in s32; retry) ---
for q in ["prozac pordenone", "acido acida prozac", "testa plastica prozac"]:
    u = "https://groups.google.com/g/italian-rock/search?q=%s" % urllib.parse.quote(q)
    raw = fetch(u, timeout=20)
    print("GG %-25s -> %s" % (q, "OK %d bytes" % len(raw) if not raw.startswith("__FETCH_ERROR__") else raw[:60]))

# fallback: usenet archive via newsgroup text archives (alt.music.italian / it.arti.musica)
for q in ["prozac", "acido acida"]:
    u = "http://www.usenetarchives.com/search.php?q=%s" % urllib.parse.quote(q)
    raw = fetch(u, timeout=20)
    print("UA %-25s -> %s" % (q, "OK %d bytes" % len(raw) if not raw.startswith("__FETCH_ERROR__") else raw[:60]))
