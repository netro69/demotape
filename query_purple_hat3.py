import os, sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from django.db.models import Count
from apps.core.models import Band

bands = Band.objects.annotate(link_count=Count('links')).order_by('link_count')

# Italian cities
italian_cities = ['Varese','Milan','Bologna','Rome','Turin','Torino','Firenze','Brescia',
                  'Cuneo','Pordenone','Arezzo','Monza','Parabiago','Sassuolo','Emilia',
                  'Lucca','Toscolano-Maderno','Venegono','Stresa','Novara','Venezia',
                  'Luvinate','Milano','Padova','Napoli','Catania','Genoa','Trieste',
                  'Como','Lecco','Bergamo','Reggio','Verona','Vicenza','Treviso']

print("=== ALL ITALIAN BANDS WITH <=5 LINKS ===")
print("ID  | Links | Name                              | City          | Active Years")
print("-" * 110)
for b in bands.filter(link_count__lte=5):
    city = b.city or ''
    active = b.active_years or ''
    bio = b.bio or ''
    
    # Skip non-italian
    if 'NOT ITALIAN UNDERGROUND' in bio or 'Modern' in bio:
        continue
    
    # Check Italian
    is_italian = False
    if city:
        for c in italian_cities:
            if c.lower() in city.lower():
                is_italian = True
                break
    if not city:
        if any(k in bio.lower() for k in ['ital','milano','varese','bologna','rome','italy','italiana']):
            is_italian = True
    
    if not is_italian:
        continue
    
    # Check if active years touch 1985-2000
    has_era = False
    for year in range(1985, 2001):
        if str(year) in active:
            has_era = True
            break
    
    # Also check for ranges like "1980s"
    if not has_era:
        if '1980' in active or '1990' in active:
            has_era = True
    
    marker = '***' if has_era else '   '
    print(f"{marker} {b.id:>3} | {b.link_count:>5} | {b.name:<35} | {city:<15} | {active}")
    if has_era and bio:
        short_bio = bio[:150].replace('\n',' ')
        print(f"      BIO: {short_bio}")
