# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python3
"""Update C.S.I. (Consorzio Suonatori Indipendenti) band record (id=82) with research data."""
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

from django.db import connection
from django.utils.text import slugify

cursor = connection.cursor()

# === 1. Update Band ===
bio = """C.S.I. (Consorzio Suonatori Indipendenti) is an Italian band from Emilia-Romagna that evolved from CCCP Fedeli alla linea after the fall of the Berlin Wall in 1990. The name C.S.I. references both the Italian acronym for 'Consortium of Independent Players' and the CIS (Commonwealth of Independent States) that replaced the USSR.

Founded in 1992, the band brought together the 'Emilian core' (Giovanni Lindo Ferretti and Massimo Zamboni) with the 'Tuscan core' from Litfiba (Gianni Maroccolo, Francesco Magnelli) plus sound engineer Giorgio Canali. Their first collaboration was a concert at Centro Pecci in Prato on September 18, 1992 with Üstmamò and Disciplinatha, documented on the live compilation 'Maciste contro tutti' (1993).

Their debut studio album 'Ko de mondo' (1994) was recorded in a farmhouse in Brittany, France. The band released three acclaimed studio albums: 'Linea Gotica' (1996, featuring Franco Battiato), 'Tabula Rasa Elettrificata' (1997, which reached #1 on Italian charts selling 80,000+ copies), and the live album 'La terra, la guerra, una questione privata' (1998). After the departure of Zamboni and internal disagreements, the band disbanded in 2002, with some members forming PGR (Per Grazia Ricevuta).

From 2013-2018, some members performed as 'Ex-CSI' then 'Post-CSI', releasing 'Breviario partigiano' (2015). On January 22, 2026, the original lineup announced their reunion after 24 years, launching the 'In viaggio' tour for summer 2026 (28 years after their last tour), with 5000 people attending the first shows at Monte Sole."""

cursor.execute("""
    UPDATE core_band
    SET bio = %s,
        city = 'Emilia-Romagna',
        active_years = '1992-2002, 2013-2018, 2026-present',
        status = 'published',
        updated_at = %s
    WHERE id = 82
""", [bio, timezone.now()])
print("Band updated")

