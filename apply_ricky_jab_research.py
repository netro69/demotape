#!/usr/bin/env python3
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()
from apps.core.models import Band, Link, BandConnection, GenreTag

b = Band.objects.get(id=121)
b.bio = "Ricky Jabarin (stage name: Ricky Jab / RickyJab) is an American guitarist, producer, and content creator based in Philadelphia, Pennsylvania. Known on TikTok for making pop-punk and metal remixes from viral TikToks. 1/2 of post-hardcore duo Unsafe, Unsound (with Tyler Morris/Westend). Touring guitarist for Taylor Acorn (2024-2026). PRS Guitars Official Artist, Ernie Ball endorsed. Education: Penn State University (Supply Chain & Information Systems). Career catalyzed by COVID-19 lockdowns (March 2020)."
b.active_years = "2020-present"
b.save()

for slug in ["pop-punk", "post-hardcore", "alternative-rock", "metal", "emo"]:
    g = GenreTag.objects.filter(slug=slug).first() or GenreTag.objects.filter(name__iexact=slug.replace('-',' ')).first()
    if g: b.genre_tags.add(g)

links = [
    ("social","Instagram @rickyjab","https://www.instagram.com/rickyjab/","11K followers, guitarist/producer"),
    ("social","TikTok @rickyjab","https://www.tiktok.com/@rickyjab","Primary platform; pop-punk/metal content"),
    ("social","Threads @rickyjab","https://www.threads.com/@rickyjab","1.7K followers"),
    ("social","Facebook RickyJab","https://www.facebook.com/rickyjabmusic/","889 likes"),
    ("social","LinkedIn Ricky Jabarin","https://www.linkedin.com/in/rickyjab","Penn State, Philadelphia"),
    ("streaming","Apple Music (solo)","https://music.apple.com/us/artist/rickyjab/1169772710","6+ tracks"),
    ("streaming","Shazam (solo)","https://www.shazam.com/artist/ricky-jab/1634799449","Active"),
    ("streaming","Spotify (Unsafe Unsound)","https://open.spotify.com/artist/1JNcqU8eMwSIIgSn62UJqi","108K monthly listeners"),
    ("streaming","Apple Music (Unsafe Unsound)","https://music.apple.com/us/artist/unsafe-unsound/1591822435","Active"),
    ("streaming","Genius (solo)","https://genius.com/artists/Ricky-jab/songs","6 songs cataloged"),
    ("website","Unsafe Unsound","https://unsafeunsound.com/","Merch store"),
    ("social","Unsafe Unsound TikTok","https://www.tiktok.com/@unsafeunsound","67K followers, 623K likes"),
    ("social","Unsafe Unsound Twitter/X","https://twitter.com/unsafeunsound","Active"),
    ("linktree","SoundBetter","https://soundbetter.com/profiles/379019-rickyjab","Session work/production"),
    ("article","All The Things Music Interview","https://www.allthethings-music.com/post/exclusive-interview-rickyjab-on-touring-with-taylor-acorn-forming-unsafe-unsound-and-building-a","June 2026"),
    ("article","Mullins Over Music EP76","https://www.youtube.com/watch?v=0dSJOZBxIsc","Podcast interview"),
    ("article","Hughesley Show Interview","https://podcasts.apple.com/ru/podcast/ricky-jab/id1580288807?i=1000546397427","Dec 2021, 46 min"),
]
for lt,title,url,desc in links:
    if not b.links.filter(url=url).first():
        Link.objects.create(band=b, link_type=lt, title=title, url=url, description=desc)

conn_targets = ["Taylor Acorn","David Michael Frank","Mathieux Davis","Future Sunsets","Anji Kaizen"]
for name in conn_targets:
    try:
        t = Band.objects.get(name=name)
        if not BandConnection.objects.filter(from_band=b, to_band=t).first():
            BandConnection.objects.create(from_band=b, to_band=t, connection_type="associated", notes=f"Connection via research")
    except Band.DoesNotExist:
        print(f"  Target not in DB: {name}")

b.refresh_from_db()
print(f"Ricky Jab (121): {b.links.count()} links, {b.connections_from.count()} conns")
