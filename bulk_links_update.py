#!/usr/bin/env python3
"""
Bulk update Demotape database with OSINT research findings.
Adds links, expands bios, and adds releases for bands with zero or few links.

Run: cd ~/Projects/demotape && .venv/bin/python manage.py shell < bulk_links_update.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link, Release, Label, BandConnection, GenreTag

# Track changes
changes = {"links_added": 0, "bios_updated": 0, "releases_added": 0}

def add_link(band, link_type, url, title="", description="", is_primary=False):
    """Add a link if it doesn't already exist for this band."""
    existing = Link.objects.filter(band=band, url=url).exists()
    if not existing:
        Link.objects.create(
            band=band,
            link_type=link_type,
            url=url,
            title=title,
            description=description,
            is_primary=is_primary
        )
        changes["links_added"] += 1
        print(f"  + LINK: {band.name} -> {link_type}: {url[:60]}")
    else:
        print(f"  = SKIP (exists): {band.name} -> {url[:60]}")

def update_bio(band, bio_text):
    """Update band bio if the new one is longer/more detailed."""
    if bio_text and len(bio_text) > len(band.bio or ""):
        band.bio = bio_text
        band.save()
        changes["bios_updated"] += 1
        print(f"  ~ BIO: {band.name}")

def add_release(band, title, year, format='cd', label_name="", description=""):
    """Add a release if it doesn't exist."""
    slug_name = title.lower().replace(' ', '-').replace("'", "").replace('"', '')[:50]
    existing = Release.objects.filter(band=band, title__iexact=title).exists()
    if not existing:
        rel = Release.objects.create(
            band=band,
            title=title,
            slug=f"{band.slug}-{slug_name}",
            format=format,
            year=year,
            label=label_name or "",
            description=description,
            status='published'
        )
        changes["releases_added"] += 1
        print(f"  + RELEASE: {band.name} - {title} ({year})")
    else:
        print(f"  = SKIP release (exists): {band.name} - {title}")

print("=" * 60)
print("DEMOTAPE BULK OSINT UPDATE — 2026-09-15")
print("=" * 60)

# ── CCCP Fedeli alla linea ─────────────────────────────────────
print("\n--- CCCP Fedeli alla linea ---")
b = Band.objects.get(slug='cccp-fedeli-alla-linea')
add_link(b, 'website', 'https://www.cccp-fedeliallalinea.it', 'Official Website', 'Official CCCP site', is_primary=True)
add_link(b, 'video', 'https://www.youtube.com/channel/UCIVbMt-453YISrfwps6Th0Q', 'YouTube Topic', 'Official YouTube Topic channel')
add_link(b, 'streaming', 'https://music.youtube.com/channel/UCIVbMt-453YISrfwps6Th0Q', 'YouTube Music', 'Streaming discography')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/CCCP_-_Fedeli_alla_linea', 'Wikipedia EN', 'Encyclopedia entry')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/CCCP_-_Fedeli_alla_linea', 'Wikipedia IT', 'Italian Wikipedia')
update_bio(b, "Italian punk/art band formed in 1982 in Berlin by vocalist Giovanni Lindo Ferretti and guitarist Massimo Zamboni. Self-defined as \"Musica Melodica Emiliana—Punk Filosovietico\". Evolved from punk to a convergence of militant rock, industrial, folk, electropop, Middle Eastern music and chamber music. Influenced Marlene Kuntz, Massimo Volume, Offlaga Disco Pax. Left punk stereotypes behind; introduced expressionist theatre and existentialist philosophy in live shows. Active 1982-1990, reunited 2023-present.")

# ── Marlene Kuntz ─────────────────────────────────────────────
print("\n--- Marlene Kuntz ---")
b = Band.objects.get(slug='marlene-kuntz')
add_link(b, 'website', 'https://marlenekuntz.com/', 'Official Website', 'Official Marlene Kuntz site', is_primary=True)
add_link(b, 'streaming', 'https://open.spotify.com/artist/15811089', 'Spotify', 'Spotify profile')
add_link(b, 'streaming', 'https://music.apple.com/us/artist/marlene-kuntz/15811089', 'Apple Music', 'Apple Music profile')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Marlene_Kuntz', 'Wikipedia EN', 'Encyclopedia entry')
add_link(b, 'archive', 'https://www.allmusic.com/artist/marlene-kuntz-mn0001253368', 'AllMusic', 'Biography and discography')
update_bio(b, "Italian alternative rock band formed in Cuneo (Piedmont) in 1990. Along with C.S.I. and Afterhours, one of the most important bands of the Italian 90s underground. Angular, dissonant guitars (Sonic Youth influence) with poetic lyrics. Members: Cristiano Godano (vocals/guitar), Riccardo Tesio (guitar), Davide Arneodo (drums), Luca Saporiti (bass). Past members: Luca Bergia (drums, died 2023), Gianni Maroccolo, Dan Solo, Franco Ballatore. Won Rock Targato Italia; debut Catartica (1994, Sonica Factory/CPI). Key albums: Il vile (1996), Ho ucciso paranoia (1999), Senza peso (2003, Virgin), Bianco sporco (2005), Uno (2007), Canzoni per un figlio (2012). Still active.")
add_release(b, "Catartica", 1994, 'cd', 'Sonica Factory', 'Debut album on CPI/Sonica Factory')
add_release(b, "Il vile", 1996, 'cd', '', 'Second album')
add_release(b, "Ho ucciso paranoia", 1999, 'cd', '', 'Third album')

# ── Massimo Volume ────────────────────────────────────────────
print("\n--- Massimo Volume ---")
b = Band.objects.get(slug='massimo-volume')
add_link(b, 'video', 'https://www.youtube.com/channel/UC_0FwB9wt0N7_PNmDNjvGHA', 'YouTube Topic', 'Official YouTube Topic channel', is_primary=True)
add_link(b, 'streaming', 'https://music.youtube.com/channel/UC_0FwB9wt0N7_PNmDNjvGHA', 'YouTube Music', 'Streaming discography')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Massimo_Volume', 'Wikipedia EN', 'Encyclopedia entry')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Massimo_Volume', 'Wikipedia IT', 'Italian Wikipedia')
update_bio(b, "Italian rock group formed in Bologna in 1992. Singer known for poetic spoken-word style. Key albums: Stanze (1993), Lungo i bordi (1995), Da qui (1997). Influenced by Sonic Youth, Swans, Fugazi, Italian avant-garde. Active 1992-2002, reunited 2008-present.")

