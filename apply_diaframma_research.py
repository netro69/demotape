# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python3
"""
Diaframma research update script for Demotape.
Run: cd ~/Projects/demotape && source .venv/bin/activate && python manage.py shell < apply_diaframma_research.py
"""

import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, GenreTag, Label

print("=" * 60)
print("APPLYING DIAFRAMMA RESEARCH")
print("=" * 60)

# Get Diaframma
diaframma = Band.objects.get(slug='diaframma')
print(f"\nTarget: Diaframma (id={diaframma.id})")

# Update band info
old_bio = diaframma.bio
new_bio = "Italian dark wave / new wave / gothic rock band from Florence. Formed late 1970s/early 1980s. One of the most iconic Italian new wave acts alongside Litfiba, Pankow, and Neon. Still active today led by Federico Fiumani."

if old_bio == new_bio:
    print("Bio unchanged, skipping")
else:
    diaframma.bio = new_bio
    diaframma.city = "Florence"
    diaframma.active_years = "1979-present"
    diaframma.status = "published"
    diaframma.save()
    print(f"Updated band info: city={diaframma.city}, years={diaframma.active_years}")

# Add genre tags
genre_names = ['new-wave', 'dark-wave', 'gothic-rock', 'post-punk', 'alternative-rock', 'punk-rock']
for gn in genre_names:
    try:
        g = GenreTag.objects.get(slug=gn)
        diaframma.genre_tags.add(g)
        print(f"Added genre: {g.name}")
    except GenreTag.DoesNotExist:
        g = GenreTag.objects.create(name=gn.replace('-', ' ').title(), slug=gn)
        diaframma.genre_tags.add(g)
        print(f"Created and added genre: {g.name}")

# Add Links
links_data = [
    ('website', 'Official Website', 'https://www.diaframma.org/', True, 'Official Diaframma website - discography, news, tour dates'),
    ('archive', 'Wikipedia (EN)', 'https://en.wikipedia.org/wiki/Diaframma', False, 'English Wikipedia page with full discography and history'),
    ('archive', 'Wikipedia (IT)', 'https://it.wikipedia.org/wiki/Diaframma_(gruppo_musicale)', False, 'Italian Wikipedia page (more detailed)'),
    ('archive', 'Discogs', 'https://www.discogs.com/artist/493560-Diaframma', False, 'Complete discography with releases and credits'),
    ('archive', 'RateYourMusic', 'https://rateyourmusic.com/artist/diaframma', False, 'User reviews and release ratings'),
    ('archive', 'MusicBrainz', 'https://musicbrainz.org/artist/d3f9254c-08fe-4aa6-b601-8dd43dd1ba19/releases', False, 'Structured release metadata'),
    ('archive', 'OndaRock Interview', 'https://www.ondarock.it/interviste/diaframma/', False, 'Interview with Federico Fiumani by Claudio Lancia'),
    ('video', 'Siberia (Official Video)', 'https://www.youtube.com/watch?v=JtTHAtuootA', False, 'Official video for Siberia (1984), remastered HD'),
    ('video', 'Siberia (Track)', 'https://www.youtube.com/watch?v=vF-cH9Lms8I', False, 'Full album version of Siberia'),
    ('video', 'Circuito Chiuso', 'https://www.youtube.com/watch?v=m4C1H9cF5U4', False, 'Circuito Chiuso - 1982 split 7" with Pankow'),
    ('video', 'Gennaio live 1991', 'https://www.youtube.com/watch?v=k-M31wfcoWE', False, 'Live performance in Florence, 1991'),
    ('streaming', 'Bandcamp - Demo 1981', 'https://diaframmade.bandcamp.com/album/demo-1981', False, 'Raw 1981 demo - coldwave/new wave/post-punk'),
    ('streaming', 'Bandcamp - Sesso e Violenza', 'https://diaframmalr.bandcamp.com/album/sesso-e-violenza', False, '1996 album streaming'),
    ('streaming', 'Spotify', 'https://open.spotify.com/artist/4RbZ9lwnXlWzm0G9UZ8NEX', False, 'Diaframma on Spotify'),
    ('streaming', 'Apple Music', 'https://music.apple.com/lr/artist/diaframma/271853867', False, 'Diaframma on Apple Music'),
    ('archive', 'DeBaser - Boxe review', 'https://www.debaser.it/diaframma/boxe', False, 'Review of Boxe album on DeBaser'),
    ('archive', 'Heart of Glass - Siberia review', 'https://heartofglass.altervista.org/blog/siberia-diaframma/', False, 'Detailed review of Siberia album'),
    ('archive', 'Vice Italia - Federico Fiumani interview', 'https://www.vice.com/it/article/federico-fiumani-diaframma-intervista/', False, 'In-depth interview with Fiumani'),
    ('archive', 'Rolling Stone Italia - Normalità di una rockstar', 'https://www.rollingstone.it/musica/live/federico-fiumani-normalita-di-una-rockstar/443876/', False, 'Rolling Stone profile'),
    ('archive', 'Controradio - Live at Flog', 'https://www.controradio.it/diaframma-in-concerto-alla-flog-di-firenze/', False, 'Concert announcement and info'),
    ('archive', 'Metrodora - Pearls of post punk vol.96', 'https://www.metrodora.net/pearls-of-post-punk-vol-96-pankow/', False, 'Split 7" review with Pankow'),
    ('archive', 'Contempo Records - Altrove', 'https://contemporecords.it/prodotto/diaframma-altrove-lp-7-edizione-limitata-400-copie/', False, 'Altrove MLP limited edition (400 copies)'),
    ('archive', 'Relics Controsuoni - Live photos', 'https://www.relics-controsuoni.com/2013/03/diaframma-live-blackout-rock-club-testo-e-foto-di-simone-giuliani.html', False, 'Live photos and text by ex-keyboardist Simone Giuliani'),
    ('archive', 'Florentine scene article', 'https://www.firenzetoday.it/eventi/florence-calling-talk-litfiba-diaframma-scena-wave-firenze-2026.html', False, 'Florence wave scene talk covering Diaframma, Litfiba, Pankow'),
    ('archive', 'Koinervetti - LAbisso review', 'https://www.koinervetti.com/labisso-dei-diaframma-ovvero-florence-calling/', False, 'Review of LAbisso album'),
    ('archive', 'WIP Radio Interview', 'https://www.wipradio.it/2017/11/03/intervista-ai-diaframma/', False, 'Interview about Florentine scene history'),
    ('archive', 'Paese Sera article', 'https://www.paesesera.toscana.it/diaframma-gratis-al-riff-club/', False, 'Early 1980s scene article mentioning Diaframma, Neon, Pankow, Litfiba'),
    ('archive', 'Il Fatto Quotidiano - Niente di serio', 'https://www.ilfattoquotidiano.it/2012/01/17/niente-serio-esce-oggi-nuovo-discodei-diaframma-federico-fiumani/184372/', False, 'Album review'),
    ('archive', 'CSi Magazine Interview', 'https://www.csimagazine.it/intervista-a-federico-fiumani/', False, 'Interview with Fiumani'),
    ('archive', 'NTS Radio', 'https://www.nts.live/artists/52495-diaframma', False, 'NTS radio plays Diaframma tracks'),
]

