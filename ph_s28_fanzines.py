import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

from apps.core.models import Band, Link, Fanzine, FanzineReview

print('=== EXISTING FANZINES ===')
for f in Fanzine.objects.all():
    n = FanzineReview.objects.filter(fanzine=f).count()
    print(f'[{f.id}] {f.name} | city={f.city} | years={f.active_years} | website={f.website} | reviews={n}')

print()
print('=== MV existing link URLs (for dedupe) ===')
for l in Link.objects.filter(band_id=47):
    print(l.url)

print()
print('=== FanzineReview nullability ===')
for f in FanzineReview._meta.get_fields():
    print(f.name, f.get_internal_type(), 'null=', getattr(f, 'null', '?'))
