"""Session 37 — oembed-verify YouTube candidates; TPB torrent check; fetch slowcult reunion article."""
import html
import json
import re
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

# (video_id, note)
CANDIDATES = [
    ("5oYF6moscbI", "Tungsteno VEVO"),
    ("IzgpAi_KB9A", "L'Equilibrio VEVO"),
    ("hx8yMhNKVVE", "L'Innocenza VEVO"),
    ("jAxUB0-KIhc", "Armstrong Topic"),
    ("NUz3yYhLzzo", "Simmetrie Topic"),
    ("F2flbWGDmj0", "Giuseppe Pierri Topic"),
    ("HjEJgPRDJ94", "L'Amour Topic"),
    ("UVdi9eiPRDk", "Jetsons High Speed Topic"),
    ("o_kP0p2hMS0", "L'Universo Topic"),
    ("ws9FcwnI1FE", "Centro Topic"),
    ("5pdSkLB0PNE", "Rosemary Plexiglas Topic"),
    ("GBmpb7UARN8", "Completo Topic"),
    ("P-tEfothiI8", "Svecchiamento Topic"),
    ("TC1sf0JIgoE", "84 Topic"),
    ("YhIspqotyeg", "Il Muro 1997 Tape Trading"),
    ("beV4n3s5NfE", "Live TV RP+Centro HD"),
    ("-C2ZZ8ux6hw", "Live TV Videoginnastica+Golf HD"),
    ("v-mYrhMiLdc", "Rosemary Plexiglas/Centro Capitolocinque"),
    ("NzqDV0lJJcY", "troppo poco intelligente il vicolo MPG"),
    ("yIhqDYkP2Yw", "centro il vicolo MPG"),
    ("ZS6bHVgE-jE", "Show Case parte 1"),
    ("l2_-ohac470", "Rave on Benvegnu Scisma Huyghens"),
    ("ZJWoUvWClQA", "L'equilibrio Mengo tribute"),
    ("xjy--ZQeuaw", "I'm the Ocean Mengo Huyghens"),
    ("Z9fGhkE9Y14", "Rosemary Plexiglas Mengo Fest"),
    ("zpL969rHW0Y", "Simmetrie Mengo Anna Benvegnu"),
    ("Za2AeaZW_Fw", "Simmetrie Arezzo 2025"),
    ("yv7x0mdxMT8", "Suggestionabili Torino L'innocenza"),
    ("iCgN6RxSZxU", "L'innocenza Monk Roma 2015"),
    ("j9S9Qb6NZbg", "Tungsteno Locomotiv 2015"),
    ("IO1dApDWz9w", "centro Locomotiv 2015"),
    ("oKC1Wxg8Yes", "simmetrie Locomotiv 2015"),
    ("v9U7_xmp0hc", "Tungsteno album version"),
    ("pGuxUW6tkB4", "Tungsteno Sigma Tibet Remix 12in"),
    ("uskAFo13S2k", "Cavallo Bianco Ruggiero feat Scisma"),
    ("d3sUO0PkOT4", "Azioni Meccaniche Soniche Avventure"),
    ("rADG7FLajwo", "L'equilibrio 1998 Lostwave"),
    ("tTO7AswC_YA", "In dissolvenza Davide Ruggerini"),
    ("Qp0Oyh3t2zo", "Armstrong Vinacea"),
    ("7j378R4ZGgA", "Rosemary Plexiglas laura palmer"),
]

print("=== OEMBED VERIFICATION ===")
alive = []
dead = []
for vid, note in CANDIDATES:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    try:
        req = urllib.request.Request(url, headers=UA)
        d = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
        print(f"OK   {vid} | {d.get('title')[:70]} | {d.get('author_name')[:35]}")
        alive.append((vid, d.get("title"), d.get("author_name"), note))
    except Exception as e:
        print(f"DEAD {vid} | {note} | {e}")
        dead.append(vid)

print(f"\nAlive: {len(alive)} / {len(CANDIDATES)}")
with open("/home/ubuntu/.hermes/profiles/amanda/cache/scratch/s37/oembed_alive.json", "w") as f:
    json.dump(alive, f, ensure_ascii=False, indent=1)

# TPB check
print("\n=== THE PIRATE BAY (tpb.party) ===")
for q in ["scisma", "rosemary plexiglas", "armstrong scisma"]:
    try:
        u = "https://tpb.party/search/" + urllib.parse.quote(q) + "/1/99/0"
        req = urllib.request.Request(u, headers=UA)
        raw = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
        rows = re.findall(r'<a href="/torrent/(\d+)/[^"]*" class="detLink"[^>]*>([^<]+)</a>', raw)
        print(f"-- {q}: {len(rows)} results")
        for tid, title in rows[:10]:
            print("   ", tid, title[:80])
    except Exception as e:
        print(f"-- {q} FAILED: {e}")

# slowcult reunion article
print("\n=== SLOWCULT REUNION ARTICLE ===")
try:
    u = "https://www.slowcult.com/musica-2/musica/il-ritorno-della-magia-degli-scisma"
    req = urllib.request.Request(u, headers=UA)
    raw = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
    t = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    # find the Scisma-relevant part
    m = re.search(r"(Quando salgono sul palco.{0,2500})", t, re.S)
    print((m.group(1) if m else t[:2000])[:2200])
except Exception as e:
    print("FAILED:", e)
