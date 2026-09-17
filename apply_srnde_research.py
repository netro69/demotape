# Created-by: architect | Date: 2026-09-17
# SRNDE (id=120) research update script for Demotape.
# Run: cd ~/Projects/demotape && source .venv/bin/activate && python manage.py shell < apply_srnde_research.py

import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, GenreTag, Release

print("=" * 60)
print("APPLYING SRNDE RESEARCH")
print("=" * 60)

# Get SRNDE
srnde = Band.objects.get(id=120)
print(f"\nTarget: SRNDE (id={srnde.id})")

# Update band info with expanded bio
srnde.bio = """SRNDE is an Italian electronic music producer and DJ specializing in melodic house, deep house, chill house, and EDM-pop. Active since 2023, the project maintains anonymity regarding personal identity, though some releases credit composer Samuel Gori (also Johnny Francesco Gori). With 177+ million global streams and 547K+ monthly listeners on Spotify, SRNDE has achieved significant international recognition in the underground electronic scene.

The producer's sound blends nostalgic '70s and '80s influences with modern deep house production, creating accessible, radio-friendly electronic music. Tracks frequently feature collaborations with vocalists and other producers. SRNDE has released through established dance labels including Armada Music, Soave Records, Tremble (ATLAST imprint), Chill Your Mind, Gahara, Gekai, Paraiso, Sony Music, and THE NIGHT DRIVE.

Notable releases include "Missing" with Giorgio Gee (2024), "Fresh Eyes" with PHARØ and Robbie Rosen (2025), and "I Was Made For Loving You" with Summer Is Calling (2025, Armada Music). The "BTM Chill Relax" series with one more cig showcases a downtempo/chillout side."""
srnde.city = "Italy"
srnde.active_years = "2023–present"
srnde.status = "published"
srnde.save()
print(f"Updated band info: city={srnde.city}, years={srnde.active_years}")

# Add genre tags
genre_names = ['electronic', 'deep-house', 'house', 'chill-house', 'edm']
for gn in genre_names:
    try:
        g = GenreTag.objects.get(slug=gn)
        srnde.genre_tags.add(g)
        print(f"Added genre: {g.name}")
    except GenreTag.DoesNotExist:
        g = GenreTag.objects.create(name=gn.replace('-', ' ').title(), slug=gn)
        srnde.genre_tags.add(g)
        print(f"Created and added genre: {g.name}")

# Add Links (new ones not already in DB)
links_data = [
    ('streaming', 'Deezer — Artist profile', 'https://www.deezer.com/us/artist/122723452', False, 'Full discography, top albums and concerts on Deezer'),
    ('streaming', 'Shazam — Artist profile', 'https://www.shazam.com/artist/srnde/1585017719', False, 'Song lyrics, music videos, tour dates on Shazam'),
    ('streaming', 'YouTube Music — Channel', 'https://music.youtube.com/channel/UCoCn2HFUy-HlvVTTJMRLmNQ', False, 'Official YouTube Music channel'),
    ('streaming', 'Amazon Music — Artist', 'https://www.amazon.com/music/player/artists/B08W53QCTM/srnde', False, 'Stream ad-free or purchase CDs and MP3s on Amazon Music'),
    ('streaming', 'Juno Download — MP3 downloads', 'https://www.junodownload.com/artists/Srnde/releases/', False, 'Legal MP3 tracks and releases for download'),
    ('streaming', 'Music Worx — Artist page', 'https://open.music-worx.com/artist/srnde/377445', False, 'Streaming and release information'),
    ('video', 'Let Her Go feat. Christie Reeves (YouTube)', 'https://www.youtube.com/watch?v=7E9wUqB8O3s', False, 'EDM Pop music video with Christie Reeves'),
    ('video', 'I Was Made For Loving You — Armada Music TV', 'https://archive.org/details/youtube-VMuuiF11IS8', False, 'Armada Music TV upload of the KISS cover remake'),
    ('archive', 'Elektrobeats — Artist profile', 'https://elektrobeats.org/music/artist/srnde', False, 'Electronic music database entry'),
]

links_added = 0
for link_type, title, url, is_primary, description in links_data:
    link, created = Link.objects.get_or_create(
        band=srnde,
        url=url,
        defaults={
            'link_type': link_type,
            'title': title,
            'is_primary': is_primary,
            'description': description,
        }
    )
    if created:
        links_added += 1
        print(f"Added link: {title}")
    else:
        print(f"Already exists: {title}")

print(f"\nTotal links added: {links_added}")

# Add Releases (singles)
releases_data = [
    ("Get It On", 2023, "Soave Records", "with Franz Kolo", "srnde-get-it-on"),
    ("Missing", 2024, "THE NIGHT DRIVE", "with Giorgio Gee", "srnde-missing"),
    ("Lovely", 2024, None, "Solo single", "srnde-lovely"),
    ("Jupiter", 2024, "Tremble / ATLAST", "Solo — composer: Samuel Gori", "srnde-jupiter"),
    ("Your Love", 2024, None, "with Claim", "srnde-your-love"),
    ("I Was Made For Loving You", 2025, "Armada Music", "with Summer Is Calling", "srnde-i-was-made-for-loving-you"),
    ("Fresh Eyes", 2025, "Soave Records", "with PHARØ feat. Robbie Rosen", "srnde-fresh-eyes"),
    ("Up To The Top", 2025, None, "with Titanz & Martin Noiserz feat. Scarlett", "srnde-up-to-the-top"),
    ("Because The Night", 2025, None, "Solo single", "srnde-because-the-night"),
    ("She's Not There", 2025, None, "Solo single", "srnde-shes-not-there"),
    ("A Spaceman Came Travelling", 2025, None, "Solo single", "srnde-a-spaceman-came-travelling"),
    ("Rinnina", 2025, None, "with KEL (album)", "srnde-rinnina"),
    ("Let Her Go", 2025, None, "feat. Christie Reeves", "srnde-let-her-go"),
    ("Butterfly", 2026, None, "Solo single", "srnde-butterfly"),
    ("Grace's Ghost", 2026, None, "with one more cig", "srnde-graces-ghost"),
]

