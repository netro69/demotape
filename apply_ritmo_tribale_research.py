#!/usr/bin/env python3
"""Apply Ritmo Tribale research findings to the Demotape DB."""

import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, FanzineReview, Fanzine

band = Band.objects.get(id=75)
print(f"Applying research to: {band.name}")

# === UPDATE BIO ===
new_bio = """Ritmo Tribale sono un gruppo rock italiano formatosi a Milano nel 1984, espressione della scena underground legata al Leoncavallo e ai centri sociali. La band è stata una delle formazioni alt-rock italiane più dirompenti, tra vocazione hard-rock/hardcore e atteggiamento barricadiero e anarchico.

Formazione originale: Fabrizio "Fabri" Rioda, Alessandro "Zero" Zerilli, Stefano "Edda" Rampoldi, Andrea Scaglia, Alex Marcheschi. Successivamente si aggiungono Andrea "Briegel" Filippazzi (basso) e Luca Talia Accardi (tastiere).

L'esordio avviene nel 1987 con uno split in cassetta con i F:A:R. allegato alla fanzine Amen This Is Religgion, legata allo spazio autogestito Virus di via Correggio. Il primo disco, A bocca chiusa (1988, Radio Base 81), è un esercizio di hardcore-energetica. Con Kriminale (1989, Vox Pop) la band trova un equilibrio tra hard rock, punk e metal, ottenendo una recensione positiva su Maximum Rock'n'Roll e suonando a New York nel New Music Seminar.

Il sound evolve verso il crossover con l'EP Ritmo Tribale (1991) e Tutti vs. tutti (1992), avvicinandosi a black wave e funk. Con Mantra (1994, Black Out) diventano un nome di punta del rock italiano, con il videoclip di "Sogna" girato a Cuba. Psycorsonica (1995, Mercury) è considerato l'opera di maturità, con il singolo "Universo".

Nel 1996 Edda lascia la band per problemi di droga e si ritira dalle scene per 12 anni. Senza di lui, la band pubblica Bahamas (1999, Edel) che non ottiene i favori della critica. Nel 2000 il gruppo si scioglie.

Nel 2007 reunion eccezionale al Fillmore di Piacenza con la pubblicazione di Uomini 1988-2000. Nel 2009 i membri (tranne Rioda) formano NoGuru con Xabier Iriondo (ex-Afterhours). Edda inizia la carriera solista nel 2009 con "Sempre Biot".

Il 2017 vede un concerto-evento al Centrale Rock Pub di Erba con la formazione storica. Nel 2020 esce La Rivoluzione del Giorno Prima, con un doppio articolo su Rockerilla (Luglio/Agosto 2020).

Il loro sound ha ispirato molti artisti italiani, tra cui Afterhours e Negrita. La band è stata definita "grunge in tempi non sospetti" per la capacità di unire Hüsker Du e rock tamarro di matrice italica."""

band.bio = new_bio
band.save()
print("✅ Bio updated")

# === ADD NEW LINKS ===
new_links = [
    # Streaming
    ('streaming', 'Spotify', 'https://open.spotify.com/artist/7FWTKsIrRo9hVTB4wAjH1h', ''),
    ('streaming', 'Apple Music', 'https://music.apple.com/gb/artist/ritmo-tribale/26377658', ''),
    ('streaming', 'Deezer', 'https://www.deezer.com/en/artist/149219', ''),
    ('streaming', 'Shazam', 'https://www.shazam.com/artist/ritmo-tribale/26377658', ''),
    # Social
    ('social', 'Instagram', 'https://www.instagram.com/ritmotribaleofficial/', ''),
    ('social', 'Facebook', 'https://www.facebook.com/iritmotribale', ''),
    # Video
    ('video', 'YouTube: Uomini - Live Unplugged @ Segnali di fumo (1995)', 'https://www.youtube.com/watch?v=_l0syrLbCY8', 'Videomusic, primavera 1995'),
    ('video', 'YouTube: La Rivoluzione del Giorno Prima (Official Video)', 'https://www.youtube.com/watch?v=vw25ZbCy-So', ''),
    # Archive/Reference
    ('archive', 'MusicBrainz', 'https://musicbrainz.org/artist/b1770720-c600-455b-b36c-69251d480c04', ''),
    ('archive', 'Wikidata', 'https://www.wikidata.org/wiki/Q3937295', ''),
    ('archive', 'Bandcamp tag', 'https://bandcamp.com/tag/ritmo-tribale', ''),
    # Articles/Reviews
    ('article', 'Rockol: La Rivoluzione del Giorno Prima review', 'https://www.rockol.it/recensioni-musicali/album/9283/ritmo-tribale-la-rivoluzione-del-giorno-prima', ''),
    ('article', 'Rockit: La Rivoluzione del Giorno Prima review', 'https://www.rockit.it/recensione/47015/ritmotribale-la-rivoluzione-del-giorno-prima', ''),
    ('article', 'RockShock: La Rivoluzione del Giorno Prima review', 'https://www.rockshock.it/ritmo-tribale-la-recensione-di-la-rivoluzione-del-giorno-prima/', ''),
    ('article', 'Debaser: Ritmo Tribale EP review', 'https://www.debaser.it/ritmo-tribale/ritmo-tribale/recensione', ''),
    ('article', 'Rolling Stone Italia: "Uomini" book review', 'https://www.rollingstone.it/cultura/news-cultura/uomini-il-libro-su-ritmo-tribale-edda-e-la-milano-degli-anni-80-e-90/248191/', ''),
    ('article', 'L\'ultima Thule: Il Mucchio Selvaggio reprint (1988-1990)', 'https://lultimathule.wordpress.com/2017/05/19/ritmo-tribale-1988-1990/', ''),
    ('article', 'Il Raglio del Mulo: Kriminale reissue', 'https://ilragliodelmulo.com/ritmo-tribale-in-arrivo-la-ristampa-di-kriminale/', ''),
    ('article', 'Antiwar Songs: Ritmo Tribale', 'https://www.antiwarsongs.org/artista.php?id=16573&lang=it&rif=1', ''),
    # Purchase/Events
    ('purchase', 'Mailticket: Live 2025', 'https://www.mailticket.it/evento/47842/ritmo-tribale', ''),
    ('purchase', 'Unilibro: "Uomini" book', 'https://www.unilibro.it/libri/f/argomento/ritmo_tribale', ''),
]

