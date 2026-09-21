import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()
from apps.core.models import Band
from django.db.models import Count, Q

# Find most under-researched Italian bands (1985-2000 era)
# Exclude flagged and ghost-records
bands = Band.objects.exclude(status='flagged').exclude(slug='ghost-records').annotate(
    link_count=Count('links')
).filter(
    # Italian bands in 1985-2000 window
    Q(active_years__icontains='198') | Q(active_years__icontains='199') | Q(active_years__icontains='2000'),
    link_count__lt=20  # Under-researched threshold
).order_by('link_count')[:10]

for b in bands:
    print(f'{b.id:3d} | {b.name:30s} | links={b.link_count:2d} | active={b.active_years} | city={b.city} | status={b.status}')
