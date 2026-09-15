#!/usr/bin/env python3
"""
Demotape database seeder — populates bands, releases, and connections.
Run: python manage.py shell < seed_demotape.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Release, Track, GenreTag, Label, BandConnection

# Clear existing data (for fresh start)
print("Clearing existing data...")
Band.objects.all().delete()
Release.objects.all().delete()
Track.objects.all().delete()
GenreTag.objects.all().delete()
Label.objects.all().delete()
BandConnection.objects.all().delete()

# Create labels
print("Creating labels...")
labels_data = [
    ("ghost-records", "Ghost Records", "Varese"),
    ("tube-records", "Tube Records", "Varese"),
    ("gamma-pop", "Gamma Pop", "Varese"),
    ("face-record", "Face Record", "Piacenza"),
    ("chaos-village", "Chaos Village", "Varese"),
    ("santeria", "Santeria", "Varese"),
    ("fannullare", "FANNULLARE", "Varese"),
    ("sezioneaurea", "sezioneaurea", "Varese"),
    ("urlo", "Urlo", "Varese"),
]
for slug, name, city in labels_data:
    Label.objects.update_or_create(slug=slug, defaults={"name": name, "city": city})

ghost_records = Label.objects.get(slug="ghost-records")
tube_records = Label.objects.get(slug="tube-records")
gamma_pop = Label.objects.get(slug="gamma-pop")
face_record = Label.objects.get(slug="face-record")
chaos_village = Label.objects.get(slug="chaos-village")
santeria = Label.objects.get(slug="santeria")
fannullare = Label.objects.get(slug="fannullare")
sezioneaurea = Label.objects.get(slug="sezioneaurea")
urlo = Label.objects.get(slug="urlo")

# Create genre tags
print("Creating genre tags...")
genres = {
    'noise-rock': GenreTag.objects.get_or_create(name='Noise Rock', slug='noise-rock')[0],
    'psychedelic-punk': GenreTag.objects.get_or_create(name='Psychedelic Punk', slug='psychedelic-punk')[0],
    'space-rock': GenreTag.objects.get_or_create(name='Space Rock', slug='space-rock')[0],
    'post-punk': GenreTag.objects.get_or_create(name='Post-Punk', slug='post-punk')[0],
    'minimalism': GenreTag.objects.get_or_create(name='Minimalism', slug='minimalism')[0],
    'punk-rock': GenreTag.objects.get_or_create(name='Punk Rock', slug='punk-rock')[0],
    'gothic-rock': GenreTag.objects.get_or_create(name='Gothic Rock', slug='gothic-rock')[0],
    'dark': GenreTag.objects.get_or_create(name='Dark', slug='dark')[0],
    'garage-punk': GenreTag.objects.get_or_create(name='Garage Punk', slug='garage-punk')[0],
    'rock-n-roll': GenreTag.objects.get_or_create(name="Rock'n'Roll", slug='rock-n-roll')[0],
    'electronic': GenreTag.objects.get_or_create(name='Electronic', slug='electronic')[0],
    'experimental': GenreTag.objects.get_or_create(name='Experimental', slug='experimental')[0],
}

# Create bands
print("Creating bands...")

# Asphodel
asphodel = Band.objects.create(
    name='Asphodel',
    slug='asphodel',
    city='Varese',
    active_years='1990-1996',
    bio='Noise rock / psychedelic punk band from Varese. Members: Roberto Binda (voice), Tommaso Canal (bass), PG Molinaro (guitar), Mauro Calderan (drums), Raffaello Migliarini (drums, from 1996). Releases: Smooth (1994, Face Record, Piacenza), Deluxe (1996, Chaos Village, Varese).',
    status='published'
)
asphodel.genre_tags.add(genres['noise-rock'], genres['psychedelic-punk'])

# Clark Nova
clark_nova = Band.objects.create(
    name='Clark Nova',
    slug='clark-nova',
    city='Varese',
    active_years='1995-2010',
    bio='Space rock / psychedelic / noise band from Varese. Members: Stefano Tosoni (vocals), Stefano Savastano (bass, 1995-98), Davide Sardi (bass, 1997-present), Alessandro Sardi (guitar), Roberto "dr." (drums). Influences: Spacemen 3, Telescopes, Morlocks, Fuzztones, Jesus and Mary Chain, 13th Floor Elevators, Barrett, Mudhoney, Kraftwerk.',
    status='published'
)
clark_nova.genre_tags.add(genres['space-rock'], genres['psychedelic-punk'], genres['noise-rock'])

# Bartòk
bartok = Band.objects.create(
    name='Bartòk',
    slug='bartok',
    city='Varese',
    active_years='1999-2004',
    bio='Post-punk / minimalism / urban blues band from Varese. Atypical formation: piano, cello, bass, drums, voice, electronics. Members: Loris Antoniazzi (and others). Releases: "The Finest Way To Offend You" (Gamma Pop, 2001), "Few lazy words" (Ghost Records/Santeria, 2003).',
    status='published'
)
bartok.genre_tags.add(genres['post-punk'], genres['minimalism'])

# Porno Riviste
porno_riviste = Band.objects.create(
    name='Porno Riviste',
    slug='porno-riviste',
    city='Venegono Superiore (VA)',
    active_years='1992-2009, 2012-2015, 2019-present',
    bio='Punk rock band from Venegono Superiore, near Varese. Members: Tommi Marson (voice, guitar), Marco Mortillaro (bass, voice), Filippo Vegezzi, Umberto Faganelli "Rambo", Daniele Marceca "Dani" (guitar, voice), Alberto Bregolin "Becio" (drums).',
    status='published'
)
porno_riviste.genre_tags.add(genres['punk-rock'])

# Mind Drop
mind_drop = Band.objects.create(
    name='Mind Drop',
    slug='mind-drop',
    city='Varese',
    active_years='1990-1996',
    bio='Gothic rock / post-punk / dark band from Varese. Releases: "Lurking Fear" (1991, demo), "Rusted Eternity" (1993, demo), "Side of Mine" (1996, CD). Later changed name to Plastik.',
    status='published'
)
mind_drop.genre_tags.add(genres['gothic-rock'], genres['post-punk'], genres['dark'])

# Ocropoid
ocropoid = Band.objects.create(
    name='Ocropoid',
    slug='ocropoid',
    city='Varese',
    active_years='2011-present',
    bio='Electronic / experimental / noise project. Releases: "Le radici dell\'odio" (2017), plus tracks on compilations. Active on streaming platforms.',
    status='published'
)
ocropoid.genre_tags.add(genres['electronic'], genres['experimental'])

# Thee Stolen Cars
thee_stolen_cars = Band.objects.create(
    name='Thee Stolen Cars',
    slug='thee-stolen-cars',
    city='Stresa (Novara)',
    active_years='1986-1991',
    bio='Garage punk / rock\'n\'roll band from Stresa. Members: Michele Anelli (bass, leader), plus others. Releases: Self-titled demo tape (1986), EP (1991, via Urlo magazine).',
    status='published'
)
thee_stolen_cars.genre_tags.add(genres['garage-punk'], genres['rock-n-roll'])

# Create releases
print("Creating releases...")

# Asphodel releases
Release.objects.create(
    band=asphodel,
    title='Smooth',
    slug='smooth',
    format='cd',
    year=1994,
    label=face_record,
    description='CD release on Face Record (Piacenza).',
    status='published'
)
Release.objects.create(
    band=asphodel,
    title='Deluxe',
    slug='deluxe',
    format='cd',
    year=1996,
    label=chaos_village,
    description='CD release on Chaos Village (Varese).',
    status='published'
)

# Clark Nova releases
Release.objects.create(
    band=clark_nova,
    title='One Way Airport',
    slug='one-way-airport',
    format='digital',
    year=2010,
    label=ghost_records,
    description='Track on Ghost Records 10-year compilation.',
    status='published'
)

# Bartòk releases
Release.objects.create(
    band=bartok,
    title='The Finest Way To Offend You',
    slug='the-finest-way-to-offend-you',
    format='cd',
    year=2001,
    label=gamma_pop,
    description='Debut album on Gamma Pop. Recorded by David Lenci at Red House Recordings.',
    status='published'
)
Release.objects.create(
    band=bartok,
    title='Few lazy words',
    slug='few-lazy-words',
    format='cd',
    year=2003,
    label=santeria,
    description='Second album on Ghost Records/Santeria.',
    status='published'
)

# Porno Riviste releases
Release.objects.create(
    band=porno_riviste,
    title='Chi non combatte cade',
    slug='chi-non-combatte-cade',
    format='cassette',
    year=1995,
    label=tube_records,
    description='Demo tape. Later reissued on vinyl.',
    status='published'
)
Release.objects.create(
    band=porno_riviste,
    title='Sogni e incubi',
    slug='sogni-e-incubi',
    format='cassette',
    year=1996,
    label=tube_records,
    description='Second demo tape.',
    status='published'
)

# Mind Drop releases
Release.objects.create(
    band=mind_drop,
    title='Lurking Fear',
    slug='lurking-fear',
    format='cassette',
    year=1991,
    description='Demo tape. Likely out of print.',
    status='published'
)
Release.objects.create(
    band=mind_drop,
    title='Rusted Eternity',
    slug='rusted-eternity',
    format='cassette',
    year=1993,
    description='Demo tape. Likely out of print.',
    status='published'
)
Release.objects.create(
    band=mind_drop,
    title='Side of Mine',
    slug='side-of-mine',
    format='cd',
    year=1996,
    description='CD release. May be out of print.',
    status='published'
)

# Ocropoid releases
Release.objects.create(
    band=ocropoid,
    title='Le radici dell\'odio',
    slug='le-radici-dell-odio',
    format='digital',
    year=2017,
    label=fannullare,
    description='Digital release on FANNULLARE.',
    status='published'
)

# Thee Stolen Cars releases
Release.objects.create(
    band=thee_stolen_cars,
    title='Thee Stolen Cars',
    slug='thee-stolen-cars',
    format='cassette',
    year=1986,
    label=urlo,
    description='Self-titled demo tape. Likely lost.',
    status='published'
)
Release.objects.create(
    band=thee_stolen_cars,
    title='EP',
    slug='ep',
    format='cd',
    year=1991,
    label=urlo,
    description='EP via Urlo magazine. May be out of print.',
    status='published'
)

# Create connections
print("Creating connections...")

connections = [
    (asphodel, clark_nova, 'scene_peer'),
    (asphodel, bartok, 'successor'),
    (asphodel, porno_riviste, 'scene_peer'),
    (clark_nova, bartok, 'label_mate'),
    (clark_nova, porno_riviste, 'scene_peer'),
    (bartok, porno_riviste, 'scene_peer'),
    (mind_drop, clark_nova, 'scene_peer'),
    (mind_drop, bartok, 'scene_peer'),
    (ocropoid, clark_nova, 'scene_peer'),
    (thee_stolen_cars, clark_nova, 'scene_peer'),
    (thee_stolen_cars, bartok, 'scene_peer'),
]

for band1, band2, conn_type in connections:
    BandConnection.objects.create(
        from_band=band1,
        to_band=band2,
        connection_type=conn_type
    )

print("Done!")
print(f"Created {Band.objects.count()} bands")
print(f"Created {Release.objects.count()} releases")
print(f"Created {BandConnection.objects.count()} connections")
