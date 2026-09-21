"""Session 31 — apply Massimo Volume research: new links + fanzine reviews."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demotape.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from apps.core.models import Band, Fanzine, FanzineReview, Link

BAND_ID = 47

NEW_LINKS = [
    # --- YouTube: cassette rips & bootlegs (underground core) ---
    ("video", "MV - Untitled / Demo Nero (1992) — ITALIAN TAPES ARCHIVE cassette rip", "https://www.youtube.com/watch?v=qN-xpWFuL5I", "Cassette rip of legendary 1992 demo, 12:11. Channel dedicated to Italian tape demos."),
    ("video", "MV - Massimo Volume (1992) demo — dovic", "https://www.youtube.com/watch?v=58um52b3-MU", "Alternate upload of the 1992 Demo Nero, 12:11."),
    ("video", "MV live - Radio Blackout, Torino 13/05/1994 (full set)", "https://www.youtube.com/watch?v=8jUQKDf8fFA", "53-min full live bootleg from Circolo della Musica, Torino."),
    ("video", "MV - Parco della Colletta, Torino, 13 May 1994 (full)", "https://www.youtube.com/watch?v=asIx1YHtMTk", "Alternate source of the 13/05/1994 Torino bootleg, 53:23."),
    ("video", "MV - Pellerossa Festival, Torino, 13 Jul 1997 (FULL)", "https://www.youtube.com/watch?v=rL9e8yjFC8M", "1h21min full festival set, Club Privè era."),
    ("video", "MV - Parco della Pellerina, Torino, 12 Jul 1997 (full)", "https://www.youtube.com/watch?v=BYdWZvpCVSg", "58-min full set from Torino park festival."),
    ("video", "MV - Live @ La Tempesta al Rivolta (official)", "https://www.youtube.com/watch?v=mtZ5nJiw31c", "42-min official La Tempesta Dischi channel live."),
    ("video", "MV - Stanze (Remastered) Full Album 1993", "https://www.youtube.com/watch?v=H-tDAO8ucYk", "Full album rip, 38:00."),
    ("video", "MV - Stanze live 1997 (Il Muro)", "https://www.youtube.com/watch?v=90ViM0lBvOU", "Live TV recording from Il Muro, 1997."),
    ("video", "MV - Aspettando i barbari (Full Album)", "https://www.youtube.com/watch?v=NA21711kUdI", "Full album rip, 41:43."),
    ("video", "MV - Club Privè", "https://www.youtube.com/watch?v=0wlG_u7A8Nc", "Club Privè (1999) track video."),
    ("video", "MV - Vedute dallo spazio / Ororo", "https://www.youtube.com/watch?v=Gn_hPfyes-k", "Classic Stanze-era fan upload, 13.7k views."),
    ("video", "MV - Stanze vuote", "https://www.youtube.com/watch?v=jvaP9TTi2NQ", "Fan upload, 14k views."),
    ("video", "MV - Fuoco Fatuo live 1997", "https://www.youtube.com/watch?v=Xri9qjjDZgU", "Live 1997, 6.3k views."),
    ("video", "MV - Il primo Dio live @ Collegno", "https://www.youtube.com/watch?v=XtlHYyjO2pQ", "Live clip."),
    ("video", "RETRONOUVEAU: MV - Il primo Dio (live)", "https://www.youtube.com/watch?v=tqfgczAhSUs", "Live clip from RETRONOUVEAU club night."),
    # --- Blogs: demo/bootleg download posts ---
    ("other", "Radio Molotov blog — Demo Nero (1992) post + MediaFire", "http://radiomolotov.blogspot.com/2009/08/massimo-volume-demo-nero-1992.html", "2009 blog post sharing the Demo Nero cassette rip with tracklist and MediaFire link."),
    ("other", "The Breakfast Jumpers — Registrazione del 10-11-92 + Demo bootleg", "https://breakfastjumpers.blogspot.com/2010/09/massimo-volume-registrazione-del-10-11.html", "Bootleg of 10-11 Nov 1992 rehearsal recordings + demo; full tracklist incl. unreleased Il Tema di Mimmo."),
    ("other", "MV stanze blog — Demo page", "http://mvstanze.blogspot.com/2005/02/demo.html", "Dedicated Massimo Volume/Stanze blog documenting the demo and song histories."),
    ("other", "MediaFire — Demo Nero (1992) [v2] rar", "http://www.mediafire.com/file/9uq3w726frca5lw/massimo%20volume%20-%20demo%20%231992%20%5Bv2%5D.rar", "Direct download of Demo Nero rip (v2)."),
    ("other", "MediaFire — Registrazione del 10-11-92 + Demo", "http://www.mediafire.com/?mhmmwqmvrbw", "Direct download of 1992 rehearsal bootleg + demo."),
    # --- Torrents ---
    ("other", "The Pirate Bay — Lungo i bordi (1995) MP3 192kbps", "https://thepiratebay.org/torrent/4962192", "Torrent, 1 seeder, info_hash BE2B674EDD124B6C3A4D02E8BADE976E06A5560C, 14 files."),
    ("other", "The Pirate Bay — Da Qui (1997) MP3 192kbps", "https://thepiratebay.org/torrent/4969569", "Torrent, 0 seeders, info_hash D4059295DA63595B7675BDAC4D1D207C58B49DED, 12 files."),
    # --- Internet Archive ---
    ("archive", "Internet Archive — Massimo Volume / Vittoria Burattini (audio)", "https://archive.org/details/massimo-volume-vittoria-burattini", "8MB MP3 audio item, Ferrara sotto le stelle / Soviet Soviet related recording."),
    # --- Press / reviews ---
    ("website", "OndaRock — Lungo i bordi (Le pietre miliari italiane)", "https://www.ondarock.it/recensioni/pietremiliariitaliane/massimovolume_lungo/", "Milestone-series review of the 1995 album."),
    ("website", "DeBaser — Lungo i bordi recensione (sallu)", "https://www.debaser.it/massimo-volume/lungo-i-bordi/recensione-sallu", "User review, CCCP/Sonic Youth/Slint comparisons."),
    ("website", "Impatto Sonoro — Giorni come Stanze: l'esordio incendiario", "https://www.impattosonoro.it/2023/12/23/speciali/back-in-time/giorni-come-stanze-lesordio-incendiario-dei-massimo-volume/", "2023 Back in Time retrospective on Stanze and the Demo Nero story."),
    ("website", "Rockit — Dieci pezzi per conoscere i Massimo Volume", "https://www.rockit.it/articolo/10-pezzi-massimo-volume-selezione", "10-track introduction selection."),
    ("website", "Vice Italia — I Massimo Volume classificano i loro album", "https://www.vice.com/it/article/abbiamo-chiesto-ai-massimo-volume-di-fare-una-classifica-dei-loro-album/", "Band self-ranking interview with Clementi and Sommacal."),
    ("website", "OndaRock — Il nuotatore review", "https://www.ondarock.it/recensioni/sullacrestadellonda/2019-massimovolume-ilnuotatore/", "Review of 2019 comeback album."),
    ("website", "Heart of Glass — Lungo i bordi review", "https://heartofglass.altervista.org/blog/lungo-i-bordi-massimo-volume/", "Blog review of Lungo i bordi."),
    ("website", "Recensiamo Musica — Solchi: Lungo i bordi", "https://recensiamomusica.com/solchi-parliamo-di-lungo-i-bordi-dei-massimo-volume/", "Solchi series deep-dive on Lungo i bordi."),
    ("website", "Medium (EN) — Massimo Volume: Time Running Along the Edges", "https://eliaalovisi.medium.com/massimo-volume-time-running-along-the-edges-9d969028dfcd", "English-language essay on the band."),
    ("website", "Rumore — tour e ristampa Stanze (2019)", "https://rumoremag.com/2019/10/31/massimo-volume-tour-ristampa-stanze/", "First-ever Stanze reissue announcement, remastered from tapes."),
    # --- Discography / reference ---
    ("purchase", "Discogs — Demo Nero cassette (1992)", "https://www.discogs.com/release/5408615-Massimo-Volume-Massimo-Volume", "Original 1992 cassette entry with song-history notes."),
    ("purchase", "Discogs — Lungo i bordi 2013 vinyl reissue (Tannen Records)", "https://www.discogs.com/release/5092482-Massimo-Volume-Lungo-I-Bordi", "Limited 500 hand-numbered copies reissue."),
    ("website", "Genius — Demo Nero tracklist & notes", "https://genius.com/albums/Massimo-volume/Demo-nero", "Tracklist with notes on the black-cassette circulation."),
    ("archive", "Wikipedia IT — Stanze (album)", "https://it.wikipedia.org/wiki/Stanze_(Massimo_Volume)", "Album article with demo-song history."),
    ("archive", "Wikipedia IT — Lungo i bordi (album)", "https://it.wikipedia.org/wiki/Lungo_i_bordi", "Album article."),
    ("streaming", "Spotify — Massimo Volume artist", "https://open.spotify.com/artist/24GE8PrrmxG6XocV1UQPmP", "Official streaming, 13.6k monthly listeners."),
    ("website", "MusicBrainz — Da Qui release", "https://musicbrainz.org/release/60ecb50c-f659-30e9-b028-a8ed867f43f9", "Full credits: Valerio Soave prod., Steve Piccolo guest."),
    ("website", "Album of the Year — Stanze", "https://www.albumoftheyear.org/album/182663-massimo-volume-stanze.php", "Aggregator page with full discography links."),
]

band = Band.objects.get(id=BAND_ID)
existing = set(band.links.values_list("url", flat=True))

added, skipped = [], []
for lt, title, url, desc in NEW_LINKS:
    if url in existing:
        skipped.append(url)
        continue
    Link.objects.create(band=band, link_type=lt, title=title, url=url, description=desc)
    added.append(url)

print("added:", len(added))
print("skipped (dupes):", len(skipped))
for s in skipped:
    print("  DUP:", s)

# --- Fanzine reviews (Rumore magazine, id 30) ---
rumore = Fanzine.objects.filter(name__icontains="Rumore").first()
print("rumore fanzine:", rumore)
if rumore:
    fr1, c1 = FanzineReview.objects.get_or_create(
        band=band, fanzine=rumore, digitized_url="https://rumoremag.com/2019/01/19/massimo-volume-dettagli-nuovo-album/",
        defaults=dict(
            year=2019,
            review_text="Annuncio e dettagli del nuovo album 'Il Nuotatore' (La Tempesta): prima uscita come trio, tour nei teatri, tracklist completa.",
            notes="Online article on rumoremag.com (Rumore magazine official site).",
        ),
    )
    print("fanzine review 1:", fr1.id, "created:", c1)
    fr2, c2 = FanzineReview.objects.get_or_create(
        band=band, fanzine=rumore, digitized_url="https://rumoremag.com/2019/10/31/massimo-volume-tour-ristampa-stanze/",
        defaults=dict(
            year=2019,
            review_text="Prima ristampa mai realizzata di 'Stanze' (1993): remaster dai nastri, formato digitale, vinile e CD, nuovo tour.",
            notes="Online article on rumoremag.com (Rumore magazine official site).",
        ),
    )
    print("fanzine review 2:", fr2.id, "created:", c2)

# --- Final count ---
band.refresh_from_db()
print("FINAL LINK COUNT:", band.links.count())
