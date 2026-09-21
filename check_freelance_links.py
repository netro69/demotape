import os, sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from apps.core.models import Band, Link

# Check existing links for Freelance Co. (ID 39)
band = Band.objects.get(id=39)
print(f"Band: {band.name} (ID:{band.id})")
print(f"City: {band.city}")
print(f"Active: {band.active_years}")
print(f"Bio: {band.bio[:300] if band.bio else ''}")
print()
print("=== EXISTING LINKS ===")
for link in band.links.all():
    print(f"  [{link.link_type}] {link.title or '(no title)'}: {link.url}")
