# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python3
"""Update Litfiba (id=95) with research findings."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

from django.db import connection
from django.utils.text import slugify

cursor = connection.cursor()

# === 1. Update Band ===
bio = """Litfiba is an Italian rock band formed in Florence in 1980. The band evolved from a British-influenced new wave rock to a more personal rock sound influenced by Mediterranean vibes; their songs are mostly sung in Italian.

Founded by guitarist Federico "Ghigo" Renzulli and vocalist Piero Pelù, the band's core lineup also included bassist Gianni Maroccolo and keyboardist Antonio Aiazzi. Litfiba became one of the most influential Italian rock bands, spanning genres from new wave and post-punk to hard rock, Latin metal, and pop rock.

The band's "Trilogy of Power" (Desaparecido, 17 RE, Litfiba 3) is considered a landmark of Italian new wave. The 1990s brought commercial success with the "Tetralogia" albums: El Diablo (fire), Terremoto (earth), Spirito (air), and Mondi sommersi (water).

Piero Pelù left in 1999 for a solo career; the band continued with Gianluigi Cavallo on vocals. Pelù and Renzulli reunited in 2009, releasing Grande nazione (2012) and Eutòpia (2016). The band officially retired in 2022 but reunited in 2025 for the 40th anniversary of "17 RE"."""

cursor.execute("""
    UPDATE core_band
    SET bio = %s,
        city = 'Florence',
        active_years = '1980-2022, 2025-present',
        website = 'https://litfiba.net/',
        discogs_id = '618504',
        musicbrainz_id = 'e68a900e-4fae-493a-84a8-f76ab62d23e4',
        status = 'published',
        updated_at = NOW()
    WHERE id = 95
""", [bio])
print("Band updated")

# === 2. Add Genre Tags ===
genres = ['New wave', 'Hard rock', 'Pop rock', 'Latin rock', 'Heavy metal', 'Post-punk']
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
        VALUES (95, %s)
        ON CONFLICT DO NOTHING
    """, [genre_id])
print("Genres added")

# === 3. Add Links ===
links = [
    ('website', 'Litfiba Official Website', 'https://litfiba.net/', 'Official website', True),
    ('video', 'Litfiba Official YouTube', 'https://www.youtube.com/channel/UCWDnr474piAHwPd1UEY-ybQ', 'Official YouTube channel', False),
    ('social', 'Litfiba Facebook', 'https://www.facebook.com/litfibaufficiale/', 'Official Facebook page', False),
    ('social', 'Litfiba Instagram', 'https://www.instagram.com/Litfiba/', 'Official Instagram', False),
    ('streaming', 'Litfiba Apple Music', 'https://music.apple.com/ca/artist/litfiba/14646701', 'Apple Music artist page', False),
    ('streaming', 'Litfiba Spotify', 'https://open.spotify.com/artist/1HmcAWATwElCmQheMCKGI7', 'Spotify artist page', False),
    ('purchase', 'Litfiba Bandcamp', 'https://litfibalf.bandcamp.com/', 'Bandcamp artist page', False),
    ('archive', 'Litfiba Discogs', 'https://www.discogs.com/artist/618504-Litfiba', 'Discogs discography', False),
    ('archive', 'Litfiba MusicBrainz', 'https://musicbrainz.org/artist/e68a900e-4fae-493a-84a8-f76ab62d23e4', 'MusicBrainz artist page', False),
    ('archive', 'Litfiba Wikipedia EN', 'https://en.wikipedia.org/wiki/Litfiba', 'English Wikipedia', False),
    ('archive', 'Litfiba Wikipedia IT', 'https://it.wikipedia.org/wiki/Litfiba', 'Italian Wikipedia', False),
    ('streaming', 'Litfiba Deezer', 'https://www.deezer.com/en/artist/3314', 'Deezer artist page', False),
    ('purchase', 'Litfiba Bandcamp (Ghigo)', 'https://litfibagh.bandcamp.com/', 'Ghigo Renzulli Bandcamp', False),
    ('archive', 'Litfiba AllMusic', 'https://www.allmusic.com/artist/litfiba-mn0000303552', 'AllMusic biography & discography', False),
    ('archive', 'Litfiba DeBaser', 'https://www.debaser.it/litfiba', 'Italian reviews and community', False),
    ('archive', 'Litfiba Antiwar Songs', 'https://www.antiwarsongs.org/artista.php?lang=en&id=67', 'Lyrics and antiwar themes', False),
]

