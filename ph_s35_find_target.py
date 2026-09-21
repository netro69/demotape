"""Session 35 — find target: most under-researched Italian band, 1985-2000 era."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link
from django.db.models import Count

qs = Band.objects.filter(status="published").annotate(n=Count("links", distinct=True)).order_by("n")
print("=== Published bands by link count (lowest first), era-filtered 1985-2000 ===")
count = 0
for b in qs:
    ay = (b.active_years or "").strip()
    # extract first 4-digit year
    import re
    m = re.search(r"(19\d{2}|20\d{2})", ay)
    start = int(m.group(1)) if m else None
    if start is None:
        continue
    if start < 1985 or start > 2000:
        continue
    print(f"{b.id}|{b.name}|{b.city}|{ay}|{b.n}|{(b.bio or '')[:70].replace(chr(10), ' ')}")
    count += 1
    if count >= 35:
        break