added_links = 0
for link_type, title, url, desc in new_links:
    link, created = Link.objects.get_or_create(
        band=band,
        url=url,
        defaults={'link_type': link_type, 'title': title, 'description': desc}
    )
    if created:
        added_links += 1
        print(f"  + Link: {title}")

print(f"✅ Added {added_links} new links (total: {band.links.count()})")

# === ADD NEW CONNECTIONS ===
connections_to_add = [
    # (connected_band_name, connection_type, notes)
    ('Afterhours', 'scene_peer', 'Xabier Iriondo passed from Afterhours to NoGuru; Ritmo Tribale called "fratelli minori" of Afterhours'),
    ('Negrita', 'influence', 'Negrita influenced by Ritmo Tribale sound'),
    ('NoGuru', 'successor', 'Formed by ex-Ritmo Tribale members (Scaglia, Marcheschi, Talia, Briegel) + Xabier Iriondo'),
    ('Edda', 'shared_member', 'Stefano Rampoldi aka Edda — solo project after leaving Ritmo Tribale'),
    ('F:A.R.', 'collaboration', 'Split cassette "Allegato Sonoro" (1987) with F:A.R.'),
    ('Subsonica', 'scene_peer', 'Both part of Italian crossover/alternative scene of the 90s'),
]

added_conns = 0
for conn_band_name, conn_type, notes in connections_to_add:
    try:
        conn_band = Band.objects.get(name=conn_band_name)
        # Check if connection already exists
        exists = BandConnection.objects.filter(
            from_band=band, to_band=conn_band, connection_type=conn_type
        ).exists() or BandConnection.objects.filter(
            from_band=conn_band, to_band=band, connection_type=conn_type
        ).exists()
        if not exists:
            BandConnection.objects.create(
                from_band=band,
                to_band=conn_band,
                connection_type=conn_type,
                notes=notes
            )
            added_conns += 1
            print(f"  + Connection: {band.name} -> {conn_band_name} ({conn_type})")
    except Band.DoesNotExist:
        print(f"  ⚠️ Band not found: {conn_band_name}")

print(f"✅ Added {added_conns} new connections")

# === ADD FANZINE REVIEWS ===
# First create/get fanzines
fanzines_data = [
    ('Il Mucchio Selvaggio', 'il-mucchio-selvaggio', 'Roma', '1977-2018'),
    ('Rockerilla', 'rockerilla', 'Milano', '1978-'),
    ('Amen This Is Religgion', 'amen-this-is-religgion', 'Milano', '1980s'),
]

added_reviews = 0
for fz_name, fz_slug, fz_city, fz_years in fanzines_data:
    fz, created = Fanzine.objects.get_or_create(
        slug=fz_slug,
        defaults={'name': fz_name, 'city': fz_city, 'active_years': fz_years}
    )
    if created:
        print(f"  + Fanzine: {fz_name}")

# Add reviews
reviews_data = [
    ('Il Mucchio Selvaggio', '510', '2002', 'Recensione della raccolta Uomini 1988-2000. Articolo di Federico Guglielmi.'),
    ('Rockerilla', 'Luglio/Agosto 2020', '2020', 'Doppio articolo con intervista e recensione del nuovo album "La Rivoluzione del Giorno Prima".'),
    ('Amen This Is Religgion', '5', '1987', 'Split cassette "Allegato Sonoro" con F:A.R. allegato alla fanzine.'),
]

for fz_name, issue, year, text in reviews_data:
    try:
        fz = Fanzine.objects.get(name=fz_name)
        review, created = FanzineReview.objects.get_or_create(
            band=band,
            fanzine=fz,
            issue_number=issue,
            defaults={
                'year': int(year) if year.isdigit() else None,
                'review_text': text,
            }
        )
        if created:
            added_reviews += 1
            print(f"  + Review: {fz_name} #{issue} ({year})")
    except Fanzine.DoesNotExist:
        print(f"  ⚠️ Fanzine not found: {fz_name}")

print(f"✅ Added {added_reviews} new fanzine reviews")

# === SUMMARY ===
print(f"\n{'='*50}")
print(f"SUMMARY for {band.name}:")
print(f"  Links: {band.links.count()} (was 7)")
print(f"  Connections: {band.connections_from.count() + band.connections_to.count()} (was 2)")
print(f"  Fanzine reviews: {band.fanzine_reviews.count()} (was 0)")
print(f"  Bio: updated with detailed history")
print(f"{'='*50}")
