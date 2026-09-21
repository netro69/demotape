"""Session 33 — read fetched page extracts."""
import re

BASE = "/home/ubuntu/Projects/demotape/research_output/"

for f in ["s33_page_rollingstone_imelio.txt", "s33_page_xl_generazione.txt", "s33_page_giovanniweb.txt"]:
    t = open(BASE + f, encoding="utf-8").read()
    print("=" * 20, f, "=" * 20)
    m = re.search(r"(Si è spenta|Noi, la Generazione|Acido Acida|If you want to analyze)", t)
    start = m.start() if m else 0
    print(t[start : start + 3500])
    print()
