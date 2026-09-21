import os
import sys

os.chdir('/home/ubuntu/Projects/demotape')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')

import django
django.setup()

from apps.core.models import Release, Band

negrita = Band.objects.filter(slug='negrita').first()
print(f'Negrita releases:')
for r in negrita.releases.all():
    print(f'  ID={r.id} | slug={r.slug} | {r.title} ({r.year}) - {r.format}')

# Check for empty slugs
print('\nAll releases with empty slugs:')
for r in Release.objects.filter(slug=''):
    print(f'  ID={r.id} | Band: {r.band.name} | {r.title} ({r.year})')
