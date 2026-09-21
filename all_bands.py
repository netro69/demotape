from apps.core.models import Band, Link
from django.db.models import Count

# All published bands with link counts
bands = Band.objects.filter(
    status='published'
).annotate(
    link_count=Count('links')
).order_by('link_count')

era_bands = []
for b in bands:
    years = b.active_years or ''
    # Check if band fits 1985-2000 era
    if any(x in years for x in ['1985', '1986', '1987', '1988', '1989', '199', '2000']):
        # Check if band has Italian city or is Italian
        city = str(b.city) if b.city else ''
        # Simple heuristic - all bands in DB are Italian except where noted
        era_bands.append((b.id, b.name, city, b.active_years, b.link_count))

# Sort by link count
era_bands.sort(key=lambda x: x[4])

print(f"=== ALL PUBLISHED ITALIAN BANDS (1985-2000) sorted by link count ===")
for b in era_bands:
    print(f"ID:{b[0]} | {b[1]:<30} | {b[2]:<30} | {b[3]:<20} | links={b[4]}")
