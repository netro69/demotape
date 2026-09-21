# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python3
"""
Apply Subsonica (id=81) research findings to Demotape database.
Run: cd ~/Projects/demotape && source .venv/bin/activate && python manage.py shell < apply_subsonica_research.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Release, Label, Link, BandConnection, GenreTag

changes = {"releases_added": 0, "links_added": 0, "connections_added": 0, "labels_added": 0, "skipped": 0}


def add_release(band, title, year, format="cd", label_name="", catalog_number="", description=""):
    slug_base = f"{band.slug}-{title.lower().replace(' ', '-').replace(chr(39), '').replace(':', '').replace(chr(242), 'o').replace(chr(224), 'a').replace(chr(232), 'e').replace(chr(249), 'u')}"
    slug = slug_base[:50]
    existing = Release.objects.filter(band=band, slug=slug).exists()
    if not existing:
        Release.objects.create(
            band=band,
            title=title,
            slug=slug,
            format=format,
            year=year,
            label=label_name,
            catalog_number=catalog_number,
            description=description,
        )
        changes["releases_added"] += 1
        print(f"  + RELEASE: {band.name} - {title} ({year})")
    else:
        changes["skipped"] += 1


def add_link(band, link_type, url, title="", description="", is_primary=False):
    existing = Link.objects.filter(band=band, url=url).exists()
    if not existing:
        Link.objects.create(
            band=band,
            link_type=link_type,
            url=url,
            title=title,
            description=description,
            is_primary=is_primary,
        )
        changes["links_added"] += 1
        print(f"  + LINK: {band.name} -> {link_type}: {url[:70]}")
    else:
        changes["skipped"] += 1


def add_connection(from_band, to_band, connection_type, notes="", source=""):
    existing = BandConnection.objects.filter(
        from_band=from_band, to_band=to_band, connection_type=connection_type
    ).exists()
    reverse = BandConnection.objects.filter(
        from_band=to_band, to_band=from_band, connection_type=connection_type
    ).exists()
    if not existing and not reverse:
        BandConnection.objects.create(
            from_band=from_band,
            to_band=to_band,
            connection_type=connection_type,
            notes=notes,
            source=source,
        )
        changes["connections_added"] += 1
        print(f"  + CONN: {from_band.name} -> {to_band.name} ({connection_type})")
    else:
        changes["skipped"] += 1


def get_or_create_label(name, city=""):
    slug = name.lower().replace(' ', '-').replace(chr(39), '').replace('.', '')
    label, created = Label.objects.get_or_create(slug=slug, defaults={'name': name, 'city': city})
    if created:
        changes["labels_added"] += 1
        print(f"  + LABEL: {name}")
    return label


def get_or_create_genre(name):
    slug = name.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '')
    genre, created = GenreTag.objects.get_or_create(slug=slug, defaults={'name': name})
    return genre


# =========================================================================
# Get band
# =========================================================================
try:
    subsonica = Band.objects.get(id=81)
except Band.DoesNotExist:
    print("ERROR: Subsonica (id=81) not found in DB")
    sys.exit(1)

print("")
print("=== Applying Subsonica Research ===")
print("")
print(f"Current releases: {subsonica.releases.count()}")
print(f"Current links: {subsonica.links.count()}")
print(f"Current connections FROM: {subsonica.connections_from.count()}")
print(f"Current connections TO: {subsonica.connections_to.count()}")

# =========================================================================
# Update bio with detailed research
# =========================================================================
bio = (
    "Subsonica are an Italian electronic rock band formed in Turin (Torino) in 1996. "
    "They are among the most important acts of the Italian alternative/underground scene "
    "from the late 1990s to present, combining rock, electronica, techno, punk and new wave influences. "
    ""
    "FORMATION AND MEMBERS: "
    "The band was formed from the meeting of musicians from Turin's alternative scene: "
    "- Samuel Umberto Romano (vocals) - formerly of Gli Amici di Roland (cartoon theme covers band) "
    "and co-founder of Motel Connection side-project (2000) "
    "- Massimiliano 'C-Max' Casacci (guitar, producer) - formerly of Africa Unite (reggae band); "
    "founded Casasonica studios and label; produced for Dr. Livingstone, Mau Mau, Fratelli di Soledad, "
    "Mambassa, Disco Drive "
    "- Davide 'Boosta' Dileo (keyboards) - formerly of Gli Amici di Roland; also DJ, writer; "
    "released solo album 'Iconoclash' (2004); co-founded Caesar Palace (2008) with Linea 77 members "
    "- Enrico 'Ninja' Matta (drums) "
    "- Luca 'Bass Vicio' Vicini (bass, from 2000) - replaced original bassist Pierpaolo 'Pierfunk' "
    "Peretti Griva, who left to form Motel Connection with Samuel and DJ Pisti "
    ""
    "HISTORY: "
    "The name 'Subsonica' was a compromise between 'Sonica' (from a Marlene Kuntz song) and "
    "'Subacqueo' (title of an Africa Unite song by Max Casacci). Their debut album 'Subsonica' "
    "(1997, Mescal) showcased their signature blend of electronic and rock. Breakthrough success "
    "came with 'Microchip Emozionale' (1999, Mescal) featuring hits 'Tutti i miei sbagli' and "
    "'Discolabirinto,' with guests Daniele Silvestri, Marco 'Morgan' Castoldi (Bluvertigo), "
    "and DJ Claudio Coccoluto. In 2000 they competed at the Sanremo Music Festival. "
    ""
    "After a split with Mescal, they signed with Virgin Records, releasing 'Terrestre' (2005, "
    "certified Platinum 110,000 copies) and the live/acoustic double set 'Terrestre Live e "
    "Varie Altre Disfunzioni' (2006). The band has continued releasing albums consistently, "
    "with recent works including 'Mentale Strumentale' (2020, recorded in 2004) and the "
    "compilation 'Terre Rare 96-26' (2026). "
    ""
    "LABELS: "
    "- Mescal Records (early albums 1997-2002) "
    "- Virgin Music (2005-present) "
    "- Casasonica Records (Max Casacci's label/studios, Turin) "
    "- Kippe Records (some releases) "
    ""
    "DISCOGRAPHY: "
    "11 studio albums, 3 live albums, 5 compilations, 3 EPs, over 40 singles. Platinum "
    "certifications for multiple albums. One of Italy's most popular modern rock bands "
    "with millions of streams. "
    ""
    "CONNECTIONS: "
    "- Caesar Palace: formed in 2008 by Davide 'Boosta' Dileo (Subsonica) with Linea 77 members "
    "Davide Pavanello and Christian Montanarella "
    "- Linea 77: collaboration on '66 (Diabolus in musica)' from Linea 77's 'Numb' (2003) "
    "- Motel Connection: side-project of Samuel Romano and Pierfunk (ex-Subsonica bassist), formed 2000 "
    "- Africa Unite: Max Casacci's former reggae band (pre-Subsonica) "
    "- Marlene Kuntz: name 'Sonica' inspired by a Marlene Kuntz song; Samuel Romano co-responsible "
    "for Marlene Kuntz's 'Pornodrome' multimedia project with Dan Solo "
    "- Mau Mau, Dr. Livingstone, Fratelli di Soledad, Mambassa, Disco Drive: produced by Max Casacci "
    ""
    "STYLE/INFLUENCE: "
    "Mixing dance, electronica, and pop/rock, Subsonica represents at best the contemporary "
    "Turin scene, an extremely vital mixture of different races, styles, and rhythms born "
    "and grown up around the clubs and streets of the Murazzi area."
)

subsonica.bio = bio
subsonica.city = "Turin"
subsonica.active_years = "1996-present"
subsonica.website = "https://www.subsonica.it/"
subsonica.discogs_id = "237324"
subsonica.musicbrainz_id = "e49c9a0e-2b34-4f5e-b869-6c6c4f0a0c78"
subsonica.save()

# Add more genre tags
electronic_rock = get_or_create_genre("Electronic Rock")
indietronica = get_or_create_genre("Indietronica")
alternative_dance = get_or_create_genre("Alternative Dance")
electropop = get_or_create_genre("Electropop")
synth_pop = get_or_create_genre("Synth Pop")
new_wave = get_or_create_genre("New Wave")
techno_rock = get_or_create_genre("Techno Rock")
subsonica.genre_tags.add(electronic_rock, indietronica, alternative_dance, electropop, synth_pop, new_wave, techno_rock)
print(f"  + Updated bio and genre tags for {subsonica.name}")

# =========================================================================
# Add Labels
# =========================================================================
print("")
print("--- Adding Labels ---")
mescal = get_or_create_label("Mescal Records", "Italy")
virgin = get_or_create_label("Virgin Music", "Italy")
casasonica = get_or_create_label("Casasonica Records", "Turin")

# =========================================================================
# Add Releases (Studio Albums)
# =========================================================================
print("")
print("--- Adding Releases ---")

# Studio Albums
add_release(subsonica, "Subsonica", 1997, "cd", "Mescal Records", "", "Debut album, spring 1997. Established the band's electronic-rock fusion sound.")
add_release(subsonica, "Microchip Emozionale", 1999, "cd", "Mescal Records", "", "Breakthrough album with hits 'Tutti i miei sbagli' and 'Discolabirinto'. Guests: Daniele Silvestri, Morgan (Bluvertigo), Claudio Coccoluto.")
add_release(subsonica, "Amorematico", 2002, "cd", "Mescal Records", "", "Third studio album, Platinum certified (100,000 copies). First album with bassist Luca Vicini.")
add_release(subsonica, "Terrestre", 2005, "cd", "Virgin Records", "", "First album on Virgin. Platinum certified (110,000 copies).")
add_release(subsonica, "L'Eclissi", 2007, "cd", "Virgin Records", "", "Fifth studio album.")
add_release(subsonica, "Eden", 2011, "cd", "Virgin Records", "", "Sixth studio album, certified Platinum.")
add_release(subsonica, "Una Nave in una Foresta", 2014, "cd", "Virgin Records", "", "Seventh studio album.")
add_release(subsonica, "8", 2018, "cd", "Virgin Records", "", "Eighth studio album.")
add_release(subsonica, "Mentale Strumentale", 2020, "cd", "Virgin Records", "", "Ninth studio album, originally recorded in 2004 and shelved for 16 years.")
add_release(subsonica, "Reel", 2022, "cd", "Virgin Records", "", "Tenth studio album.")
add_release(subsonica, "Terre Rare 96-26", 2026, "cd", "Virgin Records", "", "Compilation spanning 30 years of career.")

# Live Albums
add_release(subsonica, "Terrestre Live e Varie Altre Disfunzioni", 2006, "cd", "Virgin Records", "", "Double disc set: live CD + acoustic/covers collection.")
add_release(subsonica, "Microchip Emozionale Tour", 2000, "cd", "Mescal Records", "", "Live album from Microchip Emozionale tour.")
add_release(subsonica, "Dal Vivo", 2012, "cd", "Virgin Records", "", "Live album recording.")

# Compilation Albums
add_release(subsonica, "Anni Luce 1997-2017", 2017, "cd", "Virgin Records", "", "Best-of compilation celebrating 20 years of career.")
add_release(subsonica, "Microchip Temporale", 2019, "cd", "Virgin Records", "", "Special re-recording of 'Microchip Emozionale' with 14 guest artists.")
add_release(subsonica, "Il Viaggio dell'Anima", 2001, "cd", "Mescal Records", "", "Compilation EP.")
add_release(subsonica, "Il Sangue e la Funzione", 2003, "cd", "Mescal Records", "", "Compilation EP.")
add_release(subsonica, "La Funzione", 2004, "cd", "Mescal Records", "", "EP.")

# Singles (notable)
add_release(subsonica, "Tutti i miei sbagli", 2000, "cd", "Mescal Records", "", "Single from Microchip Emozionale")
add_release(subsonica, "Discolabirinto", 2000, "cd", "Mescal Records", "", "Single from Microchip Emozionale")
add_release(subsonica, "Liberi Tutti", 1999, "cd", "Mescal Records", "", "Single from Microchip Emozionale")
add_release(subsonica, "Nuvole Rapide", 2002, "cd", "Mescal Records", "", "Single from Amorematico")

# =========================================================================
# Add Links
# =========================================================================
print("")
print("--- Adding Links ---")

links = [
    ("archive", "https://it.wikipedia.org/wiki/Subsonica", "Wikipedia IT", "", False),
    ("archive", "https://www.discogs.com/artist/237324-Subsonica", "Discogs", "", False),
    ("archive", "https://rateyourmusic.com/artist/subsonica", "RateYourMusic", "", False),
    ("archive", "https://www.allmusic.com/artist/subsonica-mn0000578715", "AllMusic", "", False),
    ("archive", "https://www.spirit-of-rock.com/en/band/Subsonica", "Spirit of Rock", "", False),
    ("archive", "https://musicbrainz.org/artist/e49c9a0e-2b34-4f5e-b869-6c6c4f0a0c78", "MusicBrainz", "", False),
    ("social", "https://www.instagram.com/subsonicaofficial/", "Instagram (@subsonicaofficial)", "209K followers", False),
    ("social", "https://www.facebook.com/Subsonica/", "Facebook", "474K+ likes", False),
    ("social", "https://soundcloud.com/subsonica", "SoundCloud", "", False),
    ("video", "https://www.youtube.com/@SubsonicaVEVO", "SubsonicaVEVO (YouTube)", "Official video channel", False),
    ("video", "https://www.youtube.com/watch?v=K_hU6pDvIMQ", "Linea 77 ft. Subsonica - 66 (Diabolus in musica)", "Collaboration video", False),
    ("streaming", "https://music.apple.com/it/artist/subsonica/1785978820", "Apple Music", "", False),
    ("purchase", "https://www.subsonica.it/", "Official Store", "Official website & merch", True),
]

for link_type, url, title, description, is_primary in links:
    add_link(subsonica, link_type, url, title, description, is_primary)

# =========================================================================
# Add Connections to other bands
# =========================================================================
print("")
print("--- Adding Connections ---")

# Get related bands from DB
try:
    linea77 = Band.objects.get(id=67)
    add_connection(
        subsonica, linea77, "collaboration",
        "Davide 'Boosta' Dileo (Subsonica) co-founded Caesar Palace (2008) with Linea 77 members Davide Pavanello and Christian Montanarella. Linea 77's 'Numb' (2003) features Subsonica on '66 (Diabolus in musica)'.",
        "https://en.wikipedia.org/wiki/Davide_Dileo"
    )
    add_connection(
        subsonica, linea77, "scene_peer",
        "Both bands from Turin area. Shared members via Caesar Palace superband."
    )
except Band.DoesNotExist:
    print("  Linea 77 not in DB, skipping connection")

try:
    marlene = Band.objects.get(id=62)
    add_connection(
        subsonica, marlene, "scene_peer",
        "Name 'Subsonica' partly inspired by Marlene Kuntz song 'Sonica'. Samuel Romano co-responsible for Marlene Kuntz's 'Pornodrome' multimedia project with Dan Solo. Both bands from same Italian alternative rock scene.",
        "https://grokipedia.com/page/subsonica"
    )
except Band.DoesNotExist:
    print("  Marlene Kuntz not in DB, skipping connection")

try:
    litfiba = Band.objects.get(id=95)
    add_connection(
        subsonica, litfiba, "scene_peer",
        "Both among Italy's most important rock bands. Shared Italian alternative/rock festival circuit. Max Casacci (Subsonica) and Litfiba both represented Turin in national rock scene.",
    )
except Band.DoesNotExist:
    print("  Litfiba not in DB, skipping connection")

try:
    vasco = Band.objects.get(id=96)
    add_connection(
        subsonica, vasco, "scene_peer",
        "Both major Italian rock acts. Shared festival appearances (Cornetto Free Music Festival). Subsonica represented contemporary Italian rock alongside Vasco Rossi's legacy.",
    )
except Band.DoesNotExist:
    print("  Vasco Rossi not in DB, skipping connection")

try:
    diaframma = Band.objects.get(id=98)
    add_connection(
        subsonica, diaframma, "scene_peer",
        "Both part of the 1990s Italian alternative rock wave. Shared underground credibility and festival circuit.",
    )
except Band.DoesNotExist:
    print("  Diaframma not in DB, skipping connection")

try:
    pankow = Band.objects.get(id=99)
    add_connection(
        subsonica, pankow, "scene_peer",
        "Both part of the 1990s Italian alternative rock movement. Shared underground scene credibility.",
    )
except Band.DoesNotExist:
    print("  Pankow not in DB, skipping connection")

# =========================================================================
# Summary
# =========================================================================
print("")
print("=" * 60)
print(f"LABELS ADDED: {changes['labels_added']}")
print(f"RELEASES ADDED: {changes['releases_added']}")
print(f"LINKS ADDED: {changes['links_added']}")
print(f"CONNECTIONS ADDED: {changes['connections_added']}")
print(f"SKIPPED (duplicates): {changes['skipped']}")

# Final status
subsonica.refresh_from_db()
print("")
print(f"=== Final Status for {subsonica.name} ===")
print(f"Releases: {subsonica.releases.count()}")
print(f"Links: {subsonica.links.count()}")
print(f"Connections FROM: {subsonica.connections_from.count()}")
print(f"Connections TO: {subsonica.connections_to.count()}")
print(f"Genre tags: {list(subsonica.genre_tags.all())}")
