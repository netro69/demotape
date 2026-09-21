import os, sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Band, Link

band = Band.objects.get(id=39)
print(f"Adding links for {band.name}...")

links_to_add = [
    {
        'link_type': 'video',
        'title': 'Wishes Day (music video)',
        'url': 'https://www.youtube.com/watch?v=Bw2BLTDlOuQ',
        'description': 'Freelance Co. - Wishes Day, directed by Andrea Manenti, d.o.p. Ivan Vania'
    },
    {
        'link_type': 'archive',
        'title': 'Andrea Manenti Discogs',
        'url': 'https://www.discogs.com/fr/artist/5189599-Andrea-Manenti',
        'description': 'Singer and multi-instrumentalist from Varese, Italy. Includes Freelance Co. releases.'
    },
    {
        'link_type': 'archive',
        'title': 'Downlouders Discogs',
        'url': 'https://www.discogs.com/artist/5189602-Downlouders',
        'description': 'Downlouders - Varese psychedelic collective founded 2008 by Andrea Manenti. Albums: Arca (2016), Terra Session, The Void.'
    },
    {
        'link_type': 'streaming',
        'title': 'Andrea Scream Manenti SoundCloud',
        'url': 'https://soundcloud.com/andrea-scream-manenti',
        'description': 'Andrea Manenti solo/side project SoundCloud page'
    },
    {
        'link_type': 'social',
        'title': 'Andrea Manenti TikTok',
        'url': 'https://www.tiktok.com/@andrea.manenti',
        'description': 'Andrea Manenti TikTok - original music content'
    },
    {
        'link_type': 'video',
        'title': 'Andrea Manenti YouTube',
        'url': 'https://www.youtube.com/@andreamanenti',
        'description': 'Andrea Manenti YouTube channel - director and musician'
    },
    {
        'link_type': 'archive',
        'title': 'Le Madri Degli Orfani Discogs',
        'url': 'https://www.discogs.com/Le-Madri-Degli-Orfani-Anni-Dieci-Un-Nuovo-Mondo/release/18450049',
        'description': 'Le Madri Degli Orfani - Andrea Manenti (2) on vocals/guitar. Release: Anni Dieci / Un Nuovo Mondo.'
    },
    {
        'link_type': 'archive',
        'title': 'Ghost Records Discogs (label)',
        'url': 'https://www.discogs.com/label/25770-Ghost-Records',
        'description': 'Italian label formed 2002 in Varese. Roster includes Bartòk, Fiel Garvie, Freelance Co. (founders), and many others. First release: Ghost Town: 13 Songs from the Lakes County (2002).'
    },
    {
        'link_type': 'archive',
        'title': 'Ghost Records complete discography',
        'url': 'https://www.discogs.com/de/label/25770-Ghost-Records',
        'description': 'Full Ghost Records releases list: Bartòk, Fiel Garvie, Santo, Andrea Fornari, Il Triangolo, Birø, ≈ Belize ≈, etc.'
    },
    {
        'link_type': 'archive',
        'title': 'Downlouders ProgArchives',
        'url': 'https://www.progarchives.com/artist.asp?id=9822',
        'description': 'Downlouders biography - Varese psychedelic collective founded 2008 by Andrea Manenti'
    },
    {
        'link_type': 'archive',
        'title': 'Downlouders RateYourMusic',
        'url': 'https://rateyourmusic.com/artist/downlouders',
        'description': 'Downlouders discography on RateYourMusic - genres: Psychedelic Rock'
    },
    {
        'link_type': 'archive',
        'title': 'Andrea Manenti website',
        'url': 'https://andreamanenti.net/',
        'description': 'Andrea Manenti official website'
    },
]

added = 0
for link_data in links_to_add:
    # Check if URL already exists
    existing = Link.objects.filter(band=band, url=link_data['url']).exists()
    if existing:
        print(f"  SKIP (exists): {link_data['url'][:60]}")
        continue
    
    Link.objects.create(band=band, **link_data)
    print(f"  ADDED: [{link_data['link_type']}] {link_data['title']}")
    added += 1

print(f"\nDone. Added {added} new links.")