releases_added = 0
for title, year, label, description, slug in releases_data:
    release, created = Release.objects.get_or_create(
        slug=slug,
        defaults={
            'band': srnde,
            'title': title,
            'year': year,
            'label': label or '',
            'format': 'digital',
            'description': description,
            'status': 'published',
        }
    )
    if created:
        releases_added += 1
        print(f"Added release: {title} ({year})")
    else:
        print(f"Already exists: {title}")

print(f"\nTotal releases added: {releases_added}")

# Add Connections (collaborators)
# First, create missing collaborator bands
collaborators_to_create = [
    ("Giorgio Gee", "Italian electronic music producer, co-producer on Missing"),
    ("Franz Kolo", "Italian electronic music producer, co-producer on Get It On"),
    ("PHARØ", "Electronic music producer, co-producer on Fresh Eyes"),
    ("Robbie Rosen", "Vocalist, featured on Fresh Eyes"),
    ("Summer Is Calling", "Electronic music project, co-producer on I Was Made For Loving You"),
    ("one more cig", "Electronic music project, collaborator on BTM Chill Relax series"),
    ("Claim", "Electronic music project, co-producer on Your Love"),
    ("Christie Reeves", "Vocalist, featured on Let Her Go"),
    ("David Micheal Frank", "Artist, featured on Eye Of The Tiger (already in DB as id=116)"),
    ("Sam Ryan", "Producer, collaborator with PHARØ and Robbie Rosen"),
    ("DROP", "Producer, Sway Extended Mix collaborator"),
    ("Last Vice", "Artist, co-producer on I Hope You Make It"),
    ("Martin Noiserz", "Producer, co-producer on Up To The Top"),
    ("Scarlett", "Vocalist, featured on Up To The Top"),
    ("KEL", "Artist, collaborator on Rinnina album"),
    ("Titanz", "Producer, co-producer on Up To The Top"),
]

# Create missing bands
created_bands = {}
for name, bio_note in collaborators_to_create:
    band, created = Band.objects.get_or_create(
        name=name,
        defaults={
            'slug': name.lower().replace(' ', '-').replace("'", '').replace('ø', 'o'),
            'bio': bio_note,
            'status': 'draft',
        }
    )
    created_bands[name] = band
    if created:
        print(f"Created band: {name} (id={band.id})")
    else:
        print(f"Band exists: {name} (id={band.id})")

# Add connections
connections_data = [
    ("Giorgio Gee", "collaboration", "Co-producer on Missing (2024)"),
    ("Franz Kolo", "collaboration", "Co-producer on Get It On (2023)"),
    ("PHARØ", "collaboration", "Co-producer on Fresh Eyes (2025)"),
    ("Robbie Rosen", "collaboration", "Vocalist on Fresh Eyes (2025)"),
    ("Summer Is Calling", "collaboration", "Co-producer on I Was Made For Loving You (2025)"),
    ("one more cig", "collaboration", "BTM Chill Relax series collaborator"),
    ("Claim", "collaboration", "Co-producer on Your Love"),
    ("Christie Reeves", "collaboration", "Vocalist on Let Her Go (2025)"),
    ("David Micheal Frank", "collaboration", "Featured on Eye Of The Tiger"),
    ("Sam Ryan", "scene_peer", "Collaborator with PHARØ and Robbie Rosen"),
    ("DROP", "collaboration", "Sway Extended Mix remixer"),
    ("Last Vice", "collaboration", "Co-producer on I Hope You Make It"),
    ("Martin Noiserz", "collaboration", "Co-producer on Up To The Top (2025)"),
    ("Scarlett", "collaboration", "Vocalist on Up To The Top (2025)"),
    ("KEL", "collaboration", "Collaborator on Rinnina album (2025)"),
    ("Titanz", "collaboration", "Co-producer on Up To The Top (2025)"),
]

connections_added = 0
for to_name, conn_type, notes in connections_data:
    to_band = created_bands[to_name]
    conn, created = BandConnection.objects.get_or_create(
        from_band=srnde,
        to_band=to_band,
        connection_type=conn_type,
        defaults={'notes': notes}
    )
    if created:
        connections_added += 1
        print(f"Added connection: SRNDE → {to_name} ({conn_type})")
    else:
        print(f"Connection exists: SRNDE → {to_name}")

print(f"\nTotal connections added: {connections_added}")

# Final summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Band: SRNDE (id=120)")
print(f"Genre tags: {list(srnde.genre_tags.values_list('name', flat=True))}")
print(f"Total links: {Link.objects.filter(band=srnde).count()}")
print(f"Total connections: {BandConnection.objects.filter(from_band=srnde).count()}")
print(f"Total releases: {Release.objects.filter(band=srnde).count()}")
print("=" * 60)
