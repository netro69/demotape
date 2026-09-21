import os, sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from django.db.models import Count, Q
from apps.core.models import Band

bands = Band.objects.annotate(link_count=Count('links')).order_by('link_count')

# Find Italian bands (have a city in Italy) with 0 links and active years in 85-00 range
italian_cities = ['Varese','Milan','Bologna','Rome','Turin','Torino','Firenze','Brescia',
                  'Cuneo','Pordenone','Arezzo','Monza','Parabiago','Sassuolo','Emilia',
                  'Lucca','Toscolano-Maderno','Venegono Superiore','Stresa','Novara',
                  'Venezia','Luvinate','Varese (Luvinate)','Milano']

# First, let's look at all 0-link bands in detail
print("=== BANDS WITH 0 LINKS ===")
for b in bands.filter(link_count=0):
    print(f"ID:{b.id} | {b.name} | city:{b.city} | active:{b.active_years} | bio:{b.bio[:100] if b.bio else ''}")

print()
print("=== BANDS WITH 0-1 LINKS, ITALIAN, 1985-2000 ===")
for b in bands.filter(link_count__lte=1):
    city = b.city or ''
    active = b.active_years or ''
    # Check if has Italian-looking city
    is_italian = any(c.lower() in city.lower() for c in italian_cities) if city else False
    # Check if active in 85-00
    has_85_00 = any(y in active for y in ['198','199','2000'])
    if is_italian or has_85_00:
        print(f"ID:{b.id} | links:{b.link_count} | {b.name:<35} | city:<{city:<25} | active:{active}")
