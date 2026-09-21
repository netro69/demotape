import os
import sys

os.chdir('/home/ubuntu/Projects/demotape')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')

import django
django.setup()

from apps.core.models import Band, Release, Link

# Get Plastik band
plastik = Band.objects.filter(slug='plastik').first()
if not plastik:
    print("Plastik not found!")
    sys.exit(1)

print(f"=== Adding links to {plastik.name} ===")

# New links to add based on research
new_links = [
    # Side of Mine CD reissue on Bandcamp
    {
        'link_type': 'streaming',
        'title': 'Mind Drop - Side of Mine (Bandcamp reissue)',
        'url': 'https://energeia.bandcamp.com/album/side-of-mine-ene034',
        'description': 'Original 1996 CD reissued on Bandcamp. MP3/FLAC downloads available. Energeia label archive release.',
    },
    # Discogs for Mind Drop
    {
        'link_type': 'archive',
        'title': 'Mind Drop (2) - Discogs discography',
        'url': 'https://www.discogs.com/artist/1064060-Mind-Drop-2',
        'description': 'Full discography including demotapes "Lurking Fear" (1991) and "Rusted Eternity" (1993), CD "Side of Mine" (1996). Later changed name to Plastik.',
    },
    # Discogs for Andrea Manenti
    {
        'link_type': 'archive',
        'title': 'Andrea Manenti - Discogs',
        'url': 'https://www.discogs.com/artist/5189599-Andrea-Manenti',
        'description': 'Singer and multi-instrumentalist from Varese. Groups: Downlouders, Mind Drop, Plastik.',
    },
    # RateYourMusic
    {
        'link_type': 'archive',
        'title': 'Mind Drop - RateYourMusic',
        'url': 'https://rateyourmusic.com/artist/mind-drop-1',
        'description': 'Gothic Rock band from Varese. Albums: Side of Mine, Intimations of Immortality - Energeia Sampler Vol. 1, Rusted Eternity.',
    },
    # YouTube full album
    {
        'link_type': 'video',
        'title': 'Mind Drop - Side Of Mine (Full Album) [YouTube]',
        'url': 'https://www.youtube.com/watch?v=LoxMiZZT_s4',
        'description': 'Full album rip of the 1996 CD "Side of Mine". Italian gothic rock/darkwave.',
    },
    # Italian news article about 30th anniversary concert
    {
        'link_type': 'archive',
        'title': 'TuMiTurbi a tinte dark - 30 anni di Rusted Eternity',
        'url': 'https://www.malpensa24.it/tumiturbi-a-tinte-dark-mind-drop-in-concerto-per-i-30-anni-di-rusted-eternity/',
        'description': 'Italian article about Mind Drop reunion concert for 30th anniversary of "Rusted Eternity" demotape. Contains band history: born late 80s, played at Linus Club and Shelter Club in Varese, Hysterika in Milan, Muro in Varese.',
    },
    # Last.fm for Rusted Eternity
    {
        'link_type': 'streaming',
        'title': 'Mind Drop - Rusted Eternity (Last.fm)',
        'url': 'https://www.last.fm/music/Mind+Drop/Rusted+Eternity',
        'description': 'Demotape from 1993. 8 tracks including Mind Drop, Wake Up, Lurking Fear, Hurricane, Human Aggression.',
    },
    # Last.fm for Mind Drop overall
    {
        'link_type': 'streaming',
        'title': 'Mind Drop - Last.fm profile',
        'url': 'https://www.last.fm/music/Mind+Drop',
        'description': 'Last.fm page for Mind Drop. Demotapes "Lurking Fear" (1991) and "Rusted Eternity" (1993), CD "Side of Mine" (1996).',
    },
    # Spinn Radio bio
    {
        'link_type': 'archive',
        'title': 'Mind Drop - Spinn Radio bio',
        'url': 'https://spinnradio.com/artist/mind-drop',
        'description': 'Bio: Gothic rock band founded 1990 in Varese, Italy. Released demotapes "Lurking Fear" (1991) and "Rusted Eternity" (1993), CD "Side of Mine" (1996). Later changed name to Plastik.',
    },
]

added = 0
skipped = 0
for link_data in new_links:
    existing = Link.objects.filter(band=plastik, url=link_data['url']).exists()
    if existing:
        print(f"  SKIP (exists): {link_data['title']}")
        skipped += 1
    else:
        link = Link.objects.create(
            band=plastik,
            link_type=link_data['link_type'],
            title=link_data['title'],
            url=link_data['url'],
            description=link_data['description'],
        )
        print(f"  ADDED: {link.title}")
        added += 1

print(f"\n--- Summary ---")
print(f"Added: {added}")
print(f"Skipped: {skipped}")
print(f"Total links for Plastik now: {plastik.links.count()}")

# Also add Rock Rose info if exists
rock_rose = Band.objects.filter(slug='rock-rose').first()
if rock_rose:
    print(f"\n=== Rock Rose (Rome, 1986-1988) ===")
    print(f"Links: {rock_rose.links.count()}")
    print(f"Releases: {rock_rose.releases.count()}")
    print(f"Bio: {rock_rose.bio[:200]}")
