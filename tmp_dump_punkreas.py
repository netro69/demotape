# Dump current Punkreas DB state (id 18)
from apps.core.models import Band, Link, Release, FanzineReview, BandConnection, GenreTag

b = Band.objects.get(id=18)
print('=== BAND ===')
print('name:', b.name)
print('slug:', b.slug)
print('city:', b.city)
print('active_years:', b.active_years)
print('status:', b.status)
print('bio:', (b.bio or '')[:600])
print('website:', b.website)
print('discogs_id:', b.discogs_id)
print('musicbrainz_id:', b.musicbrainz_id)
print('genres:', [g.name for g in b.genre_tags.all()])
print('label ids via releases:', set(r.label for r in b.releases.all() if r.label))

print()
print('=== LINKS (18) ===')
for l in b.links.all().order_by('link_type', 'url'):
    print(f'[{l.link_type:9s}] {l.url}  | {str(l.title)[:60]}')

print()
print('=== RELEASES ===')
for r in b.releases.all().order_by('year'):
    print(f'{r.year} | {r.title} | label={r.label} | fmt={r.format} | cat={r.catalog_number}')

print()
print('=== CONNECTIONS ===')
for c in b.connections_from.all():
    print(f'-> {c.to_band.name} ({c.connection_type}) {str(c.notes)[:50]}')
for c in b.connections_to.all():
    print(f'<- {c.from_band.name} ({c.connection_type}) {str(c.notes)[:50]}')

print()
print('=== FANZINE REVIEWS ===')
for fr in b.fanzine_reviews.all():
    print(f'{fr.fanzine.name} | {fr.year} | {str(fr.content)[:60]}')

print()
print('=== Release model fields ===')
print([f.name for f in Release._meta.fields if f.name in ('title','year','label','catalog_number','format','slug','band')])
print('=== Link model fields ===')
print([f.name for f in Link._meta.fields])
print('=== Fanzine model fields ===')
print([f.name for f in Fanzine._meta.fields])
print('=== FanzineReview model fields ===')
print([f.name for f in FanzineReview._meta.fields])
