import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
django.setup()

from apps.core.models import Band, Link, BandConnection, Fanzine, FanzineReview
from django.utils import timezone

# Get Blue Vomit
bv = Band.objects.get(id=70)
print(f'Current band: {bv.name} (id={bv.id}), links: {bv.link_set.count()}')

# Define new links
new_links = [
    ('purchase', 'F.O.A.D. Records — Blue Vomit Discografia 1982/83', 'https://www.foadrecords.com/index.php/blue-vomit-discografia-1982-83-out-now/'),
    ('purchase', 'Hells Headbangers — Blue Vomit LP', 'https://shop-hellsheadbangers.com/blue-vomit-discografia-1982-83-LP.asp'),
    ('purchase', 'Puke N Vomit Records — Blue Vomit LP', 'https://pukenvomitrecords.com/products/blue-vomit-discografia-198x-new-lp'),
    ('purchase', 'Velted Regnub Mailorder — Blue Vomit LP (black)', 'https://veltedregnubmailorder.bigcartel.com/product/blue-vomit-discografia-198x-lp-black'),
    ('archive', 'Punkadeka — Blue Vomit', 'https://www.punkadeka.it/blue-vomit/'),
    ('archive', 'DeBaser — Blue Vomit Demo 83', 'https://en.debaser.it/blue-vomit'),
    ('archive', 'Last.fm — Blue Vomit', 'https://www.last.fm/music/Blue+Vomit'),
    ('archive', 'Internet Archive — Torino 198X', 'https://archive.org/details/youtube-UBrivRoG5GM'),
    ('archive', 'Anarcho-punk.net — Blue Vomit', 'https://anarcho-punk.net/band?band=Blue%20Vomit'),
    ('archive', 'Discogs — Vivo In Una Città Morta (2012)', 'https://www.discogs.com/release/13407397-Blue-Vomit-Vivo-In-Una-Città-Morta'),
    ('archive', 'Italian Wikipedia — Hardcore punk italiano', 'https://it.wikipedia.org/wiki/Hardcore_punk_italiano'),
    ('video', 'YouTube — Blue Vomit Discografia 198X (Full LP)', 'https://www.youtube.com/watch?v=TrNjR0nfrtQ'),
    ('video', 'YouTube — Blue Vomit Vivo In Una Città Morta', 'https://www.youtube.com/watch?v=EzZUoL4zmEg'),
    ('video', 'YouTube — Blue Vomit Vivo In Una Città Morta (2012 Remaster)', 'https://www.youtube.com/watch?v=jczm8YUddqg'),
    ('archive', 'Lyrics Translate — Blue Vomit', 'https://lyricstranslate.com/en/blue-vomit-vivo-una-citta-morta-lyrics.html'),
    ('archive', 'Kleisma — Enrico Falulera (drummer)', 'https://www.kleisma.com/musicisti/profilo/enrico-falulera'),
]

