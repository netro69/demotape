import os, sys
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
import django
django.setup()
from django.db.models import Count, Q
from apps.core.models import Band

bands = Band.objects.annotate(link_count=Count('links')).order_by('link_count')

# Cities/keywords that suggest Italian origin
italian_cities = ['Varese','Milan','Bologna','Rome','Turin','Torino','Firenze','Brescia',
                  'Cuneo','Pordenone','Arezzo','Monza','Parabiago','Sassuolo','Emilia',
                  'Lucca','Toscolano-Maderno','Venegono','Stresa','Novara','Venezia',
                  'Luvinate','Milano','Padova','Napoli','Catania','Genoa','Trieste',
                  'Como','Lecco','Bergamo','Reggio','Verona','Vicenza','Treviso']

# Look at all bands - print those that have some link count but are clearly Italian and 85-00
print("=== ALL ITALIAN BANDS WITH <=5 LINKS, 1985-2000 ===")
for b in bands.filter(link_count__lte=5):
    city = b.city or ''
    active = b.active_years or ''
    bio = b.bio or ''
    
    # Skip non-italian bios
    if 'NOT ITALIAN UNDERGROUND' in bio or 'Modern' in bio:
        continue
    
    # Check if Italian
    is_italian = False
    if city:
        for c in italian_cities:
            if c.lower() in city.lower():
                is_italian = True
                break
    # If city is empty, check bio for Italian keywords
    if not city:
        if any(k in bio.lower() for k in ['ital','milano','varese','bologna','rome','italy','italiana']):
            is_italian = True
    
    # Check 1985-2000 era
    has_era = any(y in active for y in ['1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000'])
    
    if is_italian and has_era:
        print(f"ID:{b.id:>3} | links:{b.link_count} | {b.name:<35} | {city:<25} | {active}")
        if bio:
            print(f"     bio: {bio[:200]}")
