#!/usr/bin/env python
"""Update database with CCCP Fedeli alla linea findings."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link

# Get CCCP
try:
    cccp = Band.objects.get(name='CCCP Fedeli alla linea')
except Band.DoesNotExist:
    print("ERROR: CCCP Fedeli alla linea not found!")
    sys.exit(1)

print(f"Found: {cccp.name} (ID={cccp.id})")
print(f"Current links: {cccp.links.count()}")

# Define new links to add
new_links = [
    # RuTracker (torrent trackers)
    ('archive', 'RuTracker - Full 9CD Discography MP3 320kbps', 'https://rutracker.org/forum/viewtopic.php?t=5247651'),
    ('archive', 'RuTracker - 1964/1985 Affinità-Divergenze FLAC', 'https://rutracker.org/forum/viewtopic.php?t=4493660'),
    ('archive', 'RuTracker - Canzoni Preghiere Danze FLAC', 'https://rutracker.org/forum/viewtopic.php?t=5256826'),
    ('archive', 'RuTracker - Felicitazioni! 2023 FLAC 24-44', 'https://1337x.to/torrent/5844971/CCCP-Fedeli-Alla-Linea-Felicitazioni-2023-Punk-New-wave-Flac-24-44/'),
    
    # Video (YouTube)
    ('video', 'YouTube - CCCP Fedeli alla linea Playlist', 'https://www.youtube.com/playlist?list=PLOqEiUpWrNuDAiQzbS3D_jIXUwLIuI01Z'),
    ('video', 'YouTube - Official Channel', 'https://www.youtube.com/@CCCP_FedeliAllaLinea'),
    ('video', 'YouTube - 1983 Radio Interview (Radio Antenna Uno Modena)', 'https://www.youtube.com/watch?v=DnOWSWO4JAY'),
    ('video', 'YouTube - Punk Islam Live UfaFabrik Berlin 1985', 'https://www.instagram.com/reel/DbvSC_IiV1V0/'),
    
    # Streaming
    ('streaming', 'YouTube Music', 'https://music.youtube.com/channel/UCIVbMt-453YISrfwps6Th0Q'),
    ('streaming', 'Boomplay', 'https://www.boomplay.com/artists/1939811'),
    ('streaming', 'Deezer', 'https://www.deezer.com/en/artist/1502038'),
    ('streaming', 'Apple Music', 'https://music.apple.com/us/artist/cccp-fedeli-alla-linea/201355565'),
    ('streaming', 'ISRABOX (Felicitazioni! Live)', 'https://www.israbox-music.com/artist/CCCP+-+Fedeli+Alla+Linea/'),
    
    # Archive (Discogs)
    ('archive', 'Discogs - Artist Page', 'https://www.discogs.com/artist/256245-CCCP-Fedeli-Alla-Linea'),
    ('archive', 'Discogs - 1984 Cassette Promo', 'https://www.discogs.com/de/release/12866958-CCCP-Fedeli-Alla-Linea-CCCP-Fedeli-Alla-Linea'),
    ('archive', 'Discogs - Socialismo E Barbarie LP', 'https://www.discogs.com/release/1212511-CCCP-Fedeli-Alla-Linea-Socialismo-E-Barbarie'),
    ('archive', 'Discogs - Compagni Cittadini Fratelli Partigiani', 'https://www.discogs.com/master/196384-CCCP-Fedeli-Alla-Linea-Compagni-Cittadini-Fratelli-PartigianiOrtodossia-II'),
    ('archive', 'Discogs - R.I.N.G.E.R.? Compilation', 'https://www.discogs.com/release/7035881-Various-RINGER-HardnHeavy-Compilation'),
    
    # Archive (Wikipedia/Wikidata)
    ('archive', 'Wikipedia EN', 'https://en.wikipedia.org/wiki/CCCP_-_Fedeli_alla_linea'),
    ('archive', 'Wikipedia IT', 'https://it.wikipedia.org/wiki/CCCP_-_Fedeli_alla_linea'),
    ('archive', 'Wikipedia - Giovanni Lindo Ferretti', 'https://it.wikipedia.org/wiki/Giovanni_Lindo_Ferretti'),
    ('archive', 'Wikipedia - Helena Velena', 'https://it.wikipedia.org/wiki/Helena_Velena'),
    ('archive', 'Wikipedia - Massimo Zamboni', 'https://it.wikipedia.org/wiki/Massimo_Zamboni'),
    ('archive', 'Wikidata', 'https://www.wikidata.org/wiki/Q1022705'),
    
    # Archive (Reviews and articles)
    ('archive', 'OndaRock - Affinità-Divergenze Review', 'https://www.ondarock.it/recensioni/pietremiliariitaliane/cccp_affinita/'),
    ('archive', 'DeBaser - Ortodossia II Review', 'https://en.debaser.it/cccp-fedeli-alla-linea/ortodossia-ii-compagni-cittadini-fratelli-partigiani/recensione'),
    ('archive', 'DeBaser - Affinità-Divergenze Review', 'https://www.metallized.it/recensione.php?id=15464'),
    ('archive', 'Rolling Stone Italia', 'https://www.rollingstone.it/artista/cccp/'),
    ('archive', 'Il Cibicida - Monograph', 'https://www.ilcibicida.com/monografie/cccp-fedeli-alla-linea/'),
    ('archive', 'DOKUMEN.PUB - Affinità-Divergenze Book', 'https://dokumen.pub/cccp-fedeli-alla-lineas-affinita-divergenze-fra-il-compagno-togliatti-e-noi.html'),
    ('archive', 'Academia.edu - Catalogo 1985 PDF', 'https://www.academia.edu/81678829/CCCP_Fedeli_alla_Linea_Catalogo_1985_'),
    ('archive', 'Genius Lyrics', 'https://genius.com/albums/Cccp-fedeli-alla-linea/1964-1985-affinita-divergenze-fra-il-compagno-togliatti-e-noi-del-conseguimento-della-maggiore-eta'),
    ('archive', 'RateYourMusic', 'https://rateyourmusic.com/artist/cccp-fedeli-alla-linea'),
    ('archive', 'Last.fm', 'https://www.last.fm/music/CCCP+–+Fedeli+Alla+Linea'),
    ('archive', 'Spirit of Rock', 'https://www.spirit-of-rock.com/de/discography/CCCP_Fedeli_Alla_Linea/1'),
    ('archive', 'Electrocity.it', 'https://www.electrocity.it/Discografie/pankow.htm'),
    ('archive', 'Radio Molotov - Ortodossia 1984', 'https://radiomolotov.blogspot.com/2013/05/cccp-fedeli-alla-linea-ortodossia-7.html'),
    ('archive', 'Kill Your Pet Puppy', 'https://killyourpetpuppy.co.uk/news/cccp-fedeli-alla-linea-attack-punk-records-1984/'),
    ('archive', 'OpenEdition - Academic Article', 'https://journals.openedition.org/rccs/6215'),
    ('archive', 'This Is My Jam', 'https://web.archive.org/web/20210531075230/https://www.thisismyjam.com/song/io-sto-bene/cccp-fedeli-alla-linea'),
    ('archive', 'Google Groups - free.it.enkey', 'https://groups.google.com/g/free.it.enkey/c/YuSk-bqCM-M'),
]

# Add links
added = 0
for link_type, title, url in new_links:
    link, created = Link.objects.get_or_create(
        band=cccp,
        url=url,
        defaults={'link_type': link_type, 'title': title}
    )
    if created:
        added += 1
        print(f"  + [{link_type}] {title[:40]}")
    else:
        print(f"  = [{link_type}] {title[:40]} (already exists)")

print(f"\n{'='*60}")
print(f"Added {added} new links to {cccp.name}")
print(f"Total links now: {cccp.links.count()}")
print(f"Done!")