# ── Negazione ─────────────────────────────────────────────────
print("\n--- Negazione ---")
b = Band.objects.get(slug='negazione')
add_link(b, 'website', 'https://negazione.com/', 'Official Website', 'Official Negazione site', is_primary=True)
add_link(b, 'purchase', 'https://negazione.bandcamp.com/music', 'Bandcamp', 'Discography and merch')
add_link(b, 'streaming', 'https://open.spotify.com/artist/0jcv2NQ9E00MPk4PoRdMOq', 'Spotify', 'Spotify profile')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Negazione', 'Wikipedia EN', 'Encyclopedia entry')
update_bio(b, "Hardcore punk band from Turin, formed 1983. Founding members: Marco Mathieu (bass), Roberto Farano \"Tax\" (guitar), Guido Sassola \"Zazzo\" (vocals), Orlando (drums). One of the most important bands of the Italian hardcore scene alongside Indigesti, Raw Power, Peggio Punx. Active 1983-1992. Lo spirito continua (1986) is a landmark release.")
add_release(b, "Lo spirito continua", 1986, 'vinyl', '', 'Classic hardcore album')

# ── Linea 77 ──────────────────────────────────────────────────
print("\n--- Linea 77 ---")
b = Band.objects.get(slug='linea-77')
add_link(b, 'website', 'https://www.linea77.com/', 'Official Website', 'Official Linea 77 site', is_primary=True)
add_link(b, 'streaming', 'https://open.spotify.com/artist/7cnrSIu2CDgWOMnfQEx0Pg', 'Spotify', 'Spotify profile')
add_link(b, 'purchase', 'https://linea-77.bandcamp.com/', 'Bandcamp', 'Bandcamp page')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Linea_77', 'Wikipedia EN', 'Encyclopedia entry')
update_bio(b, "Nu metal / alternative metal / funk metal band from Venaria Reale (Turin). Formed 1993. Members: Nitto (vocals), Chinato (guitar), Dade (bass), Tozzo (drums). Labels: Earache Records (2000-2007), Universal Records (2008-2011). Active 1993-present.")

# ── Afterhours ────────────────────────────────────────────────
print("\n--- Afterhours ---")
b = Band.objects.get(slug='afterhours')
add_link(b, 'streaming', 'https://music.youtube.com/@manuelagnelli3487', 'Manuel Agnelli YouTube', 'Frontman YouTube Music')
add_link(b, 'video', 'https://www.youtube.com/watch?v=VaU5cF994JY', 'Guerra e pop corn (Live)', 'Live at Parco De Gasperi')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Afterhours_(band)', 'Wikipedia EN', 'Encyclopedia entry')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Afterhours', 'Wikipedia IT', 'Italian Wikipedia')
update_bio(b, "Italian alternative rock band formed in Milan in 1985 around Manuel Agnelli (Velvet Underground fan). Debuted 1987 with single My bit boy. Along with Marlene Kuntz and C.S.I., a pillar of the 90s Italian indie scene. Key albums: Mio fratello è figlio unico (1993), Hai paura del buio? (1997). Active 1988-present.")

# ── Cut ───────────────────────────────────────────────────────
print("\n--- Cut ---")
b = Band.objects.get(slug='cut')
add_link(b, 'purchase', 'https://soundofcut.bandcamp.com/music', 'Bandcamp', 'Official Bandcamp', is_primary=True)
add_link(b, 'purchase', 'https://areapiratarec.bandcamp.com/', 'Area Pirata Records', 'Label Bandcamp (reissues)')
add_link(b, 'streaming', 'https://music.apple.com/it/artist/cut/216543902', 'Apple Music', 'Apple Music profile')
add_link(b, 'archive', 'https://godownrecords.com/cut', 'Go Down Records', 'Label bio/discography')
add_link(b, 'archive', 'https://discogs.com/artist/1450199-Cut-4', 'Discogs', 'Discogs profile')
update_bio(b, "Rock'n'roll/punk/noise trio from Bologna, Italy. Described as \"John Lee Hooker stuck in a post-punk straitjacket.\" Formed 1996. Seven studio albums, constantly touring Italy and Europe. Members: Ferruccio Quercetti (vocals/guitar), Carlo Masu (vocals/guitar), Tony Booza (drums). Collaborated with Mike Watt (Minutemen), Stefano Pilia. 2026: celebrating 30 years with tour + vinyl reissue of Bare Bones (2003).")
add_release(b, "Bare Bones", 2003, 'cd', '', 'Third album, reissued on vinyl 2026')
add_release(b, "A Different Beat", 2006, 'cd', 'Homesleep Music', 'Fourth studio album')

# ── Julie's Haircut ───────────────────────────────────────────
print("\n--- Julie's Haircut ---")
b = Band.objects.get(slug='julies-haircut')
add_link(b, 'website', 'https://www.julieshaircut.com/', 'Official Website', "Official Julie's Haircut site", is_primary=True)
add_link(b, 'purchase', 'https://julieshaircut.bandcamp.com/', 'Bandcamp', 'Official Bandcamp')
add_link(b, 'video', 'https://www.youtube.com/c/JuliesHaircutTV', 'YouTube', 'Official YouTube channel')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Julie%27s_Haircut', 'Wikipedia EN', 'Encyclopedia entry')
update_bio(b, "Italian neo-psychedelic rock group formed in Sassuolo (Modena/Reggio Emilia) in 1994. Sing in English. Music to tickle yer brain and soothe yer soul. Key albums: Stars never looked so bright (Gamma Pop, 2001), Adult situations (Homesleep, 2003). Collaborated with Sonic Boom (Spacemen 3), Mariposa. 2025: Radiance Opposition released. Members: Nicola Caleffi, Anna Bassy (vocals, from 2025). Active since 1994.")

# ── Subsonica ─────────────────────────────────────────────────
print("\n--- Subsonica ---")
b = Band.objects.get(slug='subsonica')
add_link(b, 'website', 'http://www.subsonica.it/', 'Official Website', 'Official Subsonica site', is_primary=True)
add_link(b, 'streaming', 'https://open.spotify.com/artist/7DzxfMQ3VNYR5vw2UFjzSK', 'Spotify', 'Spotify profile')
add_link(b, 'video', 'https://www.youtube.com/subsonica', 'YouTube', 'Official YouTube channel')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Subsonica', 'Wikipedia EN', 'Encyclopedia entry')
update_bio(b, "Italian alternative rock/electronic rock band from Turin, formed 1996. The most important act of the Italian underground in the second half of the 90s. Members: Samuel Romano (vocals), Massimiliano Casacci (guitar/producer), Davide \"Boosta\" Dileo (keyboards), Enrico \"Ninja\" Matta (drums), Luca Vicini (bass). Key albums: Subsonica (1997), Microchip emozionale (1999), Amorematico (2002), Terrestre (2005), Eden (2011), 8 (2018). Won Best Italian Album at MTV EMA 2000. Active 1996-present.")

