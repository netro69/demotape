from apps.core.models import Fanzine, Label, GenreTag

print('=== EXISTING FANZINES ===')
for f in Fanzine.objects.all().order_by('name'):
    print(f'id={f.id:3d} | {f.name[:35]:35s} | {f.city[:15]:15s} | {str(f.active_years)[:20]:20s} | {f.slug}')

print()
print('=== EXISTING LABELS (matching punkreas-related names) ===')
names = ['tvo', 'atomo', 'discopi', 'udp', 'canapa', 'upr', 'latomo', 'rude', 'garrincha', 'edel', 'virgin', 'universal']
for l in Label.objects.all().order_by('name'):
    nl = l.name.lower()
    if any(n in nl for n in names):
        print(f'id={l.id:3d} | {l.name[:35]:35s} | {l.city[:15]:15s} | founded={l.founded_year} | {l.slug}')

print()
print('=== GENRE TAGS (punk-related) ===')
for g in GenreTag.objects.all().order_by('name'):
    if any(k in g.name.lower() for k in ['punk', 'ska', 'hardcore', 'rock']):
        print(f'id={g.id:3d} | {g.name:25s} | {g.slug}')

print()
print('=== ALL LABELS count ===', Label.objects.count())
print('=== Punkreas connections detail ===')
from apps.core.models import BandConnection, Band
b = Band.objects.get(id=18)
for c in BandConnection.objects.filter(from_band=b) | BandConnection.objects.filter(to_band=b):
    print(f'{c.from_band.name} -> {c.to_band.name} | {c.connection_type} | source={c.source} | notes={str(c.notes)[:80]}')
