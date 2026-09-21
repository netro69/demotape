# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python
"""Batch research results: Add links and connections for 10 under-researched bands."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection, Label, GenreTag
from django.db import transaction

def get_band(name):
    return Band.objects.get(name=name)

def add_link(band, link_type, title, url, description='', is_primary=False):
    """Add a link only if it doesn't already exist."""
    existing = band.links.filter(url=url).first()
    if existing:
        print(f'  [SKIP duplicate] {band.name}: {title} -> {url}')
        return False
    link = Link.objects.create(
        band=band, link_type=link_type, title=title, url=url,
        description=description, is_primary=is_primary
    )
    print(f'  [ADD link] {band.name}: [{link_type}] {title} -> {url}')
    return True

def add_connection(from_band, to_band, conn_type, source='', notes=''):
    """Add a BandConnection if it doesn't exist. Avoid self-connections."""
    if from_band == to_band:
        print(f'  [SKIP self-connection] {from_band.name}')
        return False
    existing = BandConnection.objects.filter(
        from_band=from_band, to_band=to_band, connection_type=conn_type
    ).first()
    if existing:
        print(f'  [SKIP duplicate conn] {from_band.name} -> {to_band.name} ({conn_type})')
        return False
    conn = BandConnection.objects.create(
        from_band=from_band, to_band=to_band,
        connection_type=conn_type, source=source, notes=notes
    )
    print(f'  [ADD conn] {from_band.name} -> {to_band.name} ({conn_type})')
    return True

added_links = 0
added_conns = 0
log_lines = []

def log(msg):
    print(msg)
    log_lines.append(msg)

# ============================================================
# 1. NEGRITA
# ============================================================
log('\n=== Negrita ===')
b = get_band('Negrita')
log(f'Existing links: {b.links.count()}')

# Add Discogs link
if add_link(b, 'archive', 'Discogs', 'https://www.discogs.com/artist/349217-Negrita',
            'Discogs artist page'): added_links += 1
# Add YouTube
if add_link(b, 'video', 'YouTube Channel', 'https://www.youtube.com/channel/UCTlYeMe9L4yfcI18g6hxrDQ',
            'Official YouTube channel'): added_links += 1
# Add OndaRock
if add_link(b, 'archive', 'OndaRock', 'https://www.ondarock.it/monografie/negrita/',
            'OndaRock artist page'): added_links += 1

# ============================================================
# 2. RITMO TRIBALE
# ============================================================
log('\n=== Ritmo Tribale ===')
b = get_band('Ritmo Tribale')
log(f'Existing links: {b.links.count()}')

if add_link(b, 'archive', 'Wikipedia IT', 'https://it.wikipedia.org/wiki/Ritmo_Tribale',
            'Italian Wikipedia'): added_links += 1
if add_link(b, 'archive', 'OndaRock', 'https://www.ondarock.it/monografie/ritmotribale/',
            'OndaRock monography'): added_links += 1
if add_link(b, 'article', 'Radio Molotov: Kriminale (1990)', 'http://radiomolotov.blogspot.com/2011/08/ritmo-tribale-kriminale-1990.html',
            'Blog analysis of Kriminale album'): added_links += 1
if add_link(b, 'article', 'Pinzillacchere Musicali review', 'http://pinzillaccheremusicali.blogspot.com/2009/11/ritmo-tribale-cuore-sudore-e-rabbia.html',
            'Italian music blog review'): added_links += 1
# Connection: Ritmo Tribale -> Karma (shared member: Andrea Scaglia)
karma = get_band('Karma')
if add_connection(b, karma, 'shared_member', notes='Andrea Scaglia (Ritmo Tribale) also in Karma'): added_conns += 1

# ============================================================
# 3. SCISMA
# ============================================================
log('\n=== Scisma ===')
b = get_band('Scisma')
log(f'Existing links: {b.links.count()}')

if add_link(b, 'archive', 'Wikipedia IT', 'https://it.wikipedia.org/wiki/Scisma_(gruppo_musicale)',
            'Italian Wikipedia'): added_links += 1
if add_link(b, 'archive', 'Discogs', 'https://www.discogs.com/artist/361409-Scisma',
            'Discogs artist page'): added_links += 1
