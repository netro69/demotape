import os
import sys

os.chdir('/home/ubuntu/Projects/demotape')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')

import django
django.setup()

from apps.core.models import Release, Band
from django.utils.text import slugify

# Fix Rock Rose empty slug first
rock_rose = Band.objects.filter(slug='rock-rose').first()
if rock_rose:
    for r in rock_rose.releases.filter(slug=''):
        new_slug = slugify(r.title)
        # Check for uniqueness
        while Release.objects.filter(slug=new_slug).exists():
            new_slug = new_slug + '-2'
        r.slug = new_slug
        r.save()
        print(f'Fixed Rock Rose release slug: {r.title} -> {new_slug}')

# Now add Negrita releases with explicit slugs
negrita = Band.objects.filter(slug='negrita').first()
if not negrita:
    negrita = Band.objects.filter(name__icontains='negrita').first()

if not negrita:
    print("Negrita not found!")
    sys.exit(1)

releases_to_add = [
    {
        'title': 'Paradisi per illusi',
        'format': 'cd',
        'year': 1995,
        'label': 'Black Out / Mercury',
        'description': 'Mini-album. Recorded partly in Salvador de Bahia, Brazil. Lead single presented live throughout Europe. Represented Italy at European Rock Festival in Turkey.',
    },
    {
        'title': 'XXX',
        'format': 'cd',
        'year': 1997,
        'label': 'Black Out / Mercury',
        'description': 'Platinum album. Recorded in USA. Collaborated with Aldo, Giovanni e Giacomo for film soundtracks (Tre uomini e una gamba, Così è la vita).',
    },
    {
        'title': 'Reset',
        'format': 'cd',
        'year': 1999,
        'label': 'Black Out / Mercury',
        'description': 'Harder rock direction. Features "Mama maé".',
    },
]

for rel_data in releases_to_add:
    existing = Release.objects.filter(band=negrita, title=rel_data['title']).first()
    if existing:
        print(f"SKIP (exists): {rel_data['title']}")
    else:
        slug = slugify(rel_data['title'])
        # Ensure uniqueness
        while Release.objects.filter(slug=slug).exists():
            slug = slug + '-2'
        
        release = Release.objects.create(
            band=negrita,
            title=rel_data['title'],
            slug=slug,
            format=rel_data['format'],
            year=rel_data['year'],
            label=rel_data['label'],
            description=rel_data['description'],
        )
        print(f"ADDED: {release.title} ({release.year}) - slug: {release.slug}")

print(f"\nTotal releases for Negrita now: {negrita.releases.count()}")
for r in negrita.releases.all():
    print(f"  {r.title} ({r.year}) - {r.format} - {r.label}")
