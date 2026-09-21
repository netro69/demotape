"""Find most under-researched Italian bands formed 1985-2000 (fewest links)."""
import re
from django.db.models import Count
from apps.core.models import Band


def run():
    bands = Band.objects.filter(status='published').annotate(
        link_count=Count('links', distinct=True)
    ).order_by('link_count')

    results = []
    for b in bands:
        m = re.match(r'^(\d{4})', (b.active_years or '').strip())
        if not m:
            continue
        start = int(m.group(1))
        if 1985 <= start <= 2000:
            results.append((b.link_count, b.id, b.name, b.city, b.active_years))

    results.sort()
    for r in results[:20]:
        print(f'links: {r[0]} | id {r[1]} | {r[2]} | {r[3]} | {r[4]}')
