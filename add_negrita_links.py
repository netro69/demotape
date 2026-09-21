import os
import sys

os.chdir('/home/ubuntu/Projects/demotape')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')

import django
django.setup()

from apps.core.models import Band, Release, Link, Fanzine, FanzineReview

# Get Negrita band
negrita = Band.objects.filter(slug='negrita').first()
if not negrita:
    negrita = Band.objects.filter(name__icontains='negrita').first()

if not negrita:
    print("Negrita not found!")
    sys.exit(1)

print(f"=== Adding links to {negrita.name} ===")

# New links to add based on research
new_links = [
    # Italian Wikipedia - has more detailed history
    {
        'link_type': 'archive',
        'title': 'Negrita — Wikipedia IT (detailed history)',
        'url': 'https://it.wikipedia.org/wiki/Negrita',
        'description': 'Detailed Italian Wikipedia article covering formation at Marcena (Arezzo fraction), early demos 1992, discovery by producer Fabrizio Barbacci, first album Negrita (1994) with "Cambio", Paradisi per illusi (1995), XXX (1997, recorded in USA, platinum), Reset (1999), collaborations with Aldo Giovanni e Giacomo, and complete discography.',
    },
    # Negrita first album Wikipedia
    {
        'link_type': 'archive',
        'title': 'Negrita (album 1994) — Wikipedia IT',
        'url': 'https://it.wikipedia.org/wiki/Negrita_(album)',
        'description': 'First album recorded August 1993 at IRA Studio (Firenze) — same studio used by Litfiba, Ritmo Tribale, Extrema. All songs composed by Pau, Cesare, Drigo + Fabrizio Barbacci. Features "Peace Frog" cover.',
    },
    # Negrita official bio
    {
        'link_type': 'website',
        'title': 'Negrita — Official Biography',
        'url': 'https://www.negrita.com/bio/',
        'description': 'Official biography covering formation in Marcena (province of Arezzo), rare friendship and passion, one of the most influential and unclassifiable Italian rock groups. Loyal to Arezzo province.',
    },
    # RuTracker discography
    {
        'link_type': 'archive',
        'title': 'Negrita — Complete Discography (RuTracker)',
        'url': 'https://rutracker.org/forum/viewtopic.php?t=5631344',
        'description': 'Complete discography collection on RuTracker. Includes: Negrita (1994), Paradisi per illusi (1995), XXX (1997), Reset (1999), HELLdorado (2008), Canzoni per anni spietati (2025). Formed 1991, several successful demos before first album.',
    },
    # YouTube - official music video "Cambio"
    {
        'link_type': 'video',
        'title': 'Negrita — Cambio (Official Music Video, 1994)',
        'url': 'https://www.youtube.com/watch?v=Cw3u04Co-S0',
        'description': 'Official music video for "Cambio" — lead single from the debut album Negrita (1994). The song that launched the band.',
    },
    # YouTube - "Mama maé" from Reset (1999)
    {
        'link_type': 'video',
        'title': 'Negrita — Mama maé (Reset, 1999)',
        'url': 'https://www.youtube.com/watch?v=sqfheaUBW48',
        'description': '"Mama maé" from the album Reset (1999). Shows the band\'s harder rock direction.',
    },
    # Setlist.fm
    {
        'link_type': 'archive',
        'title': 'Negrita — Concert Setlists (setlist.fm)',
        'url': 'https://www.setlist.fm/setlists/negrita-23d6884b.html',
        'description': 'Complete concert setlists from 1990s to present. Includes "Canzoni per anni spietati tour in teatro" at Teatro Petrarca, Arezzo.',
    },
    # Apple Music
    {
        'link_type': 'streaming',
        'title': 'Negrita — Apple Music',
        'url': 'https://music.apple.com/by/artist/negrita/13432043',
        'description': 'Full catalog on Apple Music including remastered editions. Paradisi Per Illusi (Remastered 2020).',
    },
    # MusicHearts bio
    {
        'link_type': 'archive',
        'title': 'Negrita — MusicHearts Bio',
        'url': 'https://ru.musichearts.fm/en/artists/249-negrita',
        'description': 'Band profile: Italian rock band formed early 90s in Arezzo. Named after Rolling Stones\' "Hey Negrita". 130+ ratings.',
    },
    # Last.fm
    {
        'link_type': 'streaming',
        'title': 'Negrita — Last.fm',
        'url': 'https://www.last.fm/music/Negrita',
        'description': 'Last.fm page with listener stats, similar artists, and biography.',
    },
    # RateYourMusic
    {
        'link_type': 'archive',
        'title': 'Negrita — RateYourMusic',
        'url': 'https://rateyourmusic.com/artist/negrita',
        'description': 'Community ratings and discography on RateYourMusic.',
    },
    # Negrita discography page
    {
        'link_type': 'archive',
        'title': 'Negrita — Official Discography Page',
        'url': 'https://www.negrita.com/disco/',
        'description': 'Official discography page with all releases from 1994 to present.',
    },
]

added = 0
skipped = 0
for link_data in new_links:
    existing = Link.objects.filter(band=negrita, url=link_data['url']).exists()
    if existing:
        print(f"  SKIP (exists): {link_data['title']}")
        skipped += 1
    else:
        link = Link.objects.create(
            band=negrita,
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
print(f"Total links for Negrita now: {negrita.links.count()}")

# Now update the Negrita release to be more complete
# Check if Paradisi per illusi (1995) exists
paradisi = Release.objects.filter(band=negrita, title__icontains='Paradisi').first()
if paradisi:
    print(f"\nParadisi per illusi already exists: {paradisi.title} ({paradisi.year})")
else:
    # Add Paradisi per illusi
    Release.objects.create(
        band=negrita,
        title='Paradisi per illusi',
        format='cd',
        year=1995,
        label='Black Out / Mercury',
        description='Mini-album. Recorded partly in Salvador de Bahia, Brazil. Lead single presented live throughout Europe. Represented Italy at European Rock Festival in Turkey.',
    )
    print("Added: Paradisi per illusi (1995)")

# Check Reset (1999)
reset = Release.objects.filter(band=negrita, title__icontains='Reset').first()
if reset:
    print(f"Reset already exists: {reset.title} ({reset.year})")
else:
    Release.objects.create(
        band=negrita,
        title='Reset',
        format='cd',
        year=1999,
        label='Black Out / Mercury',
        description='Harder rock direction. Features "Mama maé".',
    )
    print("Added: Reset (1999)")

# Check XXX (1997)
xxx = Release.objects.filter(band=negrita, title__icontains='XXX').first()
if xxx:
    print(f"XXX already exists: {xxx.title} ({xxx.year})")
else:
    Release.objects.create(
        band=negrita,
        title='XXX',
        format='cd',
        year=1997,
        label='Black Out / Mercury',
        description='Platinum album. Recorded in USA. Collaborated with Aldo, Giovanni e Giacomo for film soundtracks.',
    )
    print("Added: XXX (1997)")

print(f"\nTotal releases for Negrita now: {negrita.releases.count()}")