links_added = 0
for link_type, title, url, is_primary, description in links_data:
    link, created = Link.objects.get_or_create(
        band=diaframma,
        url=url,
        defaults={
            'link_type': link_type,
            'title': title,
            'is_primary': is_primary,
            'description': description
        }
    )
    if created:
        links_added += 1
        print(f"  + Link: {title}")
    else:
        print(f"  = Already exists: {title}")

print(f"\nLinks added: {links_added}")

# Add Connections to other bands in Demotape database
connections_data = [
    ('Litfiba', 'scene_peer', 'Both from Florence new wave scene, shared members, split 7" Amsterdam (1985)', 'https://en.wikipedia.org/wiki/Litfiba'),
    ('Pankow', 'collaboration', 'Split 7" Circuito Chiuso/Wither (1982), Industrie Discografiche Lacerba, only 500 copies', 'https://www.discogs.com/artist/21893-Pankow'),
    ('RockGalileo', 'scene_peer', 'Florence scene peer', ''),
    ('Biagio Antonacci', 'scene_peer', 'Italian scene connection', ''),
    ('Piero Pelù', 'collaboration', 'Piero Pelù (Litfiba frontman) collaborated with Fiumani', 'https://www.rollingstone.it/musica/storie-musica/i-litfiba-i-diaframma-e-i-giorni-delli-r-a/963532/'),
]

connections_added = 0
for band_name, conn_type, notes, source in connections_data:
    try:
        other_band = Band.objects.get(name=band_name)
        conn, created = BandConnection.objects.get_or_create(
            from_band=diaframma,
            to_band=other_band,
            connection_type=conn_type,
            defaults={
                'notes': notes,
                'source': source
            }
        )
        if created:
            connections_added += 1
            print(f"  + Connection: Diaframma -> {band_name} ({conn_type})")
        else:
            print(f"  = Already exists: Diaframma -> {band_name} ({conn_type})")
    except Band.DoesNotExist:
        print(f"  ! Band not found: {band_name}")

print(f"\nConnections added: {connections_added}")

# Summary
print("\n" + "=" * 60)
print("DIAFRAMMA RESEARCH UPDATE COMPLETE")
print("=" * 60)
print(f"Band: Diaframma (id={diaframma.id})")
print(f"City: Florence")
print(f"Active: 1979-present")
print(f"Genres: {', '.join(g.name for g in diaframma.genre_tags.all())}")
print(f"Total links for Diaframma: {Link.objects.filter(band=diaframma).count()}")
print(f"Total connections for Diaframma: {BandConnection.objects.filter(from_band=diaframma).count() + BandConnection.objects.filter(to_band=diaframma).count()}")
print(f"\nConnections:")
for c in BandConnection.objects.filter(from_band=diaframma):
    print(f"  -> {c.to_band.name} ({c.connection_type})")
for c in BandConnection.objects.filter(to_band=diaframma):
    print(f"  <- {c.from_band.name} ({c.connection_type})")
