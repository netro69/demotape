# Created-by: agent | Date: 2026-09-16
# Session: automated
1|from apps.core.models import Band

print("=== ALL BANDS ===")
for b in Band.objects.all().order_by('id'):
    print(f'{b.id:3d} | {b.name:30s} | {b.city or "—":15s} | {b.active_years or "—":10s} | {b.status}')

print("\n=== VASCO ROSSI DETAIL ===")
b = Band.objects.get(id=96)
print(f'Name: {b.name}')
print(f'Slug: {b.slug}')
print(f'City: {b.city}')
print(f'Active Years: {b.active_years}')
print(f'Bio: {b.bio}')
print(f'Website: {b.website}')
print(f'Discogs: {b.discogs_id}')
print(f'MusicBrainz: {b.musicbrainz_id}')
print(f'Status: {b.status}')
print(f'Genre Tags: {list(b.genre_tags.all().values_list("name", flat=True))}')
print(f'Links: {list(b.links.all().values())}')
print(f'Connections From: {list(b.connections_from.all().values("to_band__name", "connection_type", "source", "notes"))}')
print(f'Connections To: {list(b.connections_to.all().values("from_band__name", "connection_type", "source", "notes"))}')
print(f'Releases: {list(b.releases.all().values("title","format","year","label","catalog_number"))}')
