# Created-by: agent | Date: 2026-09-17
# Session: subagent — eMi research update
"""Update Demotape database with eMi research findings: links and connections."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')
django.setup()

from apps.core.models import Band, Link, BandConnection
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

def log(msg):
    print(msg)

# ============================================================
# eMi — Emilia Nebl
# ============================================================
log('\n=== eMi ===')
b = get_band('eMi')
log(f'Existing links: {b.links.count()}')

# --- Links ---
links_to_add = [
    ('social', 'Instagram — @ehmeelya', 'https://www.instagram.com/ehmeelya/',
     'eMi official Instagram — emilia nebl | singer-songwriter | LDN/IT'),
    ('streaming', 'SoundCloud — Emilia Nebl', 'https://soundcloud.com/emilia-nebl-36037527',
     'Music archive'),
    ('website', 'Uploadsounds Artist Page', 'https://www.uploadsounds.eu/artists/emi/',
     'Artist bio, genre tags (Pop/Alternative/Electronic)'),
    ('streaming', 'Apple Music — Cheap and Cold (feat. eMi)',
     'https://music.apple.com/us/album/cheap-and-cold-feat-emi-single/1875220340',
     'To You Mom: single feat. eMi (2026)'),
    ('purchase', 'Qobuz — Cheap and Cold (feat. eMi)',
     'https://www.qobuz.com/us-en/album/cheap-and-cold-feat-emi-to-you-mom/jc5qy9ufwfn9p',
     'Hi-Res audio, label info'),
    ('video', 'YouTube — Cheap and Cold (Lyric Video)',
     'https://www.youtube.com/watch?v=HlfSN3J3eU4',
     'Official lyric video (Feb 2026)'),
    ('video', 'YouTube — Cheap and Cold (Audio)',
     'https://www.youtube.com/watch?v=sN4o2Gpdc0g',
     'Audio upload via CDBaby'),
    ('streaming', 'Anghami — Cheap and Cold (feat. eMi)',
     'https://play.anghami.com/song/1257332693',
     'Streaming presence (Middle East/North Africa)'),
    ('purchase', 'Feature.fm — Feel Me Up (Chris Bianco & eMi)',
     'https://ffm.to/feelmeup',
     'Summer anthem (July 2024, Ghost Recordz Group)'),
    ('social', 'Instagram — Dablio (@d4blioband)',
     'https://www.instagram.com/d4blioband/',
     'Band project — eMi is 1/4 of Dablio'),
]

for link_type, title, url, desc in links_to_add:
    if add_link(b, link_type, title, url, desc):
        added_links += 1

# --- Connections ---
log(f'\nExisting connections: {BandConnection.objects.filter(from_band=b).count() + BandConnection.objects.filter(to_band=b).count()}')

# Connection: eMi -> To You Mom: (collaboration)
to_you_mom = get_band('To You Mom:')
if add_connection(b, to_you_mom, 'collaboration', notes='Featured on "Cheap and Cold" (2026)'):
    added_conns += 1

# Connection: eMi -> Lynn (scene_peer via To You Mom: network)
lynn = get_band('Lynn')
if add_connection(b, lynn, 'scene_peer', notes='Via To You Mom: network — vocalist collaboration'):
    added_conns += 1

# Connection: eMi -> Waxlife (scene_peer via To You Mom: network)
waxlife = get_band('Waxlife')
if add_connection(b, waxlife, 'scene_peer', notes='Via To You Mom: network — remixer'):
    added_conns += 1

# Connection: eMi -> The Smokers (scene_peer via To You Mom: network)
the_smokers = get_band('The Smokers')
if add_connection(b, the_smokers, 'scene_peer', notes='Via To You Mom: network — remixer'):
    added_conns += 1

# Connection: eMi -> ≈ Belize ≈ (label_mate — Ghost Records orbit)
belize = get_band('≈ Belize ≈')
if add_connection(b, belize, 'label_mate', notes='Fellow Ghost Records / Ghost Recordz orbit artist'):
    added_conns += 1

# ============================================================
# Summary
# ============================================================
log('\n' + '=' * 60)
log(f'SUMMARY: {added_links} links added, {added_conns} connections added')
log(f'eMi total links: {b.links.count()}')
log(f'eMi total connections: {BandConnection.objects.filter(from_band=b).count() + BandConnection.objects.filter(to_band=b).count()}')
