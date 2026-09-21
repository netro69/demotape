"""Session 33 — find target: most under-researched Italian band, 1985-2000 era."""
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
seen_ids = []
for b in qs:
    ay = (b.active_years or "").strip()
    m = re.match(r"(\d{4})", ay)
    if not m:
        continue
    y = int(m.group(1))
    if not (1985 <= y <= 2000):
        continue
    count += 1
    seen_ids.append(b.id)
    if count <= 40:
        gt = ", ".join(t.name for t in b.genre_tags.all())[:50] if b.genre_tags.exists() else "-"
        print(f"{b.n:3d} links | id={b.id:4d} | {b.name:35s} | {b.city or '-':20s} | {ay:12s} | {gt}")
print(f"\nTotal: {count} bands")
print("IDS:" + ",".join(str(i) for i in seen_ids))