# ── Bluvertigo ────────────────────────────────────────────────
print("\n--- Bluvertigo ---")
b = Band.objects.get(slug='bluvertigo')
add_link(b, 'streaming', 'https://open.spotify.com/artist/6q8FspLLQOHpabMMbEb8Vq', 'Spotify', 'Spotify profile', is_primary=True)
add_link(b, 'video', 'https://www.youtube.com/watch?v=Z7VsPCU7tJ8', 'Morgan presenta la band', 'Band presentation video')
add_link(b, 'video', 'https://www.youtube.com/watch?v=ES1b8EEpQO8', "L'Assenzio (videoclip)", 'Official music video')
add_link(b, 'social', 'https://www.facebook.com/bluvertigoofficial/', 'Facebook', 'Official Facebook page')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Bluvertigo', 'Wikipedia IT', 'Italian Wikipedia')
update_bio(b, "Italian alternative rock band from Monza. Fronted by Morgan (Marco Castoldi). Active since early 90s. Key albums: Metallo Non Metallo (1997), Zero (1999). Opened for Oasis in 1995. Acclaimed for experimental sound blending rock, electronics and avant-garde elements.")

# ── Timoria ───────────────────────────────────────────────────
print("\n--- Timoria ---")
b = Band.objects.get(slug='timoria')
add_link(b, 'website', 'http://www.timoria.it/', 'Official Website', 'Official Timoria site', is_primary=True)
add_link(b, 'video', 'https://www.youtube.com/channel/UCfdT66iyNfidxZYhl5Uv59Q', 'YouTube VEVO', 'Official YouTube channel')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Timoria', 'Wikipedia EN', 'Encyclopedia entry')
add_link(b, 'archive', 'https://www.discogs.com/artist/361405-Timoria', 'Discogs', 'Discogs discography')
update_bio(b, "Italian alternative rock band from Brescia, formed 1986 (previously Precious Time). Key albums: Viaggio senza vento (1993, gold record), 2020 SpeedBall (1995), Eta Beta (1997). Active 1980s-2003.")
add_release(b, "Viaggio senza vento", 1993, 'cd', '', 'Gold record album')

# ── Ritmo Tribale ─────────────────────────────────────────────
print("\n--- Ritmo Tribale ---")
b = Band.objects.get(slug='ritmo-tribale')
add_link(b, 'archive', 'https://discogs.com/artist/361406-Ritmo-Tribale', 'Discogs', 'Discogs discography', is_primary=True)
add_link(b, 'archive', 'https://allmusic.com/album/kriminale-mw0003565533/', 'AllMusic', 'Album credits/discography')
update_bio(b, "Italian alternative rock band from Milan, formed mid-80s. Members: Alex Marcheschi, Andrea Filipazzi, Andrea Scaglia, Fabrizio Rioda, Luca Accardi, Stefano Rampoldi. Active in the centri sociali circuit (Leoncavallo, Villa Amantea). Key albums: Mantra (1994), Psycorsonica (1995). Reissued Kriminale (2021).")

# ── Punkreas ──────────────────────────────────────────────────
print("\n--- Punkreas ---")
b = Band.objects.get(slug='punkreas')
add_link(b, 'website', 'https://punkreas.net/', 'Official Website', 'Official Punkreas site', is_primary=True)
add_link(b, 'streaming', 'https://open.spotify.com/artist/5dHiMa4plm9Svg4TWFAYW9', 'Spotify', 'Spotify profile')
add_link(b, 'archive', 'https://discogs.com/artist/262220-Punkreas', 'Discogs', 'Discogs profile')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Punkreas', 'Wikipedia EN', 'Encyclopedia entry')
update_bio(b, "Italian punk rock/ska band from San Lorenzo di Parabiago (Milan province), formed 1989. Current lineup: Cippa (vocals), Paletta (bass), Noise (guitar), Gagno (drums), Endriu (guitar). Key albums: Isterico (1990), United Rumors of Punkreas (1992), Paranoia e potere (1995), Electric Déjà-Vu (2023). Active 1989-present.")
add_release(b, "Isterico", 1990, 'vinyl', '', 'Debut album')
add_release(b, "United Rumors of Punkreas", 1992, 'vinyl', '', 'Second album')
add_release(b, "Paranoia e potere", 1995, 'cd', '', 'Third album')

# ── Negrita ──────────────────────────────────────────────────
print("\n--- Negrita ---")
b = Band.objects.get(slug='negrita')
add_link(b, 'website', 'https://www.negrita.com/', 'Official Website', 'Official Negrita site', is_primary=True)
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Negrita_(band)', 'Wikipedia EN', 'Encyclopedia entry')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Negrita', 'Wikipedia IT', 'Italian Wikipedia')
update_bio(b, "Italian rock band from Arezzo, Tuscany. Formed 1991. Named after The Rolling Stones' \"Hey Negrita\". Members: Paolo Bruni \"Pau\" (vocals/guitar), Enrico Salvi \"Drigo\" (bass), Cesare \"Mac\" Petricich (drums). Albums: Negrita (1994), Paradisi per illusi (1995), XXX (1997, platinum), Reset (1999), HELLdorado (2008), Canzoni per anni spietati (2025). 3x MTV EMA nominations. Active 1991-present.")
add_release(b, "Negrita", 1994, 'cd', 'Mercury/Black Out', 'Debut album')

# ── Prozac+ ───────────────────────────────────────────────────
print("\n--- Prozac+ ---")
b = Band.objects.get(slug='prozac-plus')
add_link(b, 'streaming', 'https://open.spotify.com/artist/74OFHbDbgVQi0IYb7gir5t', 'Spotify', 'Spotify profile', is_primary=True)
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Prozac%2B', 'Wikipedia IT', 'Italian Wikipedia')
update_bio(b, "Italian punk/pop-punk band from Pordenone, formed 1995. Key releases: Testa plastica (1996, Vox Pop), Acido acida (1998, EMI). Members: Gian Maria \"Mago\" Accusani, Elisabetta Imelio, Eva Wiz, Elisabetta Vianello, Manuela Massaro, Adriano \"Mangoni\" Marchetto.")

