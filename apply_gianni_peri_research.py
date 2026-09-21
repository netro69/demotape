# Created-by: agent | Date: 2026-09-17
# Session: subagent
#!/usr/bin/env python3
"""
Gianni Peri research update script for Demotape.
Run: cd ~/Projects/demotape && source .venv/bin/activate && python manage.py shell < apply_gianni_peri_research.py
"""

import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, GenreTag

print("=" * 60)
print("APPLYING GIANNI PERI RESEARCH")
print("=" * 60)

# Get Gianni Peri
peri = Band.objects.get(slug='gianni-peri')
print(f"\nTarget: Gianni Peri (id={peri.id})")

# Update band info
old_bio = peri.bio
new_bio = ("Italian mastering engineer, music producer, songwriter, video editor, and occasional "
           "performing artist from Lucca, Tuscany, Italy. Active since 1999. Credits include 40+ releases "
           "on Discogs and 30+ songs listed on Genius. Worked across Italian house/dance productions "
           "and modern darkwave, minimal synth, EBM, synthpop, and industrial mastering for "
           "international artists including Boy Harsher. Also active in video editing/post-production.")

if old_bio == new_bio:
    print("Bio unchanged, skipping")
else:
    peri.bio = new_bio
    peri.city = "Lucca"
    peri.active_years = "1999-present"
    peri.website = "http://www.gianniperi.it/"
    peri.discogs_id = "1615582"
    peri.musicbrainz_id = "eff1a309-9c1c-4527-b68a-0a2c62cdf523"
    peri.status = "published"
    peri.save()
    print(f"Updated band info: city={peri.city}, years={peri.active_years}, status=published")

# Add genre tags
genre_names = ['house', 'tech-house', 'dance', 'electronic', 'darkwave', 'minimal-synth',
               'ebm', 'synthpop', 'industrial', 'coldwave', 'post-punk']
for gn in genre_names:
    try:
        g = GenreTag.objects.get(slug=gn)
        peri.genre_tags.add(g)
        print(f"  Added genre: {g.name}")
    except GenreTag.DoesNotExist:
        g = GenreTag.objects.create(name=gn.replace('-', ' ').title(), slug=gn)
        peri.genre_tags.add(g)
        print(f"  Created and added genre: {g.name}")

# Add Links
links_data = [
    ('website', 'Official Website', 'http://www.gianniperi.it/', True, 'Gianni Peri official site - credits, contact, portfolio'),
    ('website', 'Rockit Professional Credits', 'https://www.rockit.it/professionista/Gianni+Peri', False, 'Italian music industry professional credits page'),
    ('archive', 'AllMusic', 'https://www.allmusic.com/artist/gianni-peri-mn0002729514', False, 'AllMusic biography & discography'),
    ('archive', 'RateYourMusic', 'https://rateyourmusic.com/artist/gianni-peri', False, 'RateYourMusic artist profile with credits'),
    ('archive', 'MusicBrainz', 'https://musicbrainz.org/artist/eff1a309-9c1c-4527-b68a-0a2c62cdf523', False, 'MusicBrainz artist page'),
    ('archive', 'Encyclopaedia Metallum', 'https://www.metal-archives.com/artists/Gianni_Peri/1049952', False, 'Encyclopaedia Metallum artist page'),
    ('archive', 'Genius', 'https://genius.com/artists/Gianni-peri', False, 'Genius songs & lyrics (30+ songs attributed)'),
    ('archive', 'Discogs', 'https://www.discogs.com/artist/1615582-Gianni-Peri', False, 'Complete discography with 40+ credits'),
    ('streaming', 'SoundCloud', 'https://soundcloud.com/gianniperi', False, 'SoundCloud profile (77 followers, 5 tracks)'),
    ('streaming', 'Deezer', 'https://www.deezer.com/en/artist/5981498', False, 'Deezer artist profile'),
    ('streaming', 'Bandcamp (Tagged)', 'https://bandcamp.com/discover/gianni-peri', False, 'Bandcamp discover tag'),
    ('streaming', 'Spotify (Mastering Credits)', 'https://open.spotify.com/artist/4RbZ9lwnXlWzm0G9UZ8NEX', False, 'Streaming via mastering credits on various releases'),
    ('video', 'VOGUE.NOIR Resolution Film', 'https://www.youtube.com/watch?v=c92i3L-xCdU', False, 'VOGUE.NOIR Resolution film (mastered by Gianni Peri)'),
    ('video', 'Indecent Excision MV', 'https://www.youtube.com/watch?v=9Y1DLWYzvk8', False, 'Indecent Excision "Hallucination of Murder" MV'),
    ('video', 'Cuushe Magic Video', 'https://www.youtube.com/watch?v=BcMNnKq3mzI', False, 'Cuushe "Magic" official video (video edit mastered)'),
    ('social', 'Instagram', 'https://www.instagram.com/gianni.peri/', False, '@gianni.peri (168 followers, 6 posts)'),
    ('social', 'Facebook', 'https://www.facebook.com/gianni.peri.5', False, 'Facebook page (802 followers)'),
    ('social', 'LinkedIn', 'https://it.linkedin.com/in/gianni-peri-b981b597', False, 'LinkedIn profile (231 followers, 233 connections)'),
]

links_added = 0
for link_type, title, url, is_primary, description in links_data:
    link, created = Link.objects.get_or_create(
        band=peri,
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

# Update existing connection to To You Mom (add notes)
try:
    to_you_mom = Band.objects.get(name='To You Mom:')
    conn, created = BandConnection.objects.get_or_create(
        from_band=peri,
        to_band=to_you_mom,
        connection_type='related_act',
        defaults={
            'notes': 'Gianni Peri mastered multiple To You Mom: releases',
            'source': 'research/to_you_mom.md'
        }
    )
    if created:
        print(f"\n  + Connection: Gianni Peri -> To You Mom: (related_act)")
    else:
        print(f"\n  = Already exists: Gianni Peri -> To You Mom: (related_act)")
except Band.DoesNotExist:
    print(f"\n  ! Band not found: To You Mom:")

# Summary
print("\n" + "=" * 60)
print("GIANNI PERI RESEARCH UPDATE COMPLETE")
print("=" * 60)
print(f"Band: Gianni Peri (id={peri.id})")
print(f"City: {peri.city}")
print(f"Active: {peri.active_years}")
print(f"Status: {peri.status}")
print(f"Genres: {', '.join(g.name for g in peri.genre_tags.all())}")
print(f"Total links for Gianni Peri: {Link.objects.filter(band=peri).count()}")
print(f"Total connections for Gianni Peri: {BandConnection.objects.filter(from_band=peri).count() + BandConnection.objects.filter(to_band=peri).count()}")
print(f"\nConnections:")
for c in BandConnection.objects.filter(from_band=peri):
    print(f"  -> {c.to_band.name} ({c.connection_type})")
for c in BandConnection.objects.filter(to_band=peri):
    print(f"  <- {c.from_band.name} ({c.connection_type})")