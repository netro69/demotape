"""Session 35 — Rock Rose (142) existing links."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Link

for bid in [142]:
    b = Band.objects.get(id=bid)
    print(f"===== {b.name} (id {b.id}) links:")
    for l in b.links.all():
        print(f"  [{l.link_type}] {l.title[:55]} | {l.url}")