# === 2. Add Genre Tags ===
genres = ['Alternative rock', 'Art rock', 'Indie rock', 'Folk rock', 'Punk rock', 'Experimental']
for genre_name in genres:
    slug = slugify(genre_name)
    cursor.execute("""
        INSERT INTO core_genretag (name, slug)
        VALUES (%s, %s)
        ON CONFLICT (slug) DO NOTHING
    """, [genre_name, slug])
    cursor.execute("SELECT id FROM core_genretag WHERE slug = %s", [slug])
    genre_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO core_band_genre_tags (band_id, genretag_id)
        VALUES (82, %s)
        ON CONFLICT DO NOTHING
    """, [genre_id])
print("Genres added")

# === 3. Add Links ===
links = [
    ('archive', 'C.S.I. Wikipedia IT', 'https://it.wikipedia.org/wiki/Consorzio_Suonatori_Indipendenti', 'Italian Wikipedia', False),
    ('archive', 'C.S.I. Wikipedia EN', 'https://en.wikipedia.org/wiki/Consorzio_Suonatori_Indipendenti', 'English Wikipedia', False),
    ('archive', 'C.S.I. Discogs', 'https://www.discogs.com/artist/146803-CSI', 'Discogs discography', False),
    ('streaming', 'C.S.I. Spotify', 'https://open.spotify.com/playlist/1SjnjsasghfVVDJLVmQis8', 'Spotify playlist', False),
    ('streaming', 'Tabula Rasa Elettrificata - Apple Music', 'https://music.apple.com/it/album/tabula-rasa-elettrificata/1443758257', 'Apple Music album', False),
    ('archive', 'Estatica - Discografia completa', 'https://www.estatica.it/it/musica/c-s-i-consorzio-suonatori-indipendenti/discografia', 'Estatica.it discography', False),
    ('archive', 'Rockit - Album e singoli', 'https://www.rockit.it/consorziosuonatoriindipendenti/discografia', 'Rockit.it discography', False),
    ('video', 'C.S.I. YouTube Channel', 'https://www.youtube.com/channel/UCUcAPhWRKTe0yXjtCXnaO-Q', 'Official YouTube channel', False),
    ('video', 'C.S.I. - Linea gotica Live Tour 2026', 'https://www.youtube.com/watch?v=fuJaWNAw4Qg', 'Live at Monte Sole 2026', False),
    ('video', '33Giri Italian Masters - Tabula Rasa Elettrificata', 'https://www.youtube.com/watch?v=mG0DNd7xCGo', 'Documentary', False),
    ('article', 'DeBaser - Recensione Tabula Rasa', 'https://www.debaser.it/consorzio-suonatori-indipendenti/tabula-rasa-elettrificata/recensione', 'Italian review', False),
    ('article', 'OndaRock - Il miracolo del 1997', 'https://www.ondarock.it/speciali/csi-testa-classifica-album-tabularasaelettrificata/', 'Album analysis', False),
    ('article', 'Metallized - Recensione', 'https://www.metallized.it/recensione.php?id=15515', 'Album review', False),
    ('article', 'Repubblica - Reunion 2026', 'https://www.repubblica.it/spettacoli/musica/2026/08/28/news/csi_consorzio_suonatori_indipendenti_giovanni_lindo_ferretti_monte_sole_marzabotto_concerti_scaletta-425551054/', 'Live report 2026', False),
    ('article', 'Rolling Stone Italia - Reunion ufficiale', 'https://www.rollingstone.it/musica/news-musica/c-s-i-la-reunion-e-ufficiale-ecco-le-date-del-tour/1017417/', 'Reunion announcement', False),
    ('article', 'Il Post - Reunion announcement', 'https://www.ilpost.it/2026/01/22/csi-reunion/', 'News article', False),
    ('article', 'Malpensa24 - Live Monte Sole report', 'https://www.malpensa24.it/c-s-i-live-monte-sole/', 'Concert report 5000 attendees', False),
    ('article', 'Heart of Glass - Tabula Rasa analysis', 'https://heartofglass.altervista.org/blog/tabula-rasa-elettrificata-c-s/', 'Album analysis', False),
    ('shop', 'Ticketmaster - Biglietti Tour 2026', 'https://www.ticketmaster.it/artist/c-s-i-consorzio-suonatori-indipendenti-biglietti/1477663', 'Official tickets', False),
    ('archive', 'Setlist.fm - Monte Sole venue', 'https://www.setlist.fm/venue/parco-regionale-storico-di-monte-sole-marzabotto-italy-2bd2d032.html', 'Setlists', False),
    ('image', 'Wikimedia Commons - C.S.I.', 'https://commons.wikimedia.org/wiki/Category:Consorzio_Suonatori_Indipendenti', 'Media files', False),
]

for link_type, title, url, desc, _ in links:
    cursor.execute("""
        INSERT INTO core_link (band_id, link_type, title, url, description, is_primary, created_at)
        VALUES (82, %s, %s, %s, %s, false, %s)
        ON CONFLICT DO NOTHING
    """, [link_type, title, url, desc, timezone.now()])
print(f"Links added: {len(links)}")

# === 4. Add Labels ===
labels = [
    ('Black Out / Phonogram', 'black-out-phonogram', 'Milan', '', None),
    ('Polygram', 'polygram', 'London', '', 1972),
    ('Consorzio Produttori Indipendenti (CPI)', 'consorzio-produttori-indipendenti', 'Reggio Emilia', '', 1995),
    ('I dischi del mulo', 'i-dischi-del-mulo', '', '', None),
    ('Universal Music Group', 'universal-music-group', 'London', '', 1934),
    ('Tannen Records / Universal Music Italia', 'tannen-records', 'Milan', '', 2010),
]

for name, slug, city, website, founded in labels:
    cursor.execute("""
        INSERT INTO core_label (name, slug, city, website, description, founded_year, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, '', %s, 'unknown', %s, %s)
        ON CONFLICT (slug) DO NOTHING
    """, [name, slug, city, website, founded, timezone.now(), timezone.now()])
print(f"Labels added: {len(labels)}")

# === 5. Add Releases (Studio Albums) ===
studio_albums = [
    ('Ko de mondo', 1994, 'Black Out / Phonogram', 'cd', 'Studio album'),
    ('Linea Gotica', 1996, 'Black Out / Phonogram', 'cd', 'Studio album'),
    ('Tabula Rasa Elettrificata', 1997, 'Black Out / Phonogram', 'cd', 'Studio album, #1 Italian charts 80000+ sales'),
    ('Breviario Partigiano', 2015, 'Tannen Records / Universal Music Italia', 'cd', 'as Post-CSI, with book + DVD'),
]

for title, year, label, fmt, desc in studio_albums:
    slug = slugify(f"csi-{title}-{year}")
    cursor.execute("""
        INSERT INTO core_release (band_id, title, slug, format, year, label, catalog_number, status, description, description_en, cover_image, created_at, updated_at)
        VALUES (82, %s, %s, %s, %s, %s, '', 'published', %s, '', '', %s, %s)
        ON CONFLICT (slug) DO NOTHING
    """, [title, slug, fmt, year, label, desc, timezone.now(), timezone.now()])
print(f"Studio albums added: {len(studio_albums)}")

# === 6. Add Live Albums and Compilations ===
other_releases = [
    ('Maciste contro tutti', 1993, 'live', 'I dischi del mulo', 'Compilation with Üstmamò and Disciplinatha'),
    ('In quiete', 1994, 'live', 'Black Out / Phonogram', 'Live acoustic album, recorded for Videomusic Acoustica'),
    ('La terra, la guerra, una questione privata', 1998, 'live', 'CPI / Polygram', 'Live album, recorded in Alba 1996'),
    ('Noi non ci saremo Vol. 1', 2001, 'cd', 'Universal', 'Compilation'),
    ('Noi non ci saremo Vol. 2', 2001, 'cd', 'Universal', 'Compilation'),
    ('C.S.I. Consorzio Suonatori Indipendenti', 2009, 'compilation', 'Universal', 'Compilation'),
    ('Vicini per chilometri', 2013, 'vinyl', 'Tannen Records / Universal Music Italia', 'Vinyl box set with all 5 official albums'),
    ('In viaggio 1994/1998', 2026, 'compilation', 'Tannen Records / Universal Music Italia', 'Compilation for reunion tour'),
    ('Celluloide/Del mondo', 1994, 'cd', 'Black Out / Phonogram', 'MCD single'),
    ('A tratti (Datura remix)', 1994, 'cd', 'Black Out / Phonogram', 'CD single'),
    ('Buon anno ragazzi', 1996, 'cd', 'Black Out / Phonogram', 'MCD single'),
    ('Tutti giù per terra', 1997, 'cd', 'Black Out / Phonogram', 'CD single, from film soundtrack'),
    ('Forma e sostanza', 1997, 'cd', 'Black Out / Phonogram', 'MCD single'),
    ('Forma e sostanza (remixes)', 1997, 'cd', 'Black Out / Phonogram', 'CD single'),
    ('Matrilineare', 1997, 'cd', 'Black Out / Phonogram', 'CD single'),
    ("Mimporta 'nasega", 1997, 'cd', 'Black Out / Phonogram', 'CD single'),
    ('Noi non ci saremo', 2001, 'cd', 'Universal', 'CDS single'),
]

for title, year, fmt, label, desc in other_releases:
    slug = slugify(f"csi-{title}-{year}")[:255]
    cursor.execute("""
        INSERT INTO core_release (band_id, title, slug, format, year, label, catalog_number, status, description, description_en, cover_image, created_at, updated_at)
        VALUES (82, %s, %s, %s, %s, %s, '', 'published', %s, '', '', %s, %s)
        ON CONFLICT (slug) DO NOTHING
    """, [title, slug, fmt, year, label, desc, timezone.now(), timezone.now()])
print(f"Other releases added: {len(other_releases)}")

# === 7. Add Connections ===
connections_data = [
    ('CCCP Fedeli alla linea', 'predecessor', 'Evolved directly from CCCP after 1990. Same core members Ferretti and Zamboni.'),
    ('Per Grazia Ricevuta (PGR)', 'successor', 'Formed 2002 after C.S.I. disbanded. Members: Ferretti, Canali, Maroccolo, Magnelli, Di Marco.'),
    ('Beautiful', 'shared_member', 'Gianni Maroccolo was also in Beautiful.'),
    ('Üstmamò', 'collaboration', 'Joint live performance documented on Maciste contro tutti (1993).'),
    ('Disciplinatha', 'collaboration', 'Joint live performance documented on Maciste contro tutti (1993).'),
    ('Marlene Kuntz', 'scene_peer', 'C.S.I. covered Marlene Kuntz Lieve on In quiete (1994).'),
]

for band_name, conn_type, notes in connections_data:
    cursor.execute("SELECT id FROM core_band WHERE name ILIKE %s OR name ILIKE %s", [band_name, band_name.replace('(', '').replace(')', '')])
    row = cursor.fetchone()
    if row:
        other_id = row[0]
        cursor.execute("""
            INSERT INTO core_bandconnection (from_band_id, to_band_id, connection_type, notes, source, created_at)
            VALUES (82, %s, %s, %s, '', %s)
            ON CONFLICT (from_band_id, to_band_id, connection_type) DO NOTHING
        """, [other_id, conn_type, notes, timezone.now()])
        print(f"  Connected to {band_name} (id={other_id})")
    else:
        print(f"  Band not found: {band_name}")

# === 8. Verify ===
cursor.execute("SELECT COUNT(*) FROM core_link WHERE band_id = 82")
print(f"\nTotal links: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM core_release WHERE band_id = 82")
print(f"Total releases: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM core_bandconnection WHERE from_band_id = 82 OR to_band_id = 82")
print(f"Total connections: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM core_band_genre_tags WHERE band_id = 82")
print(f"Total genres: {cursor.fetchone()[0]}")

print("\nDone!")
