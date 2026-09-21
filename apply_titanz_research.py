#!/usr/bin/env python3
"""
Titanz research update script for Demotape.
Run: cd ~/Projects/demotape && source .venv/bin/activate && python manage.py shell < apply_titanz_research.py
"""

import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, GenreTag

print("=" * 60)
print("APPLYING TITANZ RESEARCH")
print("=" * 60)

# Get Titanz (UK) - the underground DnB duo
titanz = Band.objects.get(id=137)
print(f"\nTarget: Titanz (id={titanz.id})")

# Update band info - focusing on UK duo (the obscure one Demotape tracks)
titanz.bio = """British neurofunk / drum and bass duo from Hastings, South East England, formed in 2022 by Dave Warren and Scott Ransom — friends for over 40 years with more than 50 years combined production and DJ experience.

Active and prolific: multiple releases per year on respected underground DnB labels including Close 2 Death, Arrival Archetype, Neurosense Audio, VTO Records, NeuroPlague Music, Warlock Audio, Dirtbox, and NeuroPlague Music. Known for dark, heavy, neurofunk-influenced sound.

Note: Name is ambiguous — also a Malaysian pop/rock band "Titanz Band" (fronted by vocalist Leehin) signed to MVM Music, active since ~2017."""
titanz.city = "Hastings, South East England"
titanz.active_years = "2022–present"
titanz.status = "published"
titanz.save()
print(f"Updated band info: city={titanz.city}, years={titanz.active_years}")

# Add genre tags
genre_names = ['neurofunk', 'drum-and-bass', 'electronic']
for gn in genre_names:
    try:
        g = GenreTag.objects.get(slug=gn)
        titanz.genre_tags.add(g)
        print(f"Added genre: {g.name}")
    except GenreTag.DoesNotExist:
        g = GenreTag.objects.create(name=gn.replace('-', ' ').title(), slug=gn)
        titanz.genre_tags.add(g)
        print(f"Created and added genre: {g.name}")

# Add Links
links_data = [
    ('official', 'Bandcamp (UK duo)', 'https://titanz2024.bandcamp.com/', True, 'Official Bandcamp page — music, discography, merchandise'),
    ('social', 'SoundCloud (UK)', 'https://soundcloud.com/titanzdnb', False, 'Track uploads and mixes from the UK duo'),
    ('social', 'Facebook (UK)', 'https://www.facebook.com/titanzdnb/', False, 'Facebook page for Titanz DnB duo'),
    ('streaming', 'Beatport', 'https://www.beatport.com/artist/titanz-uk/1332302', False, 'Beatport artist profile — full discography with labels and release dates'),
    ('streaming', 'Apple Music (UK)', 'https://music.apple.com/mw/artist/titanz-uk/1827916017', False, 'Apple Music profile'),
    ('streaming', 'Deezer', 'https://www.deezer.com/en/artist/378343331', False, 'Deezer artist profile'),
    ('streaming', '1001Tracklists', 'https://www.1001tracklists.com/artist/titanz-(uk)/tracks.html', False, 'Tracklists and DJ mixes featuring Titanz tracks'),
    ('archive', 'Inflyte biography', 'https://inflyteapp.com/r/p231y2', False, 'Artist biography and career info'),
    ('archive', 'LightAudio tracklist', 'https://lightaudio.ru/mp3/titanz(uk)', False, 'Track listing and release data'),
    ('archive', 'Best Drum and Bass Podcast', 'https://www.bestdrumandbass.com/podcast591/', False, 'Podcast featuring Titanz tracks and sets'),
]

links_added = 0
for link_type, title, url, is_primary, description in links_data:
    link, created = Link.objects.get_or_create(
        band=titanz,
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
    ('Subsonica', 'scene_peer', 'Both active Italian-adjacent electronic/rock scenes; cross-pollination of alternative UK/Italian electronic acts', ''),
    ('Diaframma', 'scene_peer', 'Shared underground scene heritage; Italian post-punk meets UK electronic underground', ''),
]

connections_added = 0
for band_name, conn_type, notes, source in connections_data:
    try:
        other_band = Band.objects.get(name=band_name)
        conn, created = BandConnection.objects.get_or_create(
            from_band=titanz,
            to_band=other_band,
            connection_type=conn_type,
            defaults={
                'notes': notes,
                'source': source
            }
        )
        if created:
            connections_added += 1
            print(f"  + Connection: Titanz -> {band_name} ({conn_type})")
        else:
            print(f"  = Already exists: Titanz -> {band_name} ({conn_type})")
    except Band.DoesNotExist:
        print(f"  ! Band not found: {band_name}")

print(f"\nConnections added: {connections_added}")

# Summary
print("\n" + "=" * 60)
print("TITANZ RESEARCH UPDATE COMPLETE")
print("=" * 60)
print(f"Band: Titanz (UK duo) (id={titanz.id})")
print(f"City: Hastings, South East England")
print(f"Active: 2022–present")
print(f"Genres: {', '.join(g.name for g in titanz.genre_tags.all())}")
print(f"Total links for Titanz: {Link.objects.filter(band=titanz).count()}")
print(f"Total connections for Titanz: {BandConnection.objects.filter(from_band=titanz).count() + BandConnection.objects.filter(to_band=titanz).count()}")
print(f"\nConnections:")
for c in BandConnection.objects.filter(from_band=titanz):
    print(f"  -> {c.to_band.name} ({c.connection_type})")
for c in BandConnection.objects.filter(to_band=titanz):
    print(f"  <- {c.from_band.name} ({c.connection_type})")
