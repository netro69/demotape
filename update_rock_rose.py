import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, Release, Label, Fanzine, FanzineReview

band = Band.objects.get(id=142)

# 1. UPDATE BIO
band.bio = (
    "Rock Rose (also spelled Rockrose) was an Italian melodic hard rock/metal band from Rome, "
    "formed in 1986 after the first split of Scarlet (a female-fronted band whose 1985 demo "
    "featured Claudia Ruti on vocals and Stefano Toni on drums — both formerly of Lunar Sex, "
    "who released a self-titled LP in 1982). When vocalist Claudia Ruti left Scarlet in 1986, "
    "Elisabetta 'Beth' Valero replaced her and the band changed its name to Rockrose. "
    "They released one demo tape, 'Pick the Rose' (1987, self-released cassette), before "
    "vocalist Jon Pearo joined and the band reverted to the Scarlet name around 1988. "
    "Rock Rose is thus both a successor to Scarlet and a shared-member offshoot of Lunar Sex."
)
band.save()
print(f"Updated bio for {band.name}")

# 2. ADD LINKS
links_to_add = [
    ('website', 'Rockrose - Metal Archives', 'https://www.metal-archives.com/bands/Rockrose/3540494599', 'Metal Archives entry for Rockrose (Pick the Rose demo, 1987)', True),
    ('archive', 'Rock Rose Discogs Release', 'https://www.discogs.com/pt_BR/release/21289591-RockRose-Pick-The-Rose', 'Discogs entry for Pick The Rose demo tape (1987, Not On Label)', False),
    ('archive', 'Heavy Metal Rarities Forum Thread', 'https://heavymetalrarities.com/forum/viewtopic.php?f=19&t=10338', 'Forum thread with detailed history of Rock Rose and their Scarlet/Lunar Sex lineage', False),
]

for link_type, title, url, desc, is_primary in links_to_add:
    link, created = Link.objects.get_or_create(
        band=band,
        url=url,
        defaults={'link_type': link_type, 'title': title, 'description': desc, 'is_primary': is_primary}
    )
    print(f"  {'Created' if created else 'Exists'}: [{link_type}] {title}")

# 3. ADD CONNECTIONS
try:
    lunar_sex = Band.objects.get(id=140)
    conn, created = BandConnection.objects.get_or_create(
        from_band=band,
        to_band=lunar_sex,
        connection_type='shared_member',
        defaults={
            'notes': 'Claudia Ruti (vocals) and Stefano Toni (drums) were in both Rock Rose and Lunar Sex. Rock Rose evolved from Scarlet\'s 1986 split.',
            'source': 'https://www.metal-archives.com/bands/Rockrose/3540494599'
        }
    )
    print(f"  {'Created' if created else 'Exists'}: connection to Lunar Sex (shared_member)")
except Band.DoesNotExist:
    print("  Lunar Sex (id=140) not found!")

# 4. ADD RELEASE
release, created = Release.objects.get_or_create(
    band=band,
    title='Pick the Rose',
    year=1987,
    defaults={'format': 'Cassette', 'catalog_number': 'none', 'description': 'Self-released demo tape — 1st and sole release. Recorded as Rockrose after Scarlet\'s 1986 split.'}
)
print(f"  {'Created' if created else 'Exists'}: release 'Pick the Rose' (1987)")

# 5. CHECK FANZINE MODEL
print(f"\nFanzine model check:")
try:
    fanzine = Fanzine.objects.all()
    print(f"  Total fanzines: {fanzine.count()}")
    for f in fanzine:
        print(f"    {f.name} (id={f.id})")
except Exception as e:
    print(f"  Error: {e}")

print(f"\nFinal band state: {band.name} | links={band.links.count()} | connections={band.connections_from.count() + band.connections_to.count()} | releases={band.releases.count()}")