if add_link(b, 'archive', 'Last.fm', 'https://www.last.fm/music/Scisma',
            'Last.fm artist page'): added_links += 1
if add_link(b, 'video', 'YouTube: Pezzetti di carta (1993)', 'https://www.youtube.com/playlist?list=PLiY0l1AiDXnYrdo4MMLjizSEFpmeDuFqy',
            'Playlist with lyrics videos'): added_links += 1

# ============================================================
# 4. KARMA
# ============================================================
log('\n=== Karma ===')
b = get_band('Karma')
log(f'Existing links: {b.links.count()}')

# Connection: Karma -> Ritmo Tribale (shared member)
rt = get_band('Ritmo Tribale')
if add_connection(b, rt, 'shared_member', notes='Andrea Scaglia (Ritmo Tribale) also in Karma'): added_conns += 1
# Connection: Karma -> Manuel Agnelli (Afterhours)
# Check if Afterhours exists
afterhours = Band.objects.filter(name='Afterhours').first()
if afterhours:
    if add_connection(b, afterhours, 'shared_member', notes='Manuel Agnelli (Afterhours) featured in Karma'): added_conns += 1
else:
    log('  Afterhours not in database — skipping connection')
# Connection: Karma -> Negrita (both alt-rock scene peers in 90s Italy)
negrita = get_band('Negrita')
if add_connection(b, negrita, 'scene_peer', notes='Both active in Italian alternative rock scene of the 90s'): added_conns += 1

# ============================================================
# 5. C.S.I. (Consorzio Suonatori Indipendenti)
# ============================================================
log('\n=== C.S.I. ===')
b = get_band('C.S.I.')
log(f'Existing links: {b.links.count()}')

if add_link(b, 'archive', 'OpenEdition article', 'https://journals.openedition.org/rccs/6215',
            'Academic article: Fedeli alla linea: CCCP and the Italian Way to Punk'): added_links += 1
if add_link(b, 'archive', 'Last.fm', 'https://www.last.fm/music/C.S.I.', 'Last.fm artist page'): added_links += 1

# Connection: C.S.I. -> CCCP Fedeli alla linea (successor)
cccp = get_band('CCCP Fedeli alla linea')
if add_connection(b, cccp, 'successor', notes='C.S.I. evolved from CCCP Fedeli alla linea in 1990'): added_conns += 1
if add_connection(cccp, b, 'successor', notes='C.S.I. evolved from CCCP Fedeli alla linea'): added_conns += 1

# ============================================================
# 6. SINISTRI
# ============================================================
log('\n=== Sinistri ===')
b = get_band('Sinistri')
log(f'Existing links: {b.links.count()}')

if add_link(b, 'archive', 'Wikipedia EN (Starfuckers)', 'https://en.wikipedia.org/wiki/Starfuckers',
            'Wikipedia article about Starfuckers/Sinistri'): added_links += 1
if add_link(b, 'streaming', 'Bandcamp: Free Pulse', 'https://starfuckers-sinistri.bandcamp.com/album/sinistri-free-pulse',
            'Bandcamp album page'): added_links += 1

# Connection: Sinistri <- Starfuckers (already exists, check)
sf = get_band('Starfuckers')
if add_connection(sf, b, 'successor', notes='Changed name to Sinistri in 2000'): added_conns += 1

# ============================================================
# 7. OUTSIDER
# ============================================================
log('\n=== Outsider ===')
b = get_band('Outsider')
log(f'Existing links: {b.links.count()}')

if add_link(b, 'archive', 'Rockit', 'https://www.rockit.it/outsider', 'Rockit.it article'): added_links += 1
if add_link(b, 'archive', 'WhoSampled', 'https://www.whosampled.com/Outsider-(Italian-Band)/',
            'WhoSampled: Samples/Covers/Remixes connections'): added_links += 1
if add_link(b, 'archive', 'Internet Archive: Destination Wasted', 'https://archive.org/details/outsiders-destination-wasted',
            'Internet Archive audio release'): added_links += 1
if add_link(b, 'streaming', 'DewOfNothing666 Bandcamp', 'https://dewofnothing666.bandcamp.com/album/outsider-2',
            'Bandcamp Italian Edition'): added_links += 1

