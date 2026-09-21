#!/usr/bin/env python
"""Add found underground research links to Linea 77 (ID=67) in the Demotape database."""
import os
import sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Band, Link, Release

BAND_ID = 67
added = []
errors = []

# Define the new links we found
new_links = [
    # Streaming / Music
    {
        'url': 'https://music.apple.com/us/artist/linea-77/42258194',
        'link_type': 'streaming',
        'title': 'Linea 77 - Apple Music',
        'description': 'Full discography available. 8 studio albums + EPs. Probably the first Italian band to become famous abroad before getting known at home.',
    },
    {
        'url': 'https://www.last.fm/music/Linea+77',
        'link_type': 'streaming',
        'title': 'Linea 77 - Last.fm',
        'description': 'Artist page with scrobble stats, discography, and listening data.',
    },
    {
        'url': 'https://www.deezer.com/artist/3674',
        'link_type': 'streaming',
        'title': 'Linea 77 - Deezer',
        'description': 'Full catalog available for streaming.',
    },
    {
        'url': 'https://linea-77.bandcamp.com/',
        'link_type': 'purchase',
        'title': 'Linea 77 - Bandcamp',
        'description': 'Official Bandcamp. All albums: Too Much Happiness..., Ketchup Suicide, Numb, Available for Propaganda, Venareal 1995, Horror Vacui, 10, Oh! Live albums available.',
    },
    # Archive / Discography
    {
        'url': 'https://www.discogs.com/artist/309369-Linea-77',
        'link_type': 'archive',
        'title': 'Linea 77 - Discogs Artist Page',
        'description': 'Complete discography: 19 albums, 9 singles & EPs, 8 videos, 17 credits. Demo tapes: Ogni Cosa Al Suo Posto (1995), Kung Fu (1997). All studio albums documented.',
    },
    {
        'url': 'https://musicbrainz.org/artist/7798b273-e3fb-465e-9fdf-6bd7850a6d81',
        'link_type': 'archive',
        'title': 'Linea 77 - MusicBrainz',
        'description': 'Artist ID: 7798b273-e3fb-465e-9fdf-6bd7850a6d81. Founded Venaria Reale 1993. Tags: nu metal, alternative metal, rap rock.',
    },
    {
        'url': 'https://www.allmusic.com/artist/linea-77-mn0000242776',
        'link_type': 'archive',
        'title': 'Linea 77 - AllMusic',
        'description': 'Full biography + discography + expert reviews. "Probably the first Italian band to become famous abroad before getting known at home."',
    },
    {
        'url': 'https://rateyourmusic.com/artist/linea-77',
        'link_type': 'archive',
        'title': 'Linea 77 - Rate Your Music',
        'description': 'Community-rated discography. Albums: Too Much Happiness..., Ketchup Suicide, Numb, Available for Propaganda, Venareal 1995, Horror Vacui, 10, Oh!',
    },
    {
        'url': 'https://www.wikidata.org/wiki/Q1826403',
        'link_type': 'archive',
        'title': 'Linea 77 - Wikidata',
        'description': 'Q1826403. Italian nu metal band, formed 1993 in Turin.',
    },
    # Video / YouTube
    {
        'url': 'https://www.youtube.com/@Linea77',
        'link_type': 'video',
        'title': 'Linea 77 - Official YouTube Channel',
        'description': 'Official channel with music videos and live performances.',
    },
    {
        'url': 'https://www.youtube.com/watch?v=R5W5X_tkxmc',
        'link_type': 'video',
        'title': 'Linea 77 - Walk Like an Egyptian (Cover)',
        'description': 'Cover of Bangles song from Ketchup Suicide (2001).',
    },
    {
        'url': 'https://music.youtube.com/playlist?list=OLAK5uy_ny45bzcvCWOlyXJ1EJzWHyAGc3GEMtyxU',
        'link_type': 'video',
        'title': 'Available for Propaganda - Full Album (YouTube Music)',
        'description': 'Complete 4th album (2005) with Inno all odio (FIFA 06 soundtrack).',
    },
    # Article / Interview
    {
        'url': 'https://www.rollingstone.it/musica/linea-77-torino-e-addormentata-lhip-hop-e-omologato/480003/',
        'link_type': 'archive',
        'title': 'Linea 77: Torino è addormentata - Rolling Stone Italia',
        'description': '2025 interview about new EP Server Sirena (feat. Bloody Beetroots, Salmo, Ensi, Caparezza).',
    },
    {
        'url': 'https://genius.com/artists/Linea-77',
        'link_type': 'archive',
        'title': 'Linea 77 - Genius (Lyrics)',
        'description': 'Complete Italian lyrics with annotations.',
    },
    {
        'url': 'https://www.balarm.it/news/magazine/linea-77-come-suona-un-inno-all-odio-3073',
        'link_type': 'archive',
        'title': 'Linea 77: come suona un Inno all Odio - Balarm',
        'description': 'Band history and discography overview.',
    },
    {
        'url': 'https://www.antiwarsongs.org/do_search.php?lang=it&idartista=7823&stesso=1',
        'link_type': 'archive',
        'title': 'Linea 77 - Antiwar Songs (Canzoni contro la guerra)',
        'description': 'Political punk/metal database entry with band bio and demo history.',
    },
    # Purchase
    {
        'url': 'https://www.amazon.com/Venareal-1995-Linea-77/dp/B00DMWAI2I',
        'link_type': 'purchase',
        'title': 'Linea 77 - Venareal 1995 (Amazon)',
        'description': '2007 demo compilation. 10 demos from 1995 + 2 new tracks.',
    },
    {
        'url': 'https://www.amazon.com/Too-Much-Happiness-Linea-77/dp/B00DMD3A0E',
        'link_type': 'purchase',
        'title': 'Linea 77 - Too Much Happiness Makes Kids Paranoid (Amazon)',
        'description': '1998 debut album re-release on Earache Records (2000).',
    },
    {
        'url': 'https://www.amazon.it/Horror-Vacui-Linea-77/dp/B009IDOHQI',
        'link_type': 'purchase',
        'title': 'Linea 77 - Horror Vacui (Amazon IT)',
        'description': '2006 album produced by Toby Wright (Universal). First with Tiziano Ferro duet.',
    },
    # Wikipedia (IT) - NOT already in DB
    {
        'url': 'https://it.wikipedia.org/wiki/Linea_77',
        'link_type': 'archive',
        'title': 'Linea 77 - Wikipedia IT',
        'description': 'Italian Wikipedia article. Full history, discography, members, labels.',
    },
]

