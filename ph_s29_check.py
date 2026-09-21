import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

from apps.core.models import Band, Link, Fanzine, FanzineReview
from django.db.models import Count

# 1. Recent links (check for unlogged additions from sessions 27/28)
print('=== Link model fields ===')
for f in Link._meta.get_fields():
    print(' ', f.name, f.get_internal_type())

print()
print('=== Bands with recent link counts (top candidates) ===')
for bid in [47, 42, 26, 11, 20, 41, 12]:
    b = Band.objects.get(id=bid)
    n = b.links.count()
    print(f'id {bid}: {b.name} — {n} links')

print()
print('=== Last 30 links in DB (by id) ===')
for l in Link.objects.order_by('-id')[:30]:
    print(f'[{l.id}] band={l.band_id} | {l.link_type} | {str(l.title)[:60]} | {l.url[:80]}')

print()
print('=== Fanzines (last 10) ===')
for fz in Fanzine.objects.order_by('-id')[:10]:
    print(f'[{fz.id}] {fz.name}')
print('Total fanzines:', Fanzine.objects.count())
print('Total fanzine reviews:', FanzineReview.objects.count())
