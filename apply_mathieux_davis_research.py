#!/usr/bin/env python3
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()
from apps.core.models import Band, Link, BandConnection, GenreTag

b = Band.objects.get(id=122)
b.bio = "Mathieux Davis (born December 15, 1997) is an American drummer, social media influencer, and biomedical engineer based in Flowery Branch/Atlanta, Georgia. Not a traditional band but a solo artist/session drummer. Rose to fame via viral 'church metal drummer' skits and drum covers on social media (2017-present, accelerated during COVID-19). Fuses gospel music with metal/hard rock. Currently drums for NZ metal artist Vana (toured internationally, opened for Linkin Park in NZ March 2025). Has performed with country artist Reyna Roberts. Endorsements: Ludwig Drums, Zildjian Cymbals, Vic Firth, Conn Selmer. Biomedical Engineering B.S. from Mississippi State University."
b.active_years = "2017-present"
b.save()

for slug in ["metal", "hard-rock", "gospel"]:
    g = GenreTag.objects.filter(slug=slug).first() or GenreTag.objects.filter(name__iexact=slug.replace('-',' ')).first()
    if g: b.genre_tags.add(g)

links = [
    ("website","Mathieux Davis Studios","https://www.mathieuxdavisstudios.com/","Official website"),
    ("social","TikTok @mathieux_davis","https://www.tiktok.com/@mathieux_davis","469.2K followers, 10.8M likes"),
    ("social","Instagram @mathieux_davis","https://www.instagram.com/mathieux_davis/","382K followers"),
    ("social","Facebook","https://www.facebook.com/mathieuxdavisdrums/","104K likes"),
    ("social","YouTube @mathieux_davis","https://www.youtube.com/@mathieux_davis","YouTube channel"),
    ("streaming","Spotify","https://open.spotify.com/artist/73VQ36keyyyedS3WI3eTGP","~39.6K monthly listeners"),
    ("streaming","Apple Music","https://music.apple.com/us/artist/mathieux-davis/1486694694","Artist profile"),
    ("streaming","Deezer","https://www.deezer.com/en/artist/78055472","Artist page"),
    ("linktree","Linktree","https://linktr.ee/Mathieux_davis","All links"),
    ("social","Threads @mathieux_davis","https://www.threads.com/@mathieux_davis","Atlanta, Ludwig Artist, Biomed Engineer"),
    ("social","LinkedIn","https://www.linkedin.com/in/mathieux-davis-b542ab196","Mississippi State, Omnicell"),
]
for lt,title,url,desc in links:
    if not b.links.filter(url=url).first():
        Link.objects.create(band=b, link_type=lt, title=title, url=url, description=desc)

conn_targets = ["Vana","Linkin Park","Reyna Roberts","Mack Lorén"]
for name in conn_targets:
    try:
        t = Band.objects.get(name=name)
        if not BandConnection.objects.filter(from_band=b, to_band=t).first():
            BandConnection.objects.create(from_band=b, to_band=t, connection_type="associated", notes=f"Connection via research")
    except Band.DoesNotExist:
        print(f"  Target not in DB: {name}")

b.refresh_from_db()
print(f"Mathieux Davis (122): {b.links.count()} links, {b.connections_from.count()} conns")
