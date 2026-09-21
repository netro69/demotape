import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

from apps.core.models import Band, Link

# Detail on top candidates not yet covered by previous sessions
for bid in [16, 47, 86, 69, 78, 18, 112]:
    try:
        b = Band.objects.get(id=bid)
    except Band.DoesNotExist:
        print(f'--- id {bid}: NOT FOUND')
        continue
    print(f'--- id {bid}: {b.name} | {b.city} | {b.active_years} | status={b.status}')
    print(f'    bio: {(b.bio or "")[:200]}')
    for l in b.links.all():
        print(f'    [{l.link_type}] {l.title} | {l.url}')
    print()
