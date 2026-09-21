# Created-by: agent | Date: 2026-09-16
# Session: automated
1|from apps.core.models import Band, Label, Link, BandConnection, Release

# Get existing data
vasco = Band.objects.get(id=96)
rockgalileo = Band.objects.get(id=86)

print(f"=== Vasco Rossi (id={vasco.id}) ===")
print(f"Name: {vasco.name}")
print(f"Bio: {vasco.bio}")
print(f"Status: {vasco.status}")

print(f"\n=== RockGalileo (id={rockgalileo.id}) ===")
print(f"Name: {rockgalileo.name}")
print(f"City: {rockgalileo.city}")
print(f"Active Years: {rockgalileo.active_years}")
print(f"Bio: {rockgalileo.bio[:500]}")
print(f"Genre Tags: {list(rockgalileo.genre_tags.all().values_list('name', flat=True))}")
print(f"Links: {list(rockgalileo.links.all().values())}")
print(f"Releases: {list(rockgalileo.releases.all().values('title','format','year','label','catalog_number'))}")

print("\n=== All Labels ===")
for lab in Label.objects.all().order_by('id'):
    print(f'{lab.id:3d} | {lab.name:30s} | {lab.city or "—":15s} | {lab.status}')
