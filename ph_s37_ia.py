"""Session 37 — underground source checks for Scisma: Internet Archive API."""
import json
import os
import re
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace"))


QUERIES = [
    "scisma",
    "scisma armstrong",
    "rosemary plexiglas",
    "bombardando cortina",
    "pezzetti di carta scisma",
    "vive le roi",
    '"scisma" AND mediatype:audio',
]

print("=== INTERNET ARCHIVE advancedsearch ===")
for q in QUERIES:
    url = (
        "https://archive.org/advancedsearch.php?q="
        + urllib.parse.quote(q)
        + "&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=mediatype&rows=10&output=json"
    )
    try:
        d = get_json(url)
        docs = d.get("response", {}).get("docs", [])
        print(f"\n-- query: {q} -> {len(docs)} hits")
        for doc in docs:
            print("   ", doc.get("identifier"), "|", str(doc.get("title"))[:70], "|", doc.get("mediatype"), "|", doc.get("year"))
    except Exception as e:
        print(f"\n-- query: {q} FAILED: {e}")

print("\n=== INTERNET ARCHIVE metadata for promising identifiers ===")
for ident in ["scisma", "RosemaryPlexiglas"]:
    try:
        d = get_json(f"https://archive.org/metadata/{ident}")
        if d.get("metadata"):
            print(ident, "->", d["metadata"].get("title"))
        else:
            print(ident, "-> no metadata")
    except Exception as e:
        print(ident, "FAILED:", e)
