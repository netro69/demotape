"""Session 39 — fetch + strip HTML to text for Brandelli D'Odio key pages."""
import html
import os
import re
import urllib.request

OUT = os.path.expanduser("~/.hermes/profiles/amanda/cache/scratch/s39")
os.makedirs(OUT, exist_ok=True)

URLS = [
    ("radiomolotov", "https://radiomolotov.blogspot.com/2010/02/brandelli-dodio-sopravvivo-2006.html"),
    ("discomarket", "https://disco.market/discographies/artist/286146-brandelli-d-odio/"),
    ("brobtilt", "https://brobtilttapes.wordpress.com/2022/06/25/brandelli-dodio-ita-allarme-ferite-1995/"),
    ("1000flights_sopravvivo", "https://1000flights.blogspot.com/2014/11/brandelli-dodio-sopravvivo-double-cd.html"),
    ("1000flights_fullslap", "https://1000flights.blogspot.com/2015/05/brandelli-dodiofull-slap-anti.html"),
    ("discogs_artist", "https://www.discogs.com/artist/286146-Brandelli-DOdio"),
    ("rym_artist", "https://rateyourmusic.com/artist/brandelli_dodio"),
    ("lastfm", "https://www.last.fm/music/Brandelli+d`odio"),
    ("vimeo_apoteosi", "https://vimeo.com/55933414"),
    ("scaglie_split", "https://scagliedirumore.bandcamp.com/album/piz8-brandelli-dodio-the-split-tape-23-years-after"),
    ("bandcamp_bdo", "https://brandelliodio.bandcamp.com/"),
    ("agipunk_comp", "https://agipunkrecords.bandcamp.com/album/ag04-vv-aa-italia-la-punk"),
    ("cliggo", "https://music.cliggo.com/artist/286146-Brandelli_D'Odio/track/Tic-Tac_Allarme"),
]

for name, url in URLS:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"})
        raw = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
    except Exception as e:
        print(f"FAIL {name}: {e}")
        continue
    t = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    path = os.path.join(OUT, name + ".txt")
    with open(path, "w") as f:
        f.write(t)
    print(f"OK {name} ({len(t)} chars)")