# Also add demo releases
new_releases = [
    {
        'title': 'Ogni cosa al suo posto',
        'release_year': 1995,
        'format': 'Cassette Demo',
        'label': 'Self-produced',
        'description': 'First demo tape. 4 tracks. Self-produced, ~500 copies sold. Reviewed positively by music press.',
        'link': 'https://it.wikipedia.org/wiki/Linea_77',
    },
    {
        'title': 'Kung Fu',
        'release_year': 1997,
        'format': 'Cassette Demo',
        'label': 'Dracma Records',
        'description': 'Second demo tape. Released via Turin label Dracma Records. Contains re-recorded tracks from first demo.',
        'link': 'https://it.wikipedia.org/wiki/Linea_77',
    },
]

try:
    band = Band.objects.get(pk=BAND_ID)
    print(f"Target: {band.name} (ID={band.id})")
    print(f"City: {band.city}")
    print(f"Active: {band.active_years}")
    
    # Update MusicBrainz and Discogs IDs if missing
    if not band.discogs_id:
        band.discogs_id = '309369'
        print(f"Updated Discogs ID: {band.discogs_id}")
    if not band.musicbrainz_id:
        band.musicbrainz_id = '7798b273-e3fb-465e-9fdf-6bd7850a6d81'
        print(f"Updated MusicBrainz ID: {band.musicbrainz_id}")
    band.save()
    
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
    
    # Add demo releases
    for rel_data in new_releases:
        # Check if release already exists
        existing = Release.objects.filter(
            band=band, 
            title=rel_data['title'],
            release_year=rel_data['release_year']
        ).exists()
        if existing:
            print(f"  SKIP release (already exists): {rel_data['title']} ({rel_data['release_year']})")
            continue
        
        try:
            Release.objects.create(
                band=band,
                title=rel_data['title'],
                release_year=rel_data['release_year'],
                format=rel_data['format'],
                label=rel_data['label'],
                description=rel_data['description'],
            )
            print(f"  ADDED Release: {rel_data['title']} ({rel_data['release_year']})")
        except Exception as e:
            print(f"  ERROR adding release {rel_data['title']}: {e}")
    
    # Update bio
    new_bio = """Italian nu metal / alternative metal / funk metal band from Venaria Reale (Turin), Piedmont. Formed in 1993.

Name origin: The number of the bus the band members used to take to reach their rehearsal room.

Members: Nitto (Nicola Sangermano, vocals), Chinaski (Paolo Pavanello, guitar), Dade (Davide Pavanello, bass/vocals/synthesizer), Tozzo (Christian Montanarella, drums). All four are founding members. In 2012, Paolo (Paolo Paganelli, guitar) and Maggio (Fabio Zompa, bass) joined when Dade moved to synthesizer-only.

History: Started as a cover band playing Rage Against the Machine and CCCP Fedeli alla linea. First demo Ogni cosa al suo posto (July 1995, self-produced, ~500 copies). Second demo Kung Fu (1997, Dracma Records). Debut album Too Much Happiness Makes Kids Paranoid (1998, Collapse Records Milan). Re-released by Earache Records in 2000, which signed the band. Sophomore Ketchup Suicide (2001) featured a cover of "Walk Like an Egyptian." Numb (2003) was the breakthrough, with "Fantasma" (first Italian-language single) and "66 (Diabulus in Musica)" (feat. Subsonica). Available for Propaganda (2005, Earache) featured "Inno all'odio" on the FIFA 06 soundtrack. Venareal 1995 (2007) compiled old demos. Horror Vacui (2008) was their first album with Universal Music, produced by Toby Wright, featuring "Sogni Risplendono" (feat. Tiziano Ferro).

Labels: Earache Records (2000-2007), Universal Records (2008-2011), self-released since 2012.

Notable: Probably the first Italian band to become famous abroad before getting known at home. First Italian band to play Reading and Leeds festivals (2001). Influences: Deftones, Rage Against the Machine, Helmet.

Associated acts: Subsonica, CCCP Fedeli alla linea, Max Cavalera (Soulfly), Sepultura, Tiziano Ferro."""
    
    band.bio = new_bio
    band.save()
    print(f"\nUpdated bio for {band.name}")
    
    print(f"\n=== SUMMARY ===")
    print(f"New links added: {len(added)}")
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
    import traceback
    traceback.print_exc()