for link_type, title, url, desc, is_primary in links:
    cursor.execute("""
        INSERT INTO core_link (band_id, link_type, title, url, description, is_primary, created_at)
        VALUES (95, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT DO NOTHING
    """, [link_type, title, url, desc, is_primary])
print(f"Links added: {len(links)}")

# === 4. Add Labels ===
labels = [
    ('IRA Records', 'ira-records', 'Florence', '', None),
    ('CGD', 'cgd', 'Milan', '', 1948),
    ('CGD East West', 'cgd-east-west', 'Milan', '', 1995),
    ('WEA', 'wea', 'London', '', None),
    ('EastWest', 'eastwest', 'London', '', None),
    ('EMI', 'emi', 'London', '', 1931),
    ('Edel', 'edel', 'Hamburg', '', 1986),
    ('Sony Music', 'sony-music', 'New York', '', 1929),
    ('Atlantic Records', 'atlantic-records', 'New York', '', 1947),
    ('Contempo Records', 'contempo-records', 'Florence', '', None),
]

for name, slug, city, website, founded in labels:
    cursor.execute("""
        INSERT INTO core_label (name, slug, city, website, description, founded_year, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, '', %s, 'unknown', NOW(), NOW())
        ON CONFLICT (slug) DO NOTHING
    """, [name, slug, city, website, founded])
print(f"Labels added: {len(labels)}")

# === 5. Add Releases (Studio Albums) ===
studio_albums = [
    ('Desaparecido', 1985, 'IRA Records', ''),
    ('17 RE', 1986, 'CGD East West', ''),
    ('Litfiba 3', 1988, 'WEA', ''),
    ('El Diablo', 1990, 'CGD East West', ''),
    ('Terremoto', 1993, 'WEA', ''),
    ('Spirito', 1994, 'EMI', ''),
    ('Mondi sommersi', 1997, 'EMI', ''),
    ('Infinito', 1999, 'EMI', ''),
    ('Elettromacumba', 2000, 'EMI', ''),
    ('Insidia', 2001, 'EMI', ''),
    ('Essere o sembrare', 2005, 'Edel', ''),
    ('Grande nazione', 2012, 'Sony Music', ''),
    ('Eutòpia', 2016, 'Sony Music', ''),
]

for title, year, label, cat in studio_albums:
    slug = slugify(f"litfiba-{title}-{year}")
    cursor.execute("""
        INSERT INTO core_release (band_id, title, slug, format, year, label, catalog_number, status, description, description_en, cover_image, created_at, updated_at)
        VALUES (95, %s, %s, 'vinyl', %s, %s, %s, 'published', '', '', '', NOW(), NOW())
        ON CONFLICT (slug) DO NOTHING
    """, [title, slug, year, label, cat])
print(f"Studio albums added: {len(studio_albums)}")

