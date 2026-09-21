"""Session 30 — fetch underground pages for Massimo Volume, extract text."""
import re
import html
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"

PAGES = {
    "breakfastjumpers_bootleg": "https://breakfastjumpers.blogspot.com/2010/09/massimo-volume-registrazione-del-10-11.html",
    "mvstanze_demo": "http://mvstanze.blogspot.com/2005/02/demo.html",
    "mvstanze_bio": "http://mvstanze.blogspot.com/p/biografia.html",
    "storiadellamusica_stanze": "http://www.storiadellamusica.it/avant_post_rock/post_rock/massimo_volume-stanze(underground_records-1993).html",
    "beatstream_bologna": "http://www.beatstream.it/ground/band.asp?art_id=241&cat_id=1&genre_id=10",
}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read().decode("utf-8", errors="ignore")
        return raw
    except Exception as e:
        return f"__FETCH_ERROR__ {e}"

def clean(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", t)).strip()

for name, url in PAGES.items():
    print("=" * 20, name, "=" * 20)
    raw = fetch(url)
    if raw.startswith("__FETCH_ERROR__"):
        print(raw)
    else:
        print(clean(raw)[:2200])
    print()