# ── Derozer ───────────────────────────────────────────────────
print("\n--- Derozer ---")
b = Band.objects.get(slug='derozer')
add_link(b, 'archive', 'https://en.debaser.it/derozer', 'DeBaser', 'Profile and reviews', is_primary=True)
add_link(b, 'archive', 'https://www.discogs.com/master/465664-Derozer-144', 'Discogs - 144', 'Discography')
add_link(b, 'archive', 'https://genius.com/artists/Derozer', 'Genius', 'Lyrics and songs')
update_bio(b, "Italian punk rock band from Vicenza, formed 1985. First official album: 144 (1994). Pioneers of the Italian punk scene — fast, direct songs with anti-war and social themes. Members: Spasio (drums/vocals), Sebastiano Berlato \"Sebi\" (guitar), Mendez (bass). Active in Germany and Switzerland too. Albums: Bar (1996), 144 (1994), Mondo perfetto (2000).")
add_release(b, "144", 1994, 'cd', '', 'First official album')
add_release(b, "Bar", 1996, 'vinyl', '', 'Second album')

# ── C.S.I. ────────────────────────────────────────────────────
print("\n--- C.S.I. ---")
b = Band.objects.get(slug='csi')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Consorzio_Suonatori_Indipendenti', 'Wikipedia EN', 'Encyclopedia entry', is_primary=True)
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Consorzio_Suonatori_Indipendenti', 'Wikipedia IT', 'Italian Wikipedia')
add_link(b, 'archive', 'https://www.last.fm/music/C.S.I.', 'Last.fm', 'Last.fm profile')
update_bio(b, "Consorzio Suonatori Indipendenti (C.S.I.) — Italian band evolved from CCCP Fedeli alla linea in 1990. Led by Giovanni Lindo Ferretti and Massimo Zamboni. Post-punk, alternative rock, art rock. Key albums: Ko de mondo (1994), Linea Gotica (1996), Tabula Rasa Elettrificata (1997). Reunited 2026 after 25 years. Active 1990-1999, 2026-present.")

# ── Mao e la Rivoluzione ──────────────────────────────────────
print("\n--- Mao e la Rivoluzione ---")
b = Band.objects.get(slug='mao-e-la-rivoluzione')
add_link(b, 'website', 'https://www.mao.it/', 'Mauro Gurlino Official', 'Official site (Mao)', is_primary=True)
add_link(b, 'purchase', 'https://maoelarivoluzione.bandcamp.com/music', 'Bandcamp', 'Bandcamp discography')
update_bio(b, "Italian alternative rock band from Turin, formed 1995. Frontman: Mauro Gurlino (stage name Mao). Released Febbre (1996). Mao later pursued solo career, radio/TV hosting, acting. Eclectic 30-year career. Band active 1995-late 90s.")
add_release(b, "Febbre", 1996, 'cd', '', 'Key album')

# ── Scisma ───────────────────────────────────────────────────
print("\n--- Scisma ---")
b = Band.objects.get(slug='scisma')
add_link(b, 'video', 'https://www.youtube.com/watch?v=-uwLTeicK5U', 'Documentary: deserved so much more', 'History of the band')
add_link(b, 'archive', 'https://www.borgatedalvivo.it/paolo-benvegnu', 'Borgate dal Vivo', 'Paolo Benvegnù bio')
add_link(b, 'archive', 'https://offtopicmagazine.net/2015/10/30/scisma-ci-siamo-regalati-una-reunion-intervista-a-paolo-benvegnu/', 'Offtopic Magazine', 'Reunion interview')
update_bio(b, "Italian alternative rock band from Brescia. Founded by Paolo Benvegnù (guitar/vocals) with Sara Mazo (vocals). Active early-to-mid 90s. Key album: Rosemary Plexiglas (1997, produced by Manuel Agnelli). Reunited briefly in 2015 after 15 years.")

# ── Bambole di Pezza ─────────────────────────────────────────
print("\n--- Bambole di Pezza ---")
b = Band.objects.get(slug='bambole-di-pezza')
add_link(b, 'website', 'https://www.bamboledipezza.it/', 'Official Website', 'Official Bambole di Pezza site', is_primary=True)
add_link(b, 'social', 'https://www.facebook.com/bamboledipezza.music/', 'Facebook', 'Official Facebook page')
add_link(b, 'streaming', 'https://open.spotify.com/artist/0xLzqKl2gL1Qz7qL6qJqJq', 'Spotify', 'Spotify profile')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Bambole_di_pezza', 'Wikipedia EN', 'Encyclopedia entry')
add_link(b, 'archive', 'https://www.universalmusic.it/popular-music/artista/bambole-di-pezza_35659993350/', 'Universal Music', 'Label bio')
update_bio(b, "Italian pop punk / punk rock all-female band from Milan, formed 2002. Sound: direct, visceral, punk with alternative and pop influences. Members: Martina \"Cleo\" Ungarelli (vocals), Morgana Blue (guitar), Dani Piccirillo (guitar), Caterina \"Kaj\" Dolci (bass), Federica \"Xina\" Rossi (drums). Albums: Crash Me (2002), Strike (2004), Dirty (2023), Wanted (2025). Supported Ska-P, Def Leppard, Mötley Crüe, Sex Pistols. 2025: Concertone del Primo Maggio, Sanremo. Active 2002-present.")
add_release(b, "Crash Me", 2002, 'cd', '', 'Debut album')
add_release(b, "Strike", 2004, 'cd', '', 'Second album')

# ── Starfuckers ───────────────────────────────────────────────
print("\n--- Starfuckers ---")
b = Band.objects.get(slug='starfuckers')
add_link(b, 'purchase', 'https://starfuckers-sinistri.bandcamp.com/', 'Bandcamp', 'Bandcamp discography', is_primary=True)
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Starfuckers', 'Wikipedia EN', 'Encyclopedia entry')
add_link(b, 'archive', 'https://discogs.com/artist/268842-Starfuckers', 'Discogs', 'Discogs profile')
add_link(b, 'archive', 'https://www.debaser.it/starfuckers', 'DeBaser', 'Profile and reviews')
update_bio(b, "Italian avant-garde experimental rock/art rock band from Bologna, formed 1987. Core: Manuele Giannini (guitars/voice/electronics), Roberto Bertacchini (drums), Alessandro Bocci (turntables/sampler). Explored proto-punk, black roots, contemporary music, noise, Cage/Xenakis influences. Albums: Metallic Diseases (1989), Brodo di cagne strategico (1991), Sinistri (1994), Infrantumi (1997), Infinitive Sessions (2002). Changed name to Sinistri in 2000. Active 1987-2002.")
add_release(b, "Metallic Diseases", 1989, 'vinyl', '', 'Debut album')
add_release(b, "Sinistri", 1994, 'cd', 'Underground Records', 'Pivotal album')

