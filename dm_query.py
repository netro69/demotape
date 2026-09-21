import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

from django.db.models import Count, Q
from apps.core.models import Band, Link

# Find most under-researched Italian bands (1985-2000)
bands = Band.objects.filter(
    status='published'
).exclude(
    slug__in=['ghost-records']
).annotate(
    link_count=Count('links')
).order_by('link_count', '-id')[:30]

for b in bands:
    print(f'{b.name} | links: {b.link_count} | years: {b.active_years} | city: {b.city} | bio: {(b.bio or "")[:80]}')
