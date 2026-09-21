"""Session 33 — fetch key Prozac+ pages via urllib (web_extract backend is search-only)."""
import re
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
BASE = "/home/ubuntu/Projects/demotape/research_output/"


def fetch(url, timeout=30):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return "__FETCH_ERROR__ %s" % e


def strip(html):
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&nbsp;?", " ", html)
    html = re.sub(r"&amp;", "&", html)
    html = re.sub(r"\s+", " ", html)
    return html.strip()


PAGES = {
    "giovanniweb": "https://www.giovanniweb.it/prozac/prozacdiscuk.htm",
    "wiki_it": "https://it.wikipedia.org/wiki/Prozac+",
    "rollingstone_imelio": "https://www.rollingstone.it/musica/news-musica/e-morta-elisabetta-imelio-dei-prozac/505633/",
    "redbull_20anni": "https://www.redbull.com/it-it/what-the-faq-acido-acida-prozac+",
    "xl_generazione": "https://xl.repubblica.it/articoli/noi-la-generazione-prozac/97338/",
}

for name, url in PAGES.items():
    raw = fetch(url)
    if raw.startswith("__FETCH_ERROR__"):
        print("=== %s: %s ===" % (name, raw[:100]))
        with open(BASE + "s33_page_%s.err" % name, "w") as f:
            f.write(raw)
        continue
    txt = strip(raw)
    with open(BASE + "s33_page_%s.txt" % name, "w", encoding="utf-8") as f:
        f.write(txt)
    print("=== %s: %d chars saved ===" % (name, len(txt)))
    print(txt[:600])
    print()
