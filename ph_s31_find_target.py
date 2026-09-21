"""Session 31 — find target: most under-researched Italian band, 1985-2000 era."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

import re
from apps.core.models import Band, Link
from django.db.models import Count

qs = Band.objects.filter(status="published").annotate(n=Count("links", distinct=True)).order_by("n")
print("=== Published bands formed 1985-2000, by link count (lowest first) ===")
count = 0
for b in qs:
    ay = (b.active_years or "").strip()
    m = re.match(r"^(\d{4})", ay)
    start = int(m.group(1)) if m else None
    if start and 1985 <= start <= 2000:
        genres = ", ".join(g.name for g in b.genre_tags.all()[:4])
        print(f"{b.id} | {b.name} | {b.city} | {ay} | links: {b.n} | {genres}")
        count += 1
        if count >= 40:
            break
