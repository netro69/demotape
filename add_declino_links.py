#!/usr/bin/env python
"""Add found underground research links to Declino (ID=72) in the Demotape database."""
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Band, Link

BAND_ID = 72
added = []
errors = []

# Define the new links we found
new_links = [
    {
        'url': 'https://www.youtube.com/watch?v=jiu04muMeqs',
        'link_type': 'video',
        'title': 'Declino - Demo 1984 (Hardcore Punk Italy)',
        'description': 'Uploaded Jun 17, 2025. Rare 1984 demo: 1.Vita, 2.Vittime, 3.Diritto/Dovere',
    },
    {
        'url': 'https://www.discogs.com/artist/426083-Declino',
        'link_type': 'archive',
        'title': 'Declino - Discogs Discography',
        'description': 'Full discography: 7" EP (1983), Mucchio Selvaggio split tape with Negazione (1984), Eresia 12" EP (1985), Terra Bruciata 2xLP discography compilation',
    },
    {
        'url': 'https://thehcpunkdemotapesarchives.blogspot.com/2009/02/va-declino-vs-negazion-split-tape.html',
        'link_type': 'archive',
        'title': 'The HC/PUNK Demo Tapes Archives: Declino Vs Negazione',
        'description': 'Detailed article about the legendary 1984 split tape with Negazione, including history and reviews',
    },
    {
        'url': 'https://agipunkrecords.bandcamp.com/album/ag26-declino-82-85-come-una-promessa',
        'link_type': 'purchase',
        'title': 'AG26 // DECLINO - "82-85 Come Una Promessa" | Agipunk Records',
        'description': 'Jan 26, 2020. Vinyl reissue of the \'82 demotape. Includes split Negazione tracks, unreleased material, Eresia 12" (side A), 7" tracks',
    },
    {
        'url': 'https://discordanthemispheres.bandcamp.com/album/declino',
        'link_type': 'purchase',
        'title': 'Declino | Discordant Hemispheres',
        'description': 'Nov 2, 2018. Digital discography compilation. Includes unlimited streaming via Bandcamp app, plus MP3, FLAC downloads',
    },
    {
        'url': 'https://www.punkdownload.com/band.php?name=declino',
        'link_type': 'other',
        'title': 'Declino - PunkDownload.com',
        'description': 'Entry in the largest free underground punk archive (7,906 albums, 97,036 songs, 3,483 bands)',
    },
    {
        'url': 'https://www.anarcho-punk.net/band/?band=declino',
        'link_type': 'other',
        'title': 'Declino - Anarcho-punk.net',
        'description': 'Hardcore Punk band profile. Formed in 1982 in Torino, Italy',
    },
    {
        'url': 'https://www.musik-sammler.de/artist/declino/',
        'link_type': 'archive',
        'title': 'Declino - Musik-Sammler.de',
        'description': 'German collector site with discography and release details for Mucchio Selvaggio',
    },
    {
        'url': 'https://www.facebook.com/hardcorepunkblog/photos/declino-terra-bruciata-discografia-completa-2xlphardcore-punk-band-from-torino-i/1273478974788280/',
        'link_type': 'social',
        'title': 'Facebook: Declino Terra Bruciata - Discografia Completa 2xLP',
        'description': 'Jun 18, 2025. Hardcore Punk blog photo post about the Area Pirata discography release',
    },
]

try:
    band = Band.objects.get(pk=BAND_ID)
    print(f"Target: {band.name} (ID={band.id})")
    print(f"City: {band.city}")
    print(f"Active: {band.active_years}")
    
    # Get existing URLs to avoid duplicates
    existing_urls = set(Link.objects.filter(band=band).values_list('url', flat=True))
    print(f"Existing links: {len(existing_urls)}")
    
    for link_data in new_links:
        url = link_data['url']
        if url in existing_urls:
            print(f"  SKIP (already exists): {url}")
            continue
        
        try:
            link = Link.objects.create(
                band=band,
                url=url,
                link_type=link_data['link_type'],
                title=link_data['title'],
                description=link_data['description'],
            )
            added.append(url)
            print(f"  ADDED [{link.link_type}]: {url}")
        except Exception as e:
            errors.append(f"{url}: {e}")
            print(f"  ERROR: {url} -> {e}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Added: {len(added)}")
    print(f"Errors: {len(errors)}")
    if errors:
        for e in errors:
            print(f"  ! {e}")
    
    # Show all links now
    all_links = Link.objects.filter(band=band)
    print(f"\n=== ALL LINKS FOR {band.name} ({all_links.count()}) ===")
    for l in all_links:
        print(f"  [{l.link_type}] {l.title}")
        print(f"    {l.url}")
    
except Band.DoesNotExist:
    print(f"ERROR: Band ID={BAND_ID} does not exist!")
except Exception as e:
    print(f"ERROR: {e}")
