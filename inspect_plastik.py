from apps.core.models import Band, Link, Fanzine, FanzineReview, Label, GenreTag

b = Band.objects.get(id=36)
print(f"=== PLASTIK (ID:36) ===")
print(f"City: {b.city}")
print(f"Active: {b.active_years}")
print(f"Status: {b.status}")
print(f"Bio: {b.bio[:800] if b.bio else 'None'}")
print(f"\nGenres: {[g.name for g in b.genre_tags.all()]}")

print(f"\n--- Current Links ({b.links.count()}) ---")
for link in b.links.all():
    print(f"  [{link.link_type}] {link.title or 'untitled'} -> {link.url}")

print(f"\n--- Fanzine Reviews ---")
for fr in FanzineReview.objects.filter(band=b):
    print(f"  {fr.fanzine.name} - issue: {fr.issue}, page: {fr.page}")

print(f"\n--- Releases ---")
for r in b.releases.all():
    print(f"  {r.year} - {r.title} ({r.format})")
