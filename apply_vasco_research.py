# Created-by: agent | Date: 2026-09-16
# Session: automated
1|from apps.core.models import Band, Label, Link, BandConnection, Release, GenreTag

# VASCO ROSSI OSINT RESEARCH
# ========================
# Vasco Rossi is a SINGER-SONGWRITER (cantautore), not a traditional band.
# Connection to RockGalileo via Saverio Lanza (RockGalileo frontman) who later
# collaborated with Vasco Rossi as producer/songwriter.

# Build bio based on research
bio = """Vasco Rossi (born 7 February 1952 in Zocca, province of Modena, Italy) — also known mononymously as Vasco or by his nickname Il Blasco — is an Italian singer-songwriter and poet. He is one of the best-selling and most influential figures in Italian rock history, with over 30 albums (including studio, live, and compilations) and more than 250 songs written across a career spanning five decades.

Born in the small village of Zocca in the Emilia-Romagna Apennines, Rossi was encouraged by his mother Novella Corsi to study music as a child. He later worked as a DJ and, in 1975, co-founded "Punto Radio" in Zocca — one of the first private/free radio stations in Emilia-Romagna — along with his friend Marco Gherardi. Through the radio station, he began showcasing his own songs to a wider audience.

He moved to Bologna to study accountancy (ragioneria) while pursuing music. His professional career began in the late 1970s when he started performing in the Bologna-Emilia underground music scene. His first single "Jenny"/"Silvia" was released in 1977 on the Lotus label.

After his initial underground period, Vasco Rossi rose to national fame through the 1980s and beyond. He is NOT a band in the traditional sense but a solo singer-songwriter who has performed with various backing bands throughout his career, most notably the Steve Rogers Band (1980s) and later configurations (VascoNonStop Live, etc.).

**Connection to RockGalileo / Italian underground:**
The documented connection is through Saverio Lanza (frontman of RockGalileo, the Florence-based indie rock band 1989-1998). After RockGalileo disbanded in 1998, Lanza became a renowned producer, arranger, and composer who went on to collaborate with several major Italian artists, including Vasco Rossi, Piero Pelù, Biagio Antonacci, Irene Grandi, and Cristina Donà. Lanza co-wrote "Benvenuti nel vostro viaggio" with Vasco Rossi for the Pastis project (2020). This connection represents the cross-pollination between the 1990s Italian indie underground scene (RockGalileo) and mainstream Italian rock (Vasco Rossi)."""

# Update Vasco Rossi band entry
vasco = Band.objects.get(id=96)
vasco.city = "Zocca (Modena)"
vasco.active_years = "1975-present"
vasco.bio = bio
vasco.website = "https://www.vascorossi.net"
vasco.discogs_id = "130185"
vasco.musicbrainz_id = "144994cb-1734-4b3b-b856-0a49472a7181"
vasco.status = 'published'
vasco.save()
print(f"Updated Vasco Rossi: city={vasco.city}, active_years={vasco.active_years}, status={vasco.status}")

# Add genre tags (use existing ones)
rock_tag = GenreTag.objects.get(slug="rock")
pop_rock_tag = GenreTag.objects.get(slug="pop-rock")
cantautore_tag = GenreTag.objects.get(slug="singer-songwriter")
vasco.genre_tags.add(rock_tag, pop_rock_tag, cantautore_tag)
print(f"Added genre tags: Rock, Pop Rock, Singer-Songwriter")

# Add releases (key studio albums, major live albums, and notable compilations)
releases_data = [
    ("...Ma cosa vuoi che sia una canzone...", "vinyl", 1978, "Lotus", "LOP 12802"),
    ("Non siamo mica gli americani!", "vinyl", 1979, "Lotus", "LOP 12815"),
    ("Colpa d'Alfredo", "vinyl", 1980, "Targa Italiana", "TAL 1401"),
    ("Siamo solo noi", "vinyl", 1981, "Targa Italiana", "TAL 1404"),
    ("Vado al massimo", "vinyl", 1982, "Carosello", "CLN 25095"),
    ("Bollicine", "vinyl", 1983, "Carosello", "CLN 25101"),
    ("Va bene, va bene così", "vinyl", 1984, "Carosello", "CLN 25123"),
    ("Cosa succede in città", "vinyl", 1985, "Carosello", ""),
    ("Vasco Rossi", "vinyl", 1987, "Carosello", ""),
    ("Liberi liberi", "vinyl", 1989, "EMI Italiana", ""),
    ("Gli spari sopra", "cd", 1993, "Carosello", ""),
    ("Buoni o cattivi", "cd", 2004, "Universal Music Italy", ""),
    ("Vivere o niente", "cd", 2011, "Universal Music Italy", ""),
    ("Sono innocente", "cd", 2014, "Universal Music Italy", ""),
    ("Vivere o niente / Live Kom 011", "cd", 2017, "Universal Music Italy", ""),
    ("Siamo qui", "digital", 2021, "Universal Music Italy", ""),
]

