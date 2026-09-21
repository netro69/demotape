# Created-by: agent | Date: 2026-09-17
# Session: automated

#!/usr/bin/env python3
"""
Scisma research update script for Demotape.
Run: cd ~/Projects/demotape && source .venv/bin/activate && python manage.py shell < apply_scisma_research.py
"""

import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, GenreTag

print("=" * 60)
print("APPLYING SCISMA RESEARCH")
print("=" * 60)

# Get Scisma
scisma = Band.objects.get(id=78)
print(f"\nTarget: Scisma (id={scisma.id})")

# Update band info
scisma.bio = """Italian indie rock band formed in 1993 on the western shores of Lake Garda (Toscolano-Maderno area), Brescia, Lombardy. Active from 1993 to 2003, with a reunion from 2014 to 2015.

Scisma were a key act in the Italian alternative rock scene of the 1990s. Critics described them as "magniloquenti" (magniloquent) and an "imprescindibile" (essential) group for their sophisticated, refined, and intellectual approach to rock. Their sound incorporated jazz, pop, European new wave, and experimental elements alongside their rock foundation.

They won Rock Targato Italia and Arezzo Wave in 1996, launching their live career. Three studio albums followed: the self-produced debut "Bombardano Cortina" (1995), the Manuel Agnelli-produced "Rosemary Plexiglas" (1997), and their masterpiece "Armstrong" (1999) on EMI/Parlophone. The 2015 reunion EP "Mr. Newman" was considered their final work.

Frontman Paolo Benvegnù (also primary songwriter/guitarist) died on December 31, 2024, at age 59. He was eulogized as a seminal figure of Italian alternative rock and had a successful solo career after Scisma's initial 2003 breakup."""
scisma.city = "Toscolano-Maderno (Brescia), Lombardy"
scisma.active_years = "1993–2003, 2014–2015"
scisma.website = "https://it.wikipedia.org/wiki/Scisma_(gruppo_musicale)"
scisma.status = "published"
scisma.save()
print(f"Updated band info: city={scisma.city}, years={scisma.active_years}")

# Add genre tags
genre_names = ['art-rock', 'indie-rock', 'chamber-rock', 'new-wave']
for gn in genre_names:
    try:
        g = GenreTag.objects.get(slug=gn)
        scisma.genre_tags.add(g)
        print(f"Added genre: {g.name}")
    except GenreTag.DoesNotExist:
        g = GenreTag.objects.create(name=gn.replace('-', ' ').title(), slug=gn)
        scisma.genre_tags.add(g)
        print(f"Created and added genre: {g.name}")

# Add Links
links_data = [
    ('archive', 'Wikipedia (IT) — Full article', 'https://it.wikipedia.org/wiki/Scisma_(gruppo_musicale)', True, 'Detailed Italian Wikipedia article covering formation, albums, members, and legacy'),
    ('archive', 'Discogs — Artist profile', 'https://www.discogs.com/artist/361409-Scisma', False, 'Complete discography with releases, credits, and track listings'),
    ('archive', 'Genius — Armstrong tracklist/lyrics', 'https://genius.com/albums/Scisma/Armstrong', False, 'Track-by-track lyrics and annotations for the Armstrong album'),
    ('archive', 'DeBaser — Album reviews', 'https://www.debaser.it/scisma/armstrong', False, 'Two professional reviews of the Armstrong album'),
    ('archive', 'OndaRock — Band profile', 'https://www.ondarock.it/scisma.htm', False, 'Rock criticism and reviews from Italian music journalism site'),
    ('archive', 'Last.fm — Music & stats', 'https://www.last.fm/music/Scisma', False, 'Listener statistics, similar artists, and track metadata'),
    ('archive', 'Estatica — Discography', 'https://www.estatica.it/en/musica/scisma/disco/armstrong', False, 'International discography database entry'),
    ('archive', 'ConcertArchives — Tour history', 'https://www.concertarchives.org/bands/scisma', False, 'Live concert history and venue data'),
    ('archive', 'Offtopic Magazine — 2015 reunion interview', 'https://offtopicmagazine.net/2015/10/30/scisma-ci-siamo-regalati-una-reunion-intervista-a-paolo-benvegnu/', False, 'Interview with Paolo Benvegnù about the 2014 reunion and Mr. Newman EP'),
    ('archive', 'Gardanotes — Paolo Benvegnù obituary', 'https://www.gardanotes.com/toscolano-maderno-mourns-paolo-benvegnu-icon-of-italian-music/', False, 'Local memorial article on Benvegnù as Scisma founder'),
    ('archive', 'Il Post — Paolo Benvegnù obituary', 'https://www.ilpost.it/2024/12/31/morto-paolo-benvegnu/', False, 'National news obituary covering his Scisma and solo career'),
    ('archive', 'Il Fatto Quotidiano — Benvegnù obituary', 'https://www.ilfattoquotidiano.it/2024/12/31/e-morto-paolo-benvegnu-cantautore-e-poeta-della-musica-italiana-si-e-spento-allimprovviso-a-59-anni/7821656/', False, 'Detailed obituary on Benvegnù as singer-songwriter and poet of Italian music'),
    ('archive', 'RAI News — Benvegnù obituary', 'https://www.rainews.it/articoli/2024/12/morto-a-59-anni-il-cantautore-paolo-benvegnu-2d9ebcbc-20df-4200-b52f-f321d4901601.html', False, 'RAI News coverage of Benvegnù\'s legacy in Italian alternative rock'),
    ('archive', 'WECB — Benvegnù obituary (EN)', 'https://www.wecb.fm/paolo-benvegnu-is-dead-he-was-59-years-old/', False, 'English-language obituary on Benvegnù\'s death'),
    ('archive', 'Giornale di Brescia — Tribute concert', 'https://www.giornaledibrescia.it/cultura/musica/padenghe-musica-indie-ricordo-paolo-benvegnu-hll244uj', False, 'Report on tribute concert featuring Scisma reunion performance'),
    ('archive', 'Borgate dal Vivo — Paolo Benvegnù', 'https://www.borgatedalvivo.it/paolo-benvegnu', False, 'Italian live music archive with Benvegnù/Scisma performance history'),
    ('video', 'Rosemary Plexiglas — Full Album (YouTube)', 'https://www.youtube.com/watch?v=KL3iKIrl2rI', False, 'Full album stream of the 1997 Manuel Agnelli-produced record'),
    ('video', 'Pezzetti di carta (1993) — YouTube playlist', 'https://www.youtube.com/playlist?list=PLiY0l1AiDXnYrdo4MMLjizSEFpmeDuFqy', False, 'Early 1993 recordings and demos'),
    ('video', 'Scisma documentary: "deserved so much more"', 'https://www.youtube.com/watch?v=-uwLTeicK5U', False, 'Documentary video on the band\'s story and legacy'),
]

