"""Session 31 — fetch la_citta_futura OCR text, check for Massimo Volume coverage."""
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0"
url = "https://archive.org/download/la_citta_futura-5-6_2000/la_citta_futura-5-6_2000_djvu.txt"
req = urllib.request.Request(url, headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=60) as r:
    txt = r.read().decode("utf-8", errors="ignore")
print("total chars:", len(txt))
low = txt.lower()
for kw in ["massimo volume", "clementi", "sommacal", "burattini", "stanze", "lungo i bordi"]:
    idx = low.find(kw)
    if idx >= 0:
        s = max(0, idx - 250)
        print("\n### MATCH:", kw)
        print(txt[s:idx + 350].replace("\n", " "))
    else:
        print("\n### no match:", kw)
