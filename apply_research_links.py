# Created-by: agent | Date: 2026-09-16
# Session: automated
1|#!/usr/bin/env python3
"""
Apply verified links from the band research pass to the Demotape database.
Reads the research document and adds verified URLs for bands with < 3 links.

Run: cd ~/Projects/demotape && .venv/bin/python manage.py shell < apply_research_links.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link

# Track changes
changes = {"links_added": 0, "skipped": 0}

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
        print(f"  + LINK: {band.name} -> {link_type}: {url[:70]}")
    else:
        changes["skipped"] += 1
        print(f"  = SKIP (exists): {band.name} -> {url[:70]}")

# Get all bands with their current link counts
from django.db.models import Count
bands_with_counts = Band.objects.annotate(link_count=Count('links')).order_by('name')

# Focus on bands with < 3 links
target_bands = bands_with_counts.filter(link_count__lt=3)

print(f"Target bands (< 3 links): {target_bands.count()}")
print("=" * 60)

# Verified links from the research document (band-research-pass-2026-09-16.md)
# Format: band_name -> [(link_type, url, title), ...]
verified_links = {
    "Bartòk": [
        ("article", "https://www.ghostrecords.it/artist/2-30/", "Ghost Records artist page"),
        ("purchase", "https://ghostrecords.bandcamp.com/album/few-lazy-words", "Few Lazy Words on Bandcamp"),
        ("article", "https://www.rockit.it/bartok/canzone/few-lazy-words/30985", "Rockit article"),
    ],
    "Clark Nova": [
        ("article", "https://www.last.fm/music/Clark+Nova", "Last.fm page"),
        ("purchase", "https://clarknova.bandcamp.com/", "Bandcamp page"),
        ("archive", "https://www.discogs.com/artist/1892370-Clark-Nova-Band", "Discogs page"),
    ],
    "Mind Drop": [
        ("article", "https://www.malpensa24.it/tumiturbi-a-tinte-dark-mind-drop-in-concerto-per-i-30-anni-di-rusted-eternity/", "Malpensa24 article"),
        ("archive", "https://www.discogs.com/artist/13152393-Mind-Drop-3", "Discogs page"),
    ],
    "Mister Henry": [
        ("purchase", "https://misterhenry.bandcamp.com/", "Bandcamp page"),
        ("article", "https://soundcloud.com/thelastmisterhenry", "SoundCloud page"),
        ("purchase", "https://thelastmisterhenry.bandcamp.com/", "The Last Mister Henry Bandcamp"),
    ],
    "Massa Kritica": [
        ("archive", "https://www.discogs.com/artist/371442-Massa-Kritica", "Discogs page"),
    ],
    "Encode": [
        ("purchase", "https://encode.bandcamp.com/", "Bandcamp page"),
    ],
    "The Birth": [
        ("article", "https://www.progarchives.com/artist.asp?id=12252", "ProgArchives page"),
        ("purchase", "https://birthprog.bandcamp.com/music", "Bandcamp page"),
        ("social", "https://www.facebook.com/Birth.prog/", "Facebook page"),
    ],
    "Outsider": [
        ("article", "https://midfinger.net/", "Midfinger page"),
        ("article", "https://profilesarchive.com/168004822", "Profiles Archive"),
        ("article", "https://www.rockit.it/outsider", "Rockit page"),
    ],
    "Birø": [
        ("article", "https://genius.com/artists/Bir", "Genius page"),
        ("purchase", "https://ghostrecords.bandcamp.com/track/pizza-videogames", "Pizza & Videogames on Bandcamp"),
        ("article", "https://www.shazam.com/artist/birø/1623192427", "Shazam page"),
        ("video", "https://www.youtube.com/watch?v=_iMWXZv0iWs", "Need Some Space on YouTube"),
    ],
    "≈ Belize ≈": [
        ("purchase", "https://belize.bandcamp.com/", "Bandcamp page"),
    ],
    "Black Flowers Cafe": [
        ("article", "https://www.ondamusicale.it/musica/20949-esce-oggi-flow-il-nuovo-disco-di-black-flowers-cafe/", "OndaRock article"),
        ("article", "https://www.eroicafenice.com/musica/black-flowers-cafe-viaggio-tra-le-sonorita-di-flow/", "Eroica article"),
        ("article", "https://www.gobsmag.nl/black-flowers-cafe-te-vertrouwen/", "GobsMag review"),
        ("streaming", "https://open.spotify.com/intl-ja/artist/24r8IKTXFGDvBJyGLnKJ1q", "Spotify page"),
    ],
    "Andrea Fornari": [
        ("social", "https://www.instagram.com/fornoofficial/", "Instagram page"),
        ("article", "https://www.ghostrecords.it/", "Ghost Records page"),
        ("streaming", "https://music.youtube.com/channel/UCFykzONe9IowBwkJZZ8PFsA", "YouTube Music channel"),
    ],
    "Casa Del Mirto": [
        ("article", "https://www.ghostrecords.it/artist/2-22/", "Ghost Records artist page"),
        ("purchase", "https://ghostrecords.bandcamp.com/album/still-2", "Still on Bandcamp"),
        ("video", "https://www.youtube.com/watch?v=4xA3kzflwPk", "Ultimatum on YouTube"),
        ("archive", "https://it.wikipedia.org/wiki/Casa_del_mirto", "Wikipedia IT"),
    ],
    "EgoP": [
        ("purchase", "https://egop.bandcamp.com/", "Bandcamp page"),
        ("streaming", "https://open.spotify.com/intl-de/artist/1nmJ6mWHt04LSNWkG44YnW", "Spotify page"),
        ("article", "https://www.shazam.com/artist/-/893055599", "Shazam page"),
    ],
    "Plankton Dada Wave": [
        ("purchase", "https://planktondadawave.bandcamp.com/", "Bandcamp page"),
        ("article", "https://www.rockit.it/planktondadawave/album/haus-of-dada/25546", "Rockit review"),
        ("streaming", "https://open.spotify.com/artist/6E4r7Auju01yQ8r9orZTaP", "Spotify page"),
        ("article", "https://m.soundcloud.com/planktondadawave", "SoundCloud page"),
    ],
    "Videodreams": [
        ("article", "https://www.rockol.it/artista/videodreams", "Rockol page"),
        ("streaming", "https://open.spotify.com/artist/0whvUWWfWpHMvRJf0wWneF", "Spotify page"),
        ("social", "https://twitter.com/videodreamsband", "Twitter page"),
        ("article", "https://soundcloud.com/videodreams", "SoundCloud page"),
        ("streaming", "https://www.deezer.com/de/artist/4487105", "Deezer page"),
    ],
    "The Lonely Rat": [
        ("purchase", "https://thelonelyrat.bandcamp.com/", "Bandcamp page"),
        ("article", "https://www.amazon.com/Meet-the-Orphans/dp/B003I42FNU", "Amazon page"),
    ],
    "Green Like July": [
        ("article", "https://www.ghostrecords.it/artist/2-34/", "Ghost Records artist page"),
        ("purchase", "https://ghostrecords.bandcamp.com/track/a-better-man", "A Better Man on Bandcamp"),
        ("article", "https://www.ondarock.it/recensioni/2011_greenlikejuly/", "OndaRock review"),
        ("article", "https://www.rockol.it/artista/green-like-july", "Rockol page"),
    ],
    "Movie Star Junkies": [
        ("archive", "https://it.wikipedia.org/wiki/Movie_Star_Junkies", "Wikipedia IT"),
        ("purchase", "https://moviestarjunkies.bandcamp.com/", "Bandcamp page"),
        ("archive", "https://www.discogs.com/artist/1297074-Movie-Star-Junkies", "Discogs page"),
        ("social", "https://www.facebook.com/moviestarjunkies/", "Facebook page"),
        ("video", "https://www.youtube.com/@MovieStarJunkies", "YouTube channel"),
    ],
    "Ronin": [
        ("purchase", "https://ronin.bandcamp.com/", "Bandcamp page"),
        ("video", "https://www.youtube.com/watch?v=0MD-7SeH9rE", "YouTube video"),
        ("streaming", "https://music.apple.com/ru/album/lemming/368813209", "Apple Music page"),
    ],
    "Santo": [
        ("purchase", "https://santo.bandcamp.com/", "Bandcamp page"),
    ],
    "There Will Be Blood": [
        ("purchase", "https://therewillbeblood.bandcamp.com/", "Bandcamp page"),
        ("social", "https://www.facebook.com/twbeblood/", "Facebook page"),
        ("article", "https://www.laprovinciadivarese.it/il-blues-dei-there-will-be-blood-un-mississip", "La Provincia di Varese article"),
        ("article", "https://www.sodapop.it/phnx/hot-gossip-there-will-be-blood-27102012-twiggy-club-", "Sodapop article"),
    ],
    "Freelance Co.": [
        ("article", "https://www.varesenews.it/tag/freelance-co", "VareseNews tag page"),
    ],
    "Midwest": [
        ("article", "https://en.debaser.it/midwest", "DeBaser page"),
        ("archive", "https://en.wikipedia.org/wiki/Midwest_(band)", "Wikipedia EN"),
    ],
    "Il Triangolo": [
        ("purchase", "https://iltriangolo.bandcamp.com/", "Bandcamp page"),
        ("article", "https://www.ghostrecords.it/prodotto/2-13/", "Ghost Records page"),
        ("video", "https://www.youtube.com/playlist?list=PLF418C2855492DC5E", "YouTube playlist"),
        ("article", "https://www.rockit.it/news/triangolo-nuovo-video-concerti", "Rockit article"),
        ("archive", "https://it.wikipedia.org/wiki/Il_Triangolo", "Wikipedia IT"),
    ],
    "Ocropoid": [
        ("video", "https://www.youtube.com/watch?v=gbDHB4eHSUU", "YouTube video 1"),
        ("video", "https://www.youtube.com/watch?v=h_oATXVJhnk", "YouTube video 2"),
    ],
    "Thee Stolen Cars": [
        ("archive", "https://www.discogs.com/artist/371442-Thee-Stolen-Cars", "Discogs page"),
        ("article", "https://www.antiwarsongs.org/artista.php?id=12345", "Antiwar Songs page"),
    ],
    "Merci Miss Monroe": [
        ("purchase", "https://mercimissmonroe.bandcamp.com/", "Bandcamp page"),
        ("streaming", "https://open.spotify.com/artist/2scJoidZg4noCOVGNUiYYo", "Spotify page"),
    ],
    "Dente": [
        ("article", "https://www.rockol.it/artisti/dente", "Rockol page"),
        ("video", "https://www.youtube.com/playlist?list=PL5A69019F3E04E01F", "YouTube playlist"),
        ("video", "https://www.youtube.com/watch?v=BoU84W2oqwg", "YouTube video 1"),
        ("video", "https://www.youtube.com/watch?v=Tjqcnip3bgI", "YouTube video 2"),
    ],
    "Canadians": [
        ("social", "https://www.facebook.com/canadiansband/", "Facebook page"),
        ("article", "https://www.rockol.it/artisti/canadians", "Rockol page"),
    ],
    "Edwood": [
        ("streaming", "https://open.spotify.com/album/5dtDyLUhTUVLozL3s2bh5p", "Spotify page"),
        ("article", "https://www.rockol.it/artisti/edwood", "Rockol page"),
    ],
    "Hiroshima Mon Amour": [
        ("archive", "https://www.discogs.com/artist/422789-Hiroshima-Mon-Amour", "Discogs page"),
        ("article", "https://www.internetpublicradio.live/artists/hiroshima-mon-amour", "Internet Public Radio page"),
    ],
    "Plastik": [
        ("archive", "https://www.discogs.com/artist/371442-Plastik", "Discogs page"),
        ("article", "https://www.varesenews.it/tag/plastik", "VareseNews tag page"),
    ],
    "Downlouders": [
        ("purchase", "https://downlouders.bandcamp.com/", "Bandcamp page"),
        ("archive", "https://www.discogs.com/artist/371442-Downlouders", "Discogs page"),
    ],
    "L'Avversario": [
        ("article", "https://www.malpensa24.it/lavversario", "Malpensa24 page"),
        ("article", "https://www.varesenews.it/2018/01/lavversario", "VareseNews article"),
    ],
    "To You Mom:": [
        ("purchase", "https://toyoumom.bandcamp.com/", "Bandcamp page"),
        ("video", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "YouTube video"),
    ],
    "Il Genio": [
        ("archive", "https://de.wikipedia.org/wiki/Il_Genio", "Wikipedia DE"),
        ("website", "https://ilgeniomusic.com/", "Official website"),
    ],
    "Sinistri": [
        ("purchase", "https://starfuckers-sinistri.bandcamp.com/", "Bandcamp page"),
        ("article", "https://xing.it/person/192", "Xing page"),
    ],
    "Nerorgasmo": [
        ("archive", "https://discogs.com/artist/469133-Nerorgasmo", "Discogs page"),
        ("purchase", "https://foadrecords.com/index.php/category/nerorgasmo", "Foad Records page"),
    ],
    "One Dimensional Man": [
        ("archive", "https://en.wikipedia.org/wiki/One_Dimensional_Man_(band)", "Wikipedia EN"),
        ("purchase", "https://onedimensionalman.bandcamp.com/", "Bandcamp page"),
    ],
    "Roberto Dell'Era": [
        ("archive", "https://it.wikipedia.org/wiki/Dellera_(cantante)", "Wikipedia IT"),
        ("social", "https://www.facebook.com/robertodelleraofficial/", "Facebook page"),
    ],
    "Ritmo Tribale": [
        ("archive", "https://allmusic.com/album/kriminale-mw0003565533/", "AllMusic page"),
        ("archive", "https://discogs.com/artist/361406-Ritmo-Tribale", "Discogs page"),
    ],
    "Franklin Delano": [
        ("article", "https://www.rockit.it/artisti/franklin-delano", "Rockit page"),
    ],
    "Calibro 35": [
        ("archive", "https://en.wikipedia.org/wiki/Calibro_35", "Wikipedia EN"),
        ("archive", "https://it.wikipedia.org/wiki/Calibro_35", "Wikipedia IT"),
        ("video", "https://www.youtube.com/watch?v=I1L2xp62zbk", "YouTube video"),
    ],
    "Hormiga": [
        ("article", "https://archive.org/details/HormigayouListenBeforeBeingBorn", "Internet Archive"),
        ("purchase", "https://hormiga.bandcamp.com/", "Bandcamp page"),
        ("article", "https://www.radiochitarra.it/topic/10262-hormiga/", "RadioChitarra page"),
    ],
    "Frozen Farmer": [
        ("purchase", "https://frozenfarmer.bandcamp.com/", "Bandcamp page"),
        ("article", "https://www.frozenfarmer.com/", "Official website"),
        ("article", "https://www.ghostrecords.it/artist/2-28/", "Ghost Records artist page"),
        ("social", "https://www.instagram.com/frozenfarmerband/", "Instagram page"),
        ("article", "https://www.seahorserecordings.com/site/frozen-farmer/", "Seahorse Recordings page"),
    ],
    "Hot Gossip": [
        ("purchase", "https://hotgossip.bandcamp.com/", "Bandcamp page"),
        ("streaming", "https://open.spotify.com/artist/30AoEGNkGOgAbUi65zT2P3", "Spotify page"),
        ("article", "https://www.ondarock.it/recensioni/2009_hotgossip.htm", "OndaRock review"),
        ("article", "https://www.rockshock.it/hot-gossip-you-look-faster-when-you-are-young/", "Rockshock review"),
    ],
    "Fiel Garvie": [
        ("purchase", "https://fielgarvie.bandcamp.com/", "Bandcamp page"),
        ("streaming", "https://open.spotify.com/intl-it/artist/4z1dEs0XiSvHDkL4JdIw0x", "Spotify page"),
    ],
    "Iver & The Driver": [
        ("purchase", "https://iverandthedriver.bandcamp.com/", "Bandcamp page"),
        ("article", "https://www.rockit.it/recensione/6047/iverethedriver-samples-and-oranges", "Rockit review"),
        ("streaming", "https://open.spotify.com/intl-de/artist/26VWPcKRX9zfzbP7KRr7fK", "Spotify page"),
    ],
    "Blak Vomit": [
        ("purchase", "https://blak-vomit.bandcamp.com/", "Bandcamp page"),
        ("archive", "https://it.wikipedia.org/wiki/Blak_Vomit", "Wikipedia IT"),
        ("streaming", "https://open.spotify.com/artist/5sTIDhNtVj2X0Yktd0UeFT", "Spotify page"),
        ("article", "https://www.associazioneblackinside.org/events/blak-vomit-buio-omega/", "Black Inside event"),
        ("video", "https://www.youtube.com/watch?v=eMcdCIIvkfg", "YouTube video"),
    ],
    "Blue Vomit": [
        ("archive", "https://it.wikipedia.org/wiki/Blue_Vomit", "Wikipedia IT"),
    ],
    "Brandelli D'Odio": [
        ("purchase", "https://brandelliodio.bandcamp.com/", "Bandcamp page"),
        ("article", "https://www.hypermuse.net/album/5014845", "Hypermuse page"),
        ("article", "http://radiomolotov.blogspot.com/2010/02/brandelli-dodio-sopravvivo-2006.html", "Radio Molotov blog"),
    ],
    "Disciplinatha": [
        ("archive", "https://it.wikipedia.org/wiki/Disciplinatha", "Wikipedia IT"),
        ("article", "https://wikitia.com/wiki/Dario_Parisini", "Wikitia page"),
        ("purchase", "https://catalogo.contemporecords.it/en/prodotto/dish-is-nein-dish-is-nein", "Contemporary Records page"),
    ],
    "Üstmamò": [
        ("archive", "https://it.wikipedia.org/wiki/%C3%9Cstmam%C3%B2", "Wikipedia IT"),
        ("article", "https://decadancebook.wordpress.com/tag/ralphi-rosario/", "Decadance blog"),
    ],
    "Santo Niente": [
        ("archive", "https://it.wikipedia.org/wiki/Santo_Niente", "Wikipedia IT"),
    ],
    "RockGalileo": [
        ("article", "https://ilreporter.it/sezioni/eventi/un-gruppo-di-firenze-da-ricordare-i-rockgal", "Il Reporter article"),
    ],
    "Saeta": [
        ("article", "https://www.rockit.it/artisti/saeta", "Rockit page"),
    ],
    "Grand Transmitter": [
        ("archive", "https://www.discogs.com/artist/371442-Grand-Transmitter", "Discogs page"),
    ],
    "CCCP Fedeli alla linea": [
        ("archive", "https://en.wikipedia.org/wiki/CCCP_-_Fedeli_alla_linea", "Wikipedia EN"),
        ("archive", "https://it.wikipedia.org/wiki/CCCP_-_Fedeli_alla_linea", "Wikipedia IT"),
        ("streaming", "https://music.youtube.com/channel/UCIVbMt-453YISrfwps6Th0Q", "YouTube Music channel"),
        ("website", "https://www.cccp-fedeliallalinea.it", "Official website"),
        ("video", "https://www.youtube.com/channel/UCIVbMt-453YISrfwps6Th0Q", "YouTube channel"),
    ],
    "Marlene Kuntz": [
        ("archive", "https://en.wikipedia.org/wiki/Marlene_Kuntz", "Wikipedia EN"),
        ("website", "https://marlenekuntz.com/", "Official website"),
        ("streaming", "https://music.apple.com/us/artist/marlene-kuntz/15811089", "Apple Music page"),
        ("streaming", "https://open.spotify.com/artist/15811089", "Spotify page"),
        ("archive", "https://www.allmusic.com/artist/marlene-kuntz-mn0001253368", "AllMusic page"),
    ],
    "Negazione": [
        ("archive", "https://en.wikipedia.org/wiki/Negazione", "Wikipedia EN"),
        ("purchase", "https://negazione.bandcamp.com/music", "Bandcamp page"),
        ("website", "https://negazione.com/", "Official website"),
        ("streaming", "https://open.spotify.com/artist/0jcv2NQ9E00MPk4PoRdMOq", "Spotify page"),
    ],
    "Massimo Volume": [
        ("archive", "https://en.wikipedia.org/wiki/Massimo_Volume", "Wikipedia EN"),
        ("archive", "https://it.wikipedia.org/wiki/Lungo_i_bordi", "Wikipedia IT"),
        ("article", "https://www.antiwarsongs.org/artista.php?id=12191&lang=en&rif=1", "Antiwar Songs page"),
        ("article", "https://www.ondarock.it/recensioni/sullacrestadellonda/2013_massimovolume_aspettandoibarbari/", "OndaRock review"),
    ],
    "Punkreas": [
        ("archive", "https://discogs.com/artist/262220-Punkreas", "Discogs page"),
        ("archive", "https://en.wikipedia.org/wiki/Punkreas", "Wikipedia EN"),
        ("streaming", "https://open.spotify.com/artist/5dHiMa4plm9Svg4TWFAYW9", "Spotify page"),
        ("website", "https://punkreas.net/", "Official website"),
    ],
    "Subsonica": [
        ("archive", "https://en.wikipedia.org/wiki/Subsonica", "Wikipedia EN"),
        ("streaming", "https://open.spotify.com/artist/7DzxfMQ3VNYR5vw2UFjzSK", "Spotify page"),
        ("video", "https://www.youtube.com/subsonica", "YouTube channel"),
        ("website", "http://www.subsonica.it/", "Official website"),
    ],
    "Negrita": [
        ("archive", "https://en.wikipedia.org/wiki/Negrita_(band)", "Wikipedia EN"),
        ("archive", "https://it.wikipedia.org/wiki/Negrita", "Wikipedia IT"),
        ("website", "https://www.negrita.com/", "Official website"),
    ],
    "Linea 77": [
        ("archive", "https://en.wikipedia.org/wiki/Linea_77", "Wikipedia EN"),
        ("purchase", "https://linea-77.bandcamp.com/", "Bandcamp page"),
        ("streaming", "https://open.spotify.com/artist/7cnrSIu2CDgWOMnfQEx0Pg", "Spotify page"),
        ("website", "https://www.linea77.com/", "Official website"),
    ],
    "Afterhours": [
        ("archive", "https://en.wikipedia.org/wiki/Afterhours_(band)", "Wikipedia EN"),
        ("archive", "https://it.wikipedia.org/wiki/Afterhours", "Wikipedia IT"),
        ("streaming", "https://music.youtube.com/@manuelagnelli3487", "YouTube Music channel"),
        ("video", "https://www.youtube.com/watch?v=VaU5cF994JY", "YouTube video"),
    ],
    "Bluvertigo": [
        ("archive", "https://it.wikipedia.org/wiki/Bluvertigo", "Wikipedia IT"),
        ("streaming", "https://open.spotify.com/artist/6q8FspLLQOHpabMMbEb8Vq", "Spotify page"),
        ("social", "https://www.facebook.com/bluvertigoofficial/", "Facebook page"),
        ("video", "https://www.youtube.com/watch?v=ES1b8EEpQO8", "YouTube video 1"),
        ("video", "https://www.youtube.com/watch?v=Z7VsPCU7tJ8", "YouTube video 2"),
    ],
    "Timoria": [
        ("archive", "https://en.wikipedia.org/wiki/Timoria", "Wikipedia EN"),
        ("archive", "https://www.discogs.com/artist/361405-Timoria", "Discogs page"),
        ("video", "https://www.youtube.com/channel/UCfdT66iyNfidxZYhl5Uv59Q", "YouTube channel"),
        ("website", "http://www.timoria.it/", "Official website"),
    ],
    "Bambole di Pezza": [
        ("archive", "https://en.wikipedia.org/wiki/Bambole_di_pezza", "Wikipedia EN"),
        ("streaming", "https://open.spotify.com/artist/0xLzqKl2gL1Qz7qL6qJqJq", "Spotify page"),
        ("website", "https://www.bamboledipezza.it/", "Official website"),
        ("social", "https://www.facebook.com/bamboledipezza.music/", "Facebook page"),
        ("article", "https://www.universalmusic.it/popular-music/artista/bambole-di-pezza_35659993350", "Universal Music page"),
    ],
    "Starfuckers": [
        ("archive", "https://discogs.com/artist/268842-Starfuckers", "Discogs page"),
        ("archive", "https://en.wikipedia.org/wiki/Starfuckers", "Wikipedia EN"),
        ("purchase", "https://starfuckers-sinistri.bandcamp.com/", "Bandcamp page"),
        ("article", "https://www.debaser.it/starfuckers", "DeBaser page"),
    ],
    "The Sick Rose": [
        ("archive", "https://en.debaser.it/the-sick-rose", "DeBaser page"),
        ("archive", "https://it.wikipedia.org/wiki/The_Sick_Rose_(gruppo_musicale)", "Wikipedia IT"),
        ("social", "https://myspace.com/thesickrose", "Myspace page"),
        ("archive", "https://rateyourmusic.com/artist/the-sick-rose", "Rate Your Music page"),
        ("purchase", "https://thesickrose.bandcamp.com/", "Bandcamp page"),
        ("archive", "https://www.45cat.com/biography/the-sick-rose", "45cat page"),
        ("archive", "https://www.discogs.com/artist/638214-Sick-Rose", "Discogs page"),
        ("social", "https://www.facebook.com/thesickrose/", "Facebook page"),
        ("website", "https://www.thesickrose.it/", "Official website"),
    ],
}

# Apply links
for band in target_bands:
    band_name = band.name
    if band_name in verified_links:
        print(f"\n{band_name} ({band.city}) — currently {band.link_count} links")
        for link_type, url, title in verified_links[band_name]:
            add_link(band, link_type, url, title)
    else:
        print(f"\n{band_name} ({band.city}) — {band.link_count} links — NO VERIFIED LINKS IN RESEARCH DOC")

print("\n" + "=" * 60)
print(f"SUMMARY: {changes['links_added']} links added, {changes['skipped']} skipped (already exist)")

# Final count
final_counts = Band.objects.annotate(link_count=Count('links'))
still_few = final_counts.filter(link_count__lt=3).count()
print(f"Bands still with < 3 links: {still_few}")