links_added = 0
for link_type, title, url, is_primary, description in links_data:
    link, created = Link.objects.get_or_create(
        band=scisma,
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
    ('Afterhours', 'scene_peer', 'Both key acts in 90s Italian alternative rock; Manuel Agnelli produced Scisma\'s Rosemary Plexiglas', 'https://en.wikipedia.org/wiki/Afterhours_(band)'),
    ('Marlene Kuntz', 'scene_peer', 'Contemporaries in Italian alt-rock vanguard of the 1990s', 'https://en.wikipedia.org/wiki/Marlene_Kuntz'),
    ('Subsonica', 'scene_peer', 'Part of the same 90s Italian alternative rock wave', 'https://en.wikipedia.org/wiki/Subsonica'),
    ('Litfiba', 'scene_peer', 'Both from Lombardy/Rock Targato Italia scene, shared Italian alt-rock lineage', ''),
    ('Diaframma', 'scene_peer', 'Shared Italian alternative rock heritage; both Perpetuum Mobile Studios connections via Marco Tagliola', ''),
    ('Pankow', 'scene_peer', 'Connected through Italian indie/alternative network and shared producer Marco Tagliola', ''),
]

connections_added = 0
for band_name, conn_type, notes, source in connections_data:
    try:
        other_band = Band.objects.get(name=band_name)
        conn, created = BandConnection.objects.get_or_create(
            from_band=scisma,
            to_band=other_band,
            connection_type=conn_type,
            defaults={
                'notes': notes,
                'source': source
            }
        )
        if created:
            connections_added += 1
            print(f"  + Connection: Scisma -> {band_name} ({conn_type})")
        else:
            print(f"  = Already exists: Scisma -> {band_name} ({conn_type})")
    except Band.DoesNotExist:
        print(f"  ! Band not found: {band_name}")

print(f"\nConnections added: {connections_added}")

# Summary
print("\n" + "=" * 60)
print("SCISMA RESEARCH UPDATE COMPLETE")
print("=" * 60)
print(f"Band: Scisma (id={scisma.id})")
print(f"City: Toscolano-Maderno (Brescia)")
print(f"Active: 1993–2003, 2014–2015")
print(f"Genres: {', '.join(g.name for g in scisma.genre_tags.all())}")
print(f"Total links for Scisma: {Link.objects.filter(band=scisma).count()}")
print(f"Total connections for Scisma: {BandConnection.objects.filter(from_band=scisma).count() + BandConnection.objects.filter(to_band=scisma).count()}")
print(f"\nConnections:")
for c in BandConnection.objects.filter(from_band=scisma):
    print(f"  -> {c.to_band.name} ({c.connection_type})")
for c in BandConnection.objects.filter(to_band=scisma):
    print(f"  <- {c.from_band.name} ({c.connection_type})")
