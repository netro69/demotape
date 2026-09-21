import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

from apps.core.models import Band, Link, Fanzine, FanzineReview, Release, BandConnection

b = Band.objects.get(id=47)
print('=== BAND DETAIL ===')
for f in ['id', 'name', 'city', 'active_years', 'genre', 'members', 'bio', 'status']:
    print(f'{f}: {getattr(b, f, None)}')
print()
print('=== RELEASES ===')
for r in getattr(b, 'releases', None).all() if hasattr(b, 'releases') else []:
    print(vars(r))
print()
print('=== EXISTING LINKS ===')
for l in b.links.all():
    print(f'[{l.id}] {l.link_type} | {l.title} | {l.url}')
print()
print('=== LINK MODEL FIELDS ===')
for f in Link._meta.get_fields():
    print(f.name, f.get_internal_type())
print()
print('=== FANZINE MODEL FIELDS ===')
for f in Fanzine._meta.get_fields():
    print(f.name, f.get_internal_type())
print()
print('=== FANZINEREVIEW MODEL FIELDS ===')
for f in FanzineReview._meta.get_fields():
    print(f.name, f.get_internal_type())
print()
print('=== CONNECTIONS involving band ===')
try:
    for c in BandConnection.objects.filter(band=b):
        print(vars(c))
except Exception as e:
    print('conn err', e)
