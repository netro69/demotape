from apps.core.models import Band, Link
# Check Porno Riviste + related bands presence
for nm in ['Porno Riviste', 'Porno', 'Derozer', 'Persiana Jones', 'Ska-P', 'Modena City Ramblers', 'Lo Stato Sociale', 'Giancane', 'I Ministri', 'Subsonica', 'Tre Allegri', 'Skiantos', '99 Posse', 'Africa United', 'Bluebeaters', 'Flaco']:
    qs = Band.objects.filter(name__icontains=nm)
    if qs.exists():
        for b in qs:
            print(f'EXISTS: id={b.id} | {b.name} | {b.city} | {b.active_years} | {b.status}')
    else:
        print(f'absent: {nm}')