# === 6. Add Live Albums and Compilations ===
other_releases = [
    ('Guerra', 1982, 'EP', 'Contempo Records', ''),
    ('Luna/La preda', 1983, 'single', 'Contempo Records', ''),
    ('Eneide di Krypton', 1983, 'soundtrack', 'Contempo Records', ''),
    ('Yassassin', 1984, 'EP', 'Contempo Records', ''),
    ('Transea', 1986, 'EP', 'CGD', ''),
    ('Live 12-5-87 (Aprite i vostri occhi)', 1987, 'live', 'WEA', ''),
    ('Pirata', 1989, 'live', 'WEA', ''),
    ('Sogno ribelle', 1992, 'compilation', 'WEA', ''),
    ('Colpo di coda', 1994, 'live', 'EMI', ''),
    ('Lacio drom (Buon viaggio)', 1994, 'box', 'EMI', ''),
    ('Croce e delizia', 1998, 'live', 'EMI', ''),
    ('Live on Line', 2000, 'live', 'EMI', ''),
    ('The Platinum Collection', 2003, 'compilation', 'EMI', ''),
    ('Stato libero di Litfiba', 2010, 'live', 'Sony Music', ''),
    ('Trilogia 1983-1989 live 2013', 2013, 'live', 'Sony Music', ''),
]

for title, year, fmt, label, cat in other_releases:
    slug = slugify(f"litfiba-{title}-{year}")
    cursor.execute("""
        INSERT INTO core_release (band_id, title, slug, format, year, label, catalog_number, status, description, description_en, cover_image, created_at, updated_at)
        VALUES (95, %s, %s, 'vinyl', %s, %s, %s, 'published', '', '', '', NOW(), NOW())
        ON CONFLICT (slug) DO NOTHING
    """, [title, slug, year, label, cat])
print(f"Other releases added: {len(other_releases)}")

# === 7. Add Connections ===
connections_data = [
    ('CCCP Fedeli alla linea', 'shared_member', 'Gianni Maroccolo, Giorgio Canali, Francesco Magnelli, Ringo De Palma left Litfiba to join CCCP'),
    ('Consorzio Suonatori Indipendenti', 'shared_member', 'Gianni Maroccolo co-founded CSI with Ferretti and Zamboni after CCCP'),
    ('Moda', 'scene_peer', 'Florence new wave scene peers, shared bills and label (Contempo)'),
    ('Giovanni Lindo Ferretti', 'shared_member', 'Connected via CCCP and CSI; shared members with Litfiba'),
    ('Massimo Zamboni', 'shared_member', 'Connected via CCCP and CSI; shared members with Litfiba'),
    ('Gianni Maroccolo', 'shared_member', 'Original Litfiba bassist (1980-1989), later CCCP and CSI'),
    ('Antonio Aiazzi', 'shared_member', 'Original Litfiba keyboardist'),
    ('Gianluigi Cavallo', 'shared_member', 'Litfiba vocalist 1999-2009 (between Pelù eras)'),
    ('Ringo De Palma', 'shared_member', 'Litfiba drummer (1984-1990), died 1990; later joined CCCP'),
    ('Diaframma', 'scene_peer', 'Florence new wave scene peers, shared members, split 7" Amsterdam (1985)'),
    ('Pankow', 'scene_peer', 'Italian new wave scene peers'),
]

for band_name, conn_type, notes in connections_data:
    cursor.execute("SELECT id FROM core_band WHERE name ILIKE %s", [band_name])
    row = cursor.fetchone()
    if row:
        other_id = row[0]
        cursor.execute("""
            INSERT INTO core_bandconnection (from_band_id, to_band_id, connection_type, notes, source, created_at)
            VALUES (95, %s, %s, %s, '', NOW())
            ON CONFLICT (from_band_id, to_band_id, connection_type) DO NOTHING
        """, [other_id, conn_type, notes])
        print(f"  Connected to {band_name} (id={other_id})")
    else:
        print(f"  Band not found: {band_name}")

# === 8. Verify ===
cursor.execute("SELECT COUNT(*) FROM core_link WHERE band_id = 95")
print(f"\nTotal links: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM core_release WHERE band_id = 95")
print(f"Total releases: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM core_bandconnection WHERE from_band_id = 95 OR to_band_id = 95")
print(f"Total connections: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM core_band_genre_tags WHERE band_id = 95")
print(f"Total genres: {cursor.fetchone()[0]}")

print("\nDone!")