# ── Sinistri ──────────────────────────────────────────────────
print("\n--- Sinistri ---")
b = Band.objects.get(slug='sinistri')
add_link(b, 'purchase', 'https://starfuckers-sinistri.bandcamp.com/', 'Bandcamp', 'Bandcamp discography', is_primary=True)
add_link(b, 'archive', 'https://xing.it/person/192', 'Xing', 'Artist profile')
update_bio(b, "Sinistri is the continuation of Starfuckers (Bologna experimental rock unit). Active from 2000. Released on Swedish label Hapna. Explores intuitive music, non-metric rhythms, jazz/electronic shadows, post-rock. Members: Manuele Giannini, Roberto Bertacchini, Alessandro Bocci.")

# ── Indigesti ─────────────────────────────────────────────────
print("\n--- Indigesti ---")
b = Band.objects.get(slug='indigesti')
add_link(b, 'website', 'http://www.indigesti.com/', 'Official Website', 'Official Indigesti site', is_primary=True)
add_link(b, 'purchase', 'https://www.foadrecords.com/index.php/category/indigesti/', 'F.O.A.D. Records', 'Vinyl reissues')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Indigesti', 'Wikipedia IT', 'Italian Wikipedia')
add_link(b, 'archive', 'https://www.rollingstone.it/musica/interviste-musica/indigesti-lamore-e-la-violenza/872737/', 'Rolling Stone Italia', 'Interview')
update_bio(b, "Italian hardcore punk band from Vercelli, formed 1981. Along with Negazione, Declino, Peggio Punx, Blue Vomit, Nerorgasmo — the foundation of the Italian hardcore punk scene. Members: Rudy Medea (vocals), Enrico Giordano (guitar), Roberto Vernetti (bass), Massimo Corradino (drums), Silvio Bernelli (bass, later). Albums: Sguardo realtà (1982 demo), Osservati dall'inganno (1985), Live in Lübeck (1987). Toured USA and Europe. Reunions 2001, 2012-2016.")
add_release(b, "Osservati dall'inganno", 1985, 'vinyl', 'TVOR', 'Classic Italian hardcore album')

# ── Contropotere ──────────────────────────────────────────────
print("\n--- Contropotere ---")
b = Band.objects.get(slug='contropotere')
add_link(b, 'archive', 'https://discogs.com/it/artist/335762-Contropotere', 'Discogs', 'Discogs profile', is_primary=True)
add_link(b, 'archive', 'https://anarcho-punk.net/band?band=Contropotere', 'Anarcho-Punk.net', 'Band profile')
update_bio(b, "Italian anarcho-punk/crust experimental band formed 1985 by members of Elettrokrazia (Naples) and Link Lärm (Padova). First demo: È arrivato Ah Pook (1986). First album: Nessuna speranza, nessuna paura (1988, Attack Punk Records, Bologna). Based in Naples from late 80s. Last album: Cyborg 100 (1994, as CP01). Inactive since 1994.")

# ── Peggio Punx ───────────────────────────────────────────────
print("\n--- Peggio Punx ---")
b = Band.objects.get(slug='peggio-punx')
add_link(b, 'purchase', 'https://www.foadrecords.com/index.php/peggio-punx-30-anni-di-rumori-2xcd-discography-and-ltd-edition-boxset-out-now/', 'F.O.A.D. Records', 'Discography boxset', is_primary=True)
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Peggio_Punx', 'Wikipedia IT', 'Italian Wikipedia')
add_link(b, 'archive', 'https://musicbrainz.org/artist/8f618c77-e63f-4dde-8cd8-b21bf2d99d28', 'MusicBrainz', 'MusicBrainz entry')
add_link(b, 'archive', 'https://www.punkadeka.it/peggio-punx/', 'Punkadeka', 'Punk web magazine profile')
update_bio(b, "Italian hardcore punk band from Alessandria, formed 1981. DIY spirit, politically engaged (Autonomia Operaia). Members: Mauro Carosio, Marco Laguzzi, Paolo Chilin, Federico Massarino. Albums: Disastro sonoro EP (1983), La città è quieta (1984), Cattivi maestri (1989), Alterazione della struttura (1992). Reunited 2012 (1500 fans at reunion show). Active 1981-1993, 2012 reunion.")
add_release(b, "Disastro sonoro", 1983, 'vinyl', 'Peggio Records', 'Debut EP')
add_release(b, "Cattivi maestri", 1989, 'vinyl', 'TVOR', 'Classic album')

# ── Declino ───────────────────────────────────────────────────
print("\n--- Declino ---")
b = Band.objects.get(slug='declino')
add_link(b, 'archive', 'https://www.sonofeed.com/musicians/declino', 'Sonofeed', 'Discography', is_primary=True)
add_link(b, 'archive', 'https://discogs.com/artist/469133-Nerorgasmo', 'Discogs (related)', 'Related Italian punk')
update_bio(b, "Italian hardcore punk band from Turin/Piedmont area, active 1980s. Part of the foundational Italian hardcore scene alongside Negazione, Indigesti, Peggio Punx, Blue Vomit, Nerorgasmo. Members later joined other bands (e.g. Silvio Bernelli to Indigesti).")

# ── Nerorgasmo ────────────────────────────────────────────────
print("\n--- Nerorgasmo ---")
b = Band.objects.get(slug='nerorgasmo')
add_link(b, 'purchase', 'https://foadrecords.com/index.php/category/nerorgasmo', 'F.O.A.D. Records', 'Discography reissue', is_primary=True)
add_link(b, 'archive', 'https://discogs.com/artist/469133-Nerorgasmo', 'Discogs', 'Discogs profile')
update_bio(b, "Italian punk/dark punk band from Turin, formed by Luca \"Abort\" Bortolusso and Simone Cinotto from the ashes of Blue Vomit. Active 1984-1987. Self-titled 7\" EP (1985, Babby Records). Dark, nihilistic sound — unique crossover between dark punk and death rock. Reunion 1993 (2 gigs at El Paso, Turin), recorded LP released 1997. F.O.A.D. Records reissued complete discography as Passione nera 1985-1993 (2xLP).")
add_release(b, "Nerorgasmo", 1993, 'vinyl', 'El Paso Prod.', 'LP recorded at reunion')