added = 0
for link_type, title, url in new_links:
    link = Link.objects.create(
        band=bv,
        link_type=link_type,
        title=title,
        url=url,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
    added += 1
    print(f'  Added: [{link_type}] {title}')

print(f'\nTotal new links added: {added}')

# Update bio
bv.bio_en = '''Blue Vomit is a cult band from the first wave of Italian punk rock, active 1978-1983 in Torino. Known for their '77 punk sound and nihilistic attitude, they were the precursor to Nerorgasmo. Their complete discography was reissued in 2011 by F.O.A.D. Records on limited blue vinyl (300 copies).

Members: Luca "Abort" Bortolusso (vocals), Martino Cinotto (guitar), Simone Cinotto (guitar), Fabio Di Maggio (bass), Enrico Falulera (drums).

Key releases: Demo '83 (7 tracks, ~10 minutes), appearances on "Torino 198X" (Disforia/Ansia Tapes, 1983) and "Torinoise" (Ansia Tapes, 1982), "Discografia 1982/83" (F.O.A.D. Records, 2011 LP reissue), "Vivo In Una Città Morta" (2012 USB memory stick, 100 hand-numbered copies).

Luca "Abort" Bortolusso went on to form Nerorgasmo (1983-1993), becoming one of the most important figures in Italian hardcore punk. Other members contributed to Declino and the broader Torino punk scene.

Maximum Rocknroll described them as "one of the most sincere, punk and nihilistic bands in the Turin early '80s scene". Their sound evolved from pure '77 punk ("Non mi alzo in pullman", "La sfiga della suora", "Il maniaco") to self-destructive, hallucinatory hardcore ("Vivo in una città morta", "Non sopporto", "Fotti il mito") which anticipated Nerorgasmo.

Part of the foundational Torino punk scene alongside Negazione, Declino, Nerorgasmo, Raw Power, 5° Braccio, Kollettivo, and Stinky Rats.'''

bv.bio = '''Blue Vomit è un gruppo culto della prima ondata della scena punk rock italiana, attivo dal 1978 al 1983 a Torino. Noti per il suono punk '77 e l'attitudine nichilista, furono il precursore dei Nerorgasmo. La loro discografia completa fu ristampata nel 2011 da F.O.A.D. Records in vinile blu limitato (300 copie).

Membri: Luca "Abort" Bortolusso (voce), Martino Cinotto (chitarra), Simone Cinotto (chitarra), Fabio Di Maggio (basso), Enrico Falulera (batteria).

Release principali: Demo '83 (7 tracce, ~10 minuti), apparizioni su "Torino 198X" (Disforia/Ansia Tapes, 1983) e "Torinoise" (Ansia Tapes, 1982), "Discografia 1982/83" (F.O.A.D. Records, 2011 ristampa LP), "Vivo In Una Città Morta" (2012 chiavetta USB, 100 copie numerate a mano).

Luca "Abort" Bortolusso formò i Nerorgasmo (1983-1993), diventando una delle figure più importanti dell'hardcore punk italiano. Altri membri contribuirono ai Declino e alla scena punk torinesa più ampia.

Parte della scena punk torinesa fondazionale insieme a Negazione, Declino, Nerorgasmo, Raw Power, 5° Braccio, Kollettivo e Stinky Rats.'''
bv.save()
print('Bio updated.')

# Add new connections
# Nerorgasmo (71)
try:
    nerorgasmo = Band.objects.get(id=71)
    if not BandConnection.objects.filter(from_band=bv, to_band=nerorgasmo).exists():
        BandConnection.objects.create(from_band=bv, to_band=nerorgasmo, connection_type='shared_member', notes='Luca Abort (vocals) and Simone Cinotto (guitar) went from Blue Vomit to Nerorgasmo')
        print('Added connection: Blue Vomit -> Nerorgasmo (shared_member)')
    else:
        print('Connection Blue Vomit -> Nerorgasmo already exists')
except Band.DoesNotExist:
    print('Nerorgasmo (id=71) not found')

# Declino (72)
try:
    declino = Band.objects.get(id=72)
    if not BandConnection.objects.filter(from_band=bv, to_band=declino).exists():
        BandConnection.objects.create(from_band=bv, to_band=declino, connection_type='shared_member', notes='Some Blue Vomit members went to Declino')
        print('Added connection: Blue Vomit -> Declino (shared_member)')
    else:
        print('Connection Blue Vomit -> Declino already exists')
except Band.DoesNotExist:
    print('Declino (id=72) not found')

# Negazione (64)
try:
    negazione = Band.objects.get(id=64)
    if not BandConnection.objects.filter(from_band=bv, to_band=negazione).exists():
        BandConnection.objects.create(from_band=bv, to_band=negazione, connection_type='scene_peer')
        print('Added connection: Blue Vomit -> Negazione (scene_peer)')
    else:
        print('Connection Blue Vomit -> Negazione already exists')
except Band.DoesNotExist:
    print('Negazione (id=64) not found')

print(f'\nFinal link count for Blue Vomit: {bv.link_set.count()}')
