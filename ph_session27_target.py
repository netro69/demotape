import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

import re
from django.db.models import Count
from apps.core.models import Band, Link

# Find most under-researched Italian bands formed 1985-2000 (fewest links)
bands = Band.objects.filter(status='published').annotate(
    link_count=Count('links', distinct=True)
)

results = []
for b in bands:
    m = re.match(r'^(\d{4})', (b.active_years or '').strip())
    if not m:
        continue
    start = int(m.group(1))
    if 1985 <= start <= 2000:
        # skip non-Italian
        country = (getattr(b, 'origin_country', '') or '')
        results.append((b.link_count, b.id, b.name, b.city, b.active_years, country))

results.sort()
print('=== Under-researched candidates (formed 1985-2000, fewest links) ===')
for r in results[:25]:
    print(f'links: {r[0]} | id {r[1]} | {r[2]} | {r[3]} | {r[4]} | country={r[5]}')