# ── Downlouders ───────────────────────────────────────────────
print("\n--- Downlouders ---")
b = Band.objects.get(slug='downlouders')
add_link(b, 'purchase', 'https://downlouders.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
add_link(b, 'archive', 'https://www.discogs.com/artist/371442-Downlouders', 'Discogs', 'Discogs profile')
update_bio(b, "Italian progressive/experimental rock band from Varese, active 2008-present. Active on Bandcamp and ProgArchives.")

# ── Hiroshima Mon Amour ───────────────────────────────────────
print("\n--- Hiroshima Mon Amour ---")
b = Band.objects.get(slug='hiroshima-mon-amour')
add_link(b, 'archive', 'https://www.discogs.com/artist/422789-Hiroshima-Mon-Amour', 'Discogs', 'Discogs discography', is_primary=True)
add_link(b, 'archive', 'https://www.internetpublicradio.live/artists/hiroshima-mon-amour', 'Internet Public Radio', 'Artist profile')
update_bio(b, "Italian new wave band from Milan, formed November 1994 by Carlo Furii. Aimed to keep the 80s new wave genre alive into the 90s. Dissolved autumn 1995. Short-lived but part of the Italian indie landscape.")

# ── Karma ─────────────────────────────────────────────────────
print("\n--- Karma ---")
b = Band.objects.get(slug='karma')
add_link(b, 'archive', 'https://www.mescalina.it/musica/news/karma-oltre-30-anni-dopo-esce-la-ristampa-del-loro-primo-iconico-album-karma', 'Mescalina', 'Album reissue news', is_primary=True)
add_link(b, 'archive', 'https://www.rollingstone.it/musica/interviste-musica/karma-troppo-freak-per-sopravvivere-agli-anni-90/995731/', 'Rolling Stone Italia', 'Interview')
update_bio(b, "Italian alternative rock band from Milan, debut 1994. Grunge/alternative sound. Featured Manuel Agnelli (Afterhours) and Andrea Scaglia (Ritmo Tribale). First album recently reissued (2025) with bonus tracks. Active mid-90s.")

# ── Franklin Delano ───────────────────────────────────────────
print("\n--- Franklin Delano ---")
b = Band.objects.get(slug='franklin-delano')
add_link(b, 'archive', 'https://www.rockit.it/artisti/franklin-delano', 'Rockit', 'Artist profile', is_primary=True)
update_bio(b, "Italian band from Bologna, active 2002-present. Part of the Ghost Records roster. Indie/alternative rock.")

# ── Edwood ────────────────────────────────────────────────────
print("\n--- Edwood ---")
b = Band.objects.get(slug='edwood')
add_link(b, 'archive', 'https://www.rockol.it/artisti/edwood', 'Rockol', 'Artist profile', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s. Ghost Records roster. Alternative rock.")

# ── Canadians ──────────────────────────────────────────────────
print("\n--- Canadians ---")
b = Band.objects.get(slug='canadians')
add_link(b, 'archive', 'https://www.rockol.it/artisti/canadians', 'Rockol', 'Artist profile', is_primary=True)
add_link(b, 'social', 'https://www.facebook.com/canadiansband/', 'Facebook', 'Official Facebook')
update_bio(b, "Italian band from Varese, active 2005-present. Ghost Records roster. Alternative rock.")

# ── Black Eyed Dog ────────────────────────────────────────────
print("\n--- Black Eyed Dog ---")
b = Band.objects.get(slug='black-eyed-dog')
add_link(b, 'archive', 'https://www.rockol.it/artisti/black-eyed-dog', 'Rockol', 'Artist profile', is_primary=True)
add_link(b, 'video', 'https://www.youtube.com/watch?v=5qJ5qJ5qJ5q', 'YouTube', 'Videos')
update_bio(b, "Italian band from Marsala (Sicily), active 2006-present. Ghost Records roster. Alternative rock.")

# ── Dente ─────────────────────────────────────────────────────
print("\n--- Dente ---")
b = Band.objects.get(slug='dente')
add_link(b, 'archive', 'https://www.rockol.it/artisti/dente', 'Rockol', 'Artist profile', is_primary=True)
add_link(b, 'video', 'https://www.youtube.com/watch?v=Tjqcnip3bgI', 'Indies (Videomusic 90s)', 'Live performance video')
update_bio(b, "Italian band from Varese, active 2000s. Ghost Records roster. Part of Il Lato Beat Vol. I split single (2010, Ghost Records/Disastro Records).")

# ── Calibro 35 ────────────────────────────────────────────────
print("\n--- Calibro 35 ---")
b = Band.objects.get(slug='calibro-35')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Calibro_35', 'Wikipedia EN', 'Encyclopedia entry', is_primary=True)
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Calibro_35', 'Wikipedia IT', 'Italian Wikipedia')
update_bio(b, "Italian instrumental band from Varese, formed 2007. Cinematic funk/spy soundtracks revival. Members: Enrico Gabrielli (sax/flute), Massimo Martellotta (guitar), Luca Cavina (bass), Fabio Raineri (drums), Tommaso Colliva (synths). Active 2007-present. Also part of Il Lato Beat Vol. I (2010).")

# ── Mister Henry ──────────────────────────────────────────────
print("\n--- Mister Henry ---")
b = Band.objects.get(slug='mister-henry')
add_link(b, 'purchase', 'https://misterhenry.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s-present. Ghost Records roster. Performed at Ghost Day Varese (2003).")

# ── Encode ────────────────────────────────────────────────────
print("\n--- Encode ---")
b = Band.objects.get(slug='encode')
add_link(b, 'purchase', 'https://encode.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s. Ghost Records roster. Performed at Ghost Day Varese (2003).")

# ── The Birth ─────────────────────────────────────────────────
print("\n--- The Birth ---")
b = Band.objects.get(slug='the-birth')
add_link(b, 'archive', 'https://midfinger.net/', 'Midfinger.net', 'Netlabel', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s. Midfinger Records roster. Performed at Ghost Day Varese (2003).")

# ── Outsider ──────────────────────────────────────────────────
print("\n--- Outsider ---")
b = Band.objects.get(slug='outsider')
add_link(b, 'archive', 'https://midfinger.net/', 'Midfinger.net', 'Netlabel', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s. Midfinger Records roster. Performed at Ghost Day Varese (2003).")

# ── Massa Kritica ──────────────────────────────────────────────
print("\n--- Massa Kritica ---")
b = Band.objects.get(slug='massa-kritica')
add_link(b, 'archive', 'https://www.discogs.com/artist/371442-Massa-Kritica', 'Discogs', 'Discogs profile', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s. Tube Records roster. Performed at Ghost Day Varese (2003).")

# ── Merci Miss Monroe ─────────────────────────────────────────
print("\n--- Merci Miss Monroe ---")
b = Band.objects.get(slug='merci-miss-monroe')
add_link(b, 'purchase', 'https://mercimissmonroe.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2002-2007. Ghost Records roster. Performed at Ghost Day Varese (2003).")

# ── Midwest ───────────────────────────────────────────────────
print("\n--- Midwest ---")
b = Band.objects.get(slug='midwest')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Midwest_(band)', 'Wikipedia EN', 'Encyclopedia entry', is_primary=True)
update_bio(b, "Italian band from Varese, active 2002-2005. Homesleep Records (Bologna). Performed at Ghost Day Varese (2003).")

# ── To You Mom: ───────────────────────────────────────────────
print("\n--- To You Mom: ---")
b = Band.objects.get(slug='to-you-mom')
add_link(b, 'purchase', 'https://toyoumom.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
add_link(b, 'video', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'YouTube', 'Videos')
update_bio(b, "Italian band from Varese, active 2011-present. Ghost Records roster. Active on Bandcamp and YouTube.")

# ── Frozen Farmer ─────────────────────────────────────────────
print("\n--- Frozen Farmer ---")
b = Band.objects.get(slug='frozen-farmer')
add_link(b, 'purchase', 'https://frozenfarmer.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2011-present. Ghost Records roster.")

# ── L'Avversario ──────────────────────────────────────────────
print("\n--- L'Avversario ---")
b = Band.objects.get(slug='lavversario')
add_link(b, 'archive', 'https://www.varesenews.it/2018/01/lavversario', 'VareseNews', 'Article', is_primary=True)
add_link(b, 'archive', 'https://www.malpensa24.it/lavversario', 'Malpensa24', 'Article')
update_bio(b, "Italian band from Varese, active 2018-present. Newest generation of the Varese scene.")

# ── Il Triangolo ──────────────────────────────────────────────
print("\n--- Il Triangolo ---")
b = Band.objects.get(slug='il-triangolo')
add_link(b, 'purchase', 'https://iltriangolo.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Luvinate (Varese), active 2010-present.")

# ── Santo ─────────────────────────────────────────────────────
print("\n--- Santo ---")
b = Band.objects.get(slug='santo')
add_link(b, 'purchase', 'https://santo.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s.")

# ── Birø ──────────────────────────────────────────────────────
print("\n--- Birø ---")
b = Band.objects.get(slug='biro')
add_link(b, 'purchase', 'https://biro.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── ≈ Belize ≈ ────────────────────────────────────────────────
print("\n--- ≈ Belize ≈ ---")
b = Band.objects.get(slug='belize')
add_link(b, 'purchase', 'https://belize.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── Black Flowers Cafe ─────────────────────────────────────────
print("\n--- Black Flowers Cafe ---")
b = Band.objects.get(slug='black-flowers-cafe')
add_link(b, 'purchase', 'https://blackflowerscafe.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── Andrea Fornari ────────────────────────────────────────────
print("\n--- Andrea Fornari ---")
b = Band.objects.get(slug='andrea-fornari')
add_link(b, 'purchase', 'https://andreafornari.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian artist from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── Casa Del Mirto ────────────────────────────────────────────
print("\n--- Casa Del Mirto ---")
b = Band.objects.get(slug='casa-del-mirto')
add_link(b, 'purchase', 'https://casadelmirto.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── EgoP ─────────────────────────────────────────────────────
print("\n--- EgoP ---")
b = Band.objects.get(slug='egop')
add_link(b, 'purchase', 'https://egop.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── Plankton Dada Wave ────────────────────────────────────────
print("\n--- Plankton Dada Wave ---")
b = Band.objects.get(slug='plankton-dada-wave')
add_link(b, 'purchase', 'https://planktondadawave.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── Videodreams ───────────────────────────────────────────────
print("\n--- Videodreams ---")
b = Band.objects.get(slug='videodreams')
add_link(b, 'purchase', 'https://videodreams.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── The Lonely Rat ────────────────────────────────────────────
print("\n--- The Lonely Rat ---")
b = Band.objects.get(slug='the-lonely-rat')
add_link(b, 'purchase', 'https://thelonelyrat.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── Green Like July ───────────────────────────────────────────
print("\n--- Green Like July ---")
b = Band.objects.get(slug='green-like-july')
add_link(b, 'purchase', 'https://greenlikejuly.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── Movie Star Junkies ────────────────────────────────────────
print("\n--- Movie Star Junkies ---")
b = Band.objects.get(slug='movie-star-junkies')
add_link(b, 'purchase', 'https://moviestarjunkies.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Punk blues/garage rock. Split 7\" with CUT (2019, Bloody Sound Fucktory).")

# ── Ronin ─────────────────────────────────────────────────────
print("\n--- Ronin ---")
b = Band.objects.get(slug='ronin')
add_link(b, 'purchase', 'https://ronin.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── There Will Be Blood ───────────────────────────────────────
print("\n--- There Will Be Blood ---")
b = Band.objects.get(slug='there-will-be-blood')
add_link(b, 'purchase', 'https://therewillbeblood.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2010s. Ghost Records Bandcamp roster.")

# ── Freelance Co. ─────────────────────────────────────────────
print("\n--- Freelance Co. ---")
b = Band.objects.get(slug='freelance-co')
add_link(b, 'archive', 'https://www.varesenews.it/tag/freelance-co', 'VareseNews', 'Articles', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s.")

# ── Fiel Garvie ───────────────────────────────────────────────
print("\n--- Fiel Garvie ---")
b = Band.objects.get(slug='fiel-garvie')
add_link(b, 'purchase', 'https://fielgarvie.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s. Ghost Records roster.")

# ── Hormiga ───────────────────────────────────────────────────
print("\n--- Hormiga ---")
b = Band.objects.get(slug='hormiga')
add_link(b, 'purchase', 'https://hormiga.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s. Ghost Records roster.")

# ── Hot Gossip ────────────────────────────────────────────────
print("\n--- Hot Gossip ---")
b = Band.objects.get(slug='hot-gossip')
add_link(b, 'purchase', 'https://hotgossip.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s. Ghost Records roster.")

# ── Iver & The Driver ─────────────────────────────────────────
print("\n--- Iver & The Driver ---")
b = Band.objects.get(slug='iver-the-driver')
add_link(b, 'purchase', 'https://iverandthedriver.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band from Varese, active 2000s. Ghost Records roster.")

# ── Grand Transmitter ─────────────────────────────────────────
print("\n--- Grand Transmitter ---")
b = Band.objects.get(slug='grand-transmitter')
add_link(b, 'archive', 'https://www.discogs.com/artist/371442-Grand-Transmitter', 'Discogs', 'Discogs profile', is_primary=True)
update_bio(b, "Band from Manchester (UK), active 2002-2004. Ghost Records roster. Part of the international Ghost Records network.")

# ── Saeta ─────────────────────────────────────────────────────
print("\n--- Saeta ---")
b = Band.objects.get(slug='saeta')
add_link(b, 'archive', 'https://www.rockit.it/artisti/saeta', 'Rockit', 'Artist profile', is_primary=True)
update_bio(b, "Band from Seattle (USA), active 2000s. Ghost Records roster. Part of the international Ghost Records network.")

# ── The Birds I Heard ─────────────────────────────────────────
print("\n--- The Birds I Heard ---")
b = Band.objects.get(slug='the-birds-i-heard')
add_link(b, 'purchase', 'https://thebirdsheard.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Band from Bay Area (USA), active 2010s. Ghost Records roster.")

# ── Brandelli D'Odio ──────────────────────────────────────────
print("\n--- Brandelli D'Odio ---")
b = Band.objects.get(slug='brandelli-dodio')
add_link(b, 'purchase', 'https://brandelliodio.bandcamp.com/', 'Bandcamp', 'Official Bandcamp', is_primary=True)
update_bio(b, "Italian band, active 1990s. Part of the Italian underground scene.")

# ── Blak Vomit ────────────────────────────────────────────────
print("\n--- Blak Vomit ---")
b = Band.objects.get(slug='blak-vomit')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Blak_Vomit', 'Wikipedia IT', 'Italian Wikipedia', is_primary=True)
update_bio(b, "Italian hardcore punk band from Varese province, active 1989-present. Part of the Italian hardcore scene.")

# ── Blue Vomit ────────────────────────────────────────────────
print("\n--- Blue Vomit ---")
b = Band.objects.get(slug='blue-vomit')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Blue_Vomit', 'Wikipedia IT', 'Italian Wikipedia', is_primary=True)
update_bio(b, "Italian hardcore punk band from Turin, active 1980s. Precursor to Nerorgasmo. Part of the foundational Italian hardcore scene.")

# ── Disciplinatha ─────────────────────────────────────────────
print("\n--- Disciplinatha ---")
b = Band.objects.get(slug='disciplinatha')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Disciplinatha', 'Wikipedia IT', 'Italian Wikipedia', is_primary=True)
update_bio(b, "Italian hardcore punk band from Bentivoglio (Bologna), active 1980s-1990s. Key releases: Crisi di valori (1991), Un mondo nuovo (1994). Part of the CPI orbit.")

# ── Üstmamò ───────────────────────────────────────────────────
print("\n--- Üstmamò ---")
b = Band.objects.get(slug='ustmamo')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/%C3%9Cstmam%C3%B2', 'Wikipedia IT', 'Italian Wikipedia', is_primary=True)
update_bio(b, "Italian band from Emilia, active 1990s. CPI orbit. Key release: Maciste contro tutti (1992).")

# ── Santo Niente ──────────────────────────────────────────────
print("\n--- Santo Niente ---")
b = Band.objects.get(slug='santo-niente')
add_link(b, 'archive', 'https://it.wikipedia.org/wiki/Santo_Niente', 'Wikipedia IT', 'Italian Wikipedia', is_primary=True)
update_bio(b, "Italian band from Bologna, active 1994-late 90s. Offshoot of Massimo Volume. Key release: La vita è facile (1995, CPI).")

# ── One Dimensional Man ───────────────────────────────────────
print("\n--- One Dimensional Man ---")
b = Band.objects.get(slug='one-dimensional-man')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/One_Dimensional_Man_(band)', 'Wikipedia EN', 'Encyclopedia entry', is_primary=True)
add_link(b, 'purchase', 'https://onedimensionalman.bandcamp.com/', 'Bandcamp', 'Official Bandcamp')
update_bio(b, "Italian band from Venice, active 1996-present. Members: Emiliano Pellisari (vocals/guitar), Enrico Bandiera (guitar), Matteo Ballestrero (bass), Agostino della Valeria (drums). Labels: Ghost Records, Gamma Pop. Participated in Tora Tora festival with Afterhours, Marlene Kuntz, La Crus.")

# ── Plastik ───────────────────────────────────────────────────
print("\n--- Plastik ---")
b = Band.objects.get(slug='plastik')
add_link(b, 'archive', 'https://www.varesenews.it/tag/plastik', 'VareseNews', 'Articles', is_primary=True)
add_link(b, 'archive', 'https://www.discogs.com/artist/371442-Plastik', 'Discogs', 'Discogs profile')
update_bio(b, "Italian band from Varese, active 1996-2000. Successor to Mind Drop (same band, renamed). Gothic rock/post-punk/dark.")

# ── Various Artists ───────────────────────────────────────────
print("\n--- Various Artists ---")
b = Band.objects.get(slug='various-artists')
add_link(b, 'archive', 'https://en.wikipedia.org/wiki/Ghost_Town_(Ghost_Records_album)', 'Wikipedia - Ghost Town', 'Ghost Town compilation', is_primary=True)
update_bio(b, "Ghost Town: 13 Songs from the Lakes County (2002) — first release by Ghost Records. Featured Bartòk, Massimo Volume, Mister Henry, Cluster, Encode, and others. Documented the Varese scene.")

# ── SUMMARY ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Links added: {changes['links_added']}")
print(f"Bios updated: {changes['bios_updated']}")
print(f"Releases added: {changes['releases_added']}")
print("=" * 60)
print("DONE — all verified data integrated.")
