import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

import re
from apps.core.models import Band
from django.db.models import Count

# All published bands with link counts, INCLUDING blank active_years
bands = Band.objects.filter(status='published').annotate(
    link_count=Count('links', distinct=True)
)

print('=== ALL published bands sorted by links (with era parse) ===')
rows = []
for b in bands:
    m = re.match(r'^(\d{4})', (b.active_years or '').strip())
    start = int(m.group(1)) if m else None
    rows.append((b.link_count, b.id, b.name, b.city, b.active_years, start))
rows.sort()
for r in rows:
    print(f'links:{r[0]:3d} | id {r[1]:3d} | start={r[5]} | {r[2][:28]:28s} | {str(r[3])[:22]:22s} | {r[4]}')