# ============================================================
# 8. MISTER HENRY
# ============================================================
log('\n=== Mister Henry ===')
b = get_band('Mister Henry')
log(f'Existing links: {b.links.count()}')

if add_link(b, 'archive', 'AllMusic', 'https://www.allmusic.com/artist/mr-henry-mn0000512108',
            'AllMusic artist page'): added_links += 1
if add_link(b, 'archive', 'Last.fm', 'https://www.last.fm/music/Mr.+Henry',
            'Last.fm artist page'): added_links += 1

# Connection: Mister Henry <- Clark Nova (Ghost Day Varese, scene_peer)
cn = get_band('Clark Nova')
if add_connection(b, cn, 'scene_peer', notes='Both from Varese, performed at Ghost Day'): added_conns += 1

# Adding Ghost Records connections
ghost_roster = [
    'Bartòk', 'Clark Nova', 'Dente', 'Grand Transmitter', 'Calibro 35'
]
for ghost_band_name in ghost_roster:
    gb = Band.objects.filter(name=ghost_band_name).first()
    if gb and gb != b:
        if add_connection(b, gb, 'label_mate', notes='Both on Ghost Records roster'): added_conns += 1

# ============================================================
# 9. THEE STOLEN CARS
# ============================================================
log('\n=== Thee Stolen Cars ===')
b = get_band('Thee Stolen Cars')
log(f'Existing links: {b.links.count()}')

if add_link(b, 'website', 'Michele Anelli official site', 'https://micheleanelli.org/?page_id=120',
            'Bassist Michele Anelli official page about Thee Stolen Cars'): added_links += 1
if add_link(b, 'social', 'Facebook', 'https://www.facebook.com/theestolencars/',
            'Official Facebook page (reunion 2022)'): added_links += 1
if add_link(b, 'article', 'Wikipedia Michele Anelli', 'https://it.wikipedia.org/wiki/Michele_Anelli',
            'Italian Wikipedia: mentions Thee Stolen Cars discography'): added_links += 1
if add_link(b, 'archive', 'Discogs DE', 'https://www.discogs.com/de/artist/3321238-Thee-Stolen-Cars',
            'Discogs (German) artist page'): added_links += 1

# ============================================================
# 10. IL GENIO
# ============================================================
log('\n=== Il Genio ===')
b = get_band('Il Genio')
log(f'Existing links: {b.links.count()}')

if add_link(b, 'streaming', 'Apple Music', 'https://music.apple.com/it/artist/il-genio/281608602',
            'Apple Music artist page'): added_links += 1
if add_link(b, 'archive', 'Wikidata', 'https://www.wikidata.org/wiki/Q1538723',
            'Wikidata entity'): added_links += 1
if add_link(b, 'archive', 'Viberate', 'https://www.viberate.com/artist/il-genio/',
            'Viberate artist page'): added_links += 1
if add_link(b, 'archive', 'BestEverAlbums', 'https://www.besteveralbums.com/thechart.php?b=11021',
            'BestEverAlbums chart page'): added_links += 1

# Connection: Il Genio -> Dente (already in DB as collaboration)
dente = get_band('Dente')
if add_connection(b, dente, 'scene_peer', notes='Both in Varese indie/rock scene, collaborated'): added_conns += 1

# ============================================================
# SUMMARY
# ============================================================
log('\n' + '=' * 60)
log(f'SUMMARY')
log(f'Bands processed: 10')
log(f'New links added: {added_links}')
log(f'New connections added: {added_conns}')
log(f'Total bands: {Band.objects.count()}')
log(f'Total links: {Link.objects.count()}')
log(f'Total connections: {BandConnection.objects.count()}')

# Write to research log
log_path = '/home/ubuntu/Documents/Obsidian/Vault/projects/demotape-research-log.md'
with open(log_path, 'a') as f:
    f.write('\n\n## Fisherman Research Pass — ' + django.utils.timezone.now().strftime('%Y-%m-%d %H:%M') + '\n')
    f.write('\n'.join(log_lines))
print(f'\nLog appended to: {log_path}')
print('\nFiltered log (no duplicates):')
seen = set()
for line in log_lines:
    if 'SKIP' not in line and '===' not in line and line.strip():
        if line not in seen:
            seen.add(line)
            print(line)