for title, fmt, year, label_name, cat in releases_data:
    slug_base = title.lower().replace(" ", "-").replace("'", "").replace("...", "").replace("!", "")
    r, created = Release.objects.get_or_create(
        band=vasco,
        title=title,
        defaults={
            'slug': f"vasco-rossi-{slug_base}-{year}",
            'format': fmt,
            'year': year,
            'label': label_name,
            'catalog_number': cat,
            'status': 'published'
        }
    )
    if created:
        print(f"  Added release: {title} ({year}) [{fmt}] on {label_name}")
    else:
        print(f"  Already exists: {title} ({year})")

# Add links
links_data = [
    ("website", "Official Website", "https://www.vascorossi.net", True),
    ("video", "YouTube Channel (Official)", "https://www.youtube.com/channel/UCHubnYpuorQh5QglY2J60JQ", False),
    ("video", "VascoRossiVEVO", "https://www.youtube.com/channel/UCgQgdm037Fiao4utznjyhaw", False),
    ("archive", "Discogs", "https://www.discogs.com/artist/130185-Vasco-Rossi", False),
    ("archive", "MusicBrainz", "https://musicbrainz.org/artist/144994cb-1734-4b3b-b856-0a49472a7181", False),
    ("archive", "Last.fm", "https://www.last.fm/music/Vasco+Rossi", False),
    ("streaming", "Spotify", "https://open.spotify.com/artist/14589739", False),
]

for link_type, title, url, is_primary in links_data:
    l, created = Link.objects.get_or_create(
        band=vasco,
        url=url,
        defaults={
            'link_type': link_type,
            'title': title,
            'is_primary': is_primary,
        }
    )
    if created:
        print(f"  Added link: [{link_type}] {title}")

# Add/update band connection - RockGalileo -> Vasco Rossi (collaboration)
conn, created = BandConnection.objects.get_or_create(
    from_band=Band.objects.get(id=86),
    to_band=vasco,
    connection_type='collaboration',
    defaults={
        'source': 'https://www.thewalkoffame.it/blog/lintervista-la-reunion-spirituale-e-cosmica-di-saverio-lanza/',
        'notes': 'Saverio Lanza (RockGalileo frontman) collaborated with Vasco Rossi as producer, arranger, and songwriter post-1998. Lanza co-wrote "Benvenuti nel vostro viaggio" with Vasco Rossi. Represents the link between the 1990s Florentine indie underground (RockGalileo) and mainstream Italian rock.'
    }
)
if created:
    print(f"Added connection: RockGalileo -> Vasco Rossi (collaboration)")

# Add reverse connection (scene peer)
conn2, created = BandConnection.objects.get_or_create(
    from_band=vasco,
    to_band=Band.objects.get(id=86),
    connection_type='scene_peer',
    defaults={
        'source': 'https://www.thewalkoffame.it/blog/lintervista-la-reunion-spirituale-e-cosmica-di-saverio-lanza/',
        'notes': 'RockGalileo was active in the same Italian alternative rock scene era; members later crossed over to collaborate with Vasco Rossi.'
    }
)
if created:
    print(f"Added connection: Vasco Rossi -> RockGalileo (scene_peer)")

print("\n=== FINAL STATE ===")
vasco.refresh_from_db()
print(f"Bands info updated:")
print(f"  Name: {vasco.name}")
print(f"  City: {vasco.city}")
print(f"  Active Years: {vasco.active_years}")
print(f"  Discogs: {vasco.discogs_id}")
print(f"  MusicBrainz: {vasco.musicbrainz_id}")
print(f"  Status: {vasco.status}")
print(f"  Releases count: {vasco.releases.count()}")
print(f"  Links count: {vasco.links.count()}")
print(f"  Connections from: {vasco.connections_from.count()}")
print(f"  Connections to: {vasco.connections_to.count()}")
