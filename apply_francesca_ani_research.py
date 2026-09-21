# Created-by: agent | Date: 2026-09-17
# Session: subagent-research
#!/usr/bin/env python3
"""
Apply all research findings for Francesca Ani (Band ID: 119).

Adds: links (streaming, social, video, website, archive, purchase),
releases (discography), and updates band fields (bio_en, active_years,
discogs_id, website).

Run: cd ~/Projects/demotape && .venv/bin/python manage.py shell < apply_francesca_ani_research.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Release, Link, Label, BandConnection, GenreTag
from django.db.models import Count
from django.utils.text import slugify

changes = {
    "links_added": 0,
    "links_skipped": 0,
    "releases_added": 0,
    "releases_skipped": 0,
    "connections_added": 0,
    "connections_skipped": 0,
    "labels_added": 0,
    "labels_skipped": 0,
    "fields_updated": 0,
}


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
        print(f"  + LINK: {band.name} -> {link_type}: {url[:80]}")
    else:
        changes["links_skipped"] += 1
        print(f"  = SKIP (exists): {band.name} -> {url[:80]}")


def add_release(band, title, year, label_name="", description="", format_type="digital"):
    existing = Release.objects.filter(band=band, title=title).exists()
    if not existing:
        slug = slugify(f"{band.name}-{title}")
        if Release.objects.filter(slug=slug).exists():
            slug = f"{slug}-{year}"
        Release.objects.create(
            band=band,
            title=title,
            slug=slug,
            format=format_type,
            year=year,
            label=label_name,
            description=description,
            status="published",
        )
        changes["releases_added"] += 1
        print(f"  + RELEASE: {band.name} - {title} ({year})")
    else:
        changes["releases_skipped"] += 1
        print(f"  = SKIP (exists): {band.name} - {title}")


def get_or_create_label(name, city="", website=""):
    slug = slugify(name)
    label, created = Label.objects.get_or_create(
        slug=slug,
        defaults={
            "name": name,
            "city": city,
            "website": website,
            "status": "active",
        }
    )
    if created:
        changes["labels_added"] += 1
        print(f"  + LABEL: {name}")
    else:
        changes["labels_skipped"] += 1
        print(f"  = LABEL (exists): {name}")
    return label


def add_connection(from_band, to_band, connection_type, notes=""):
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
        )
        changes["connections_added"] += 1
        print(f"  + CONN: {from_band.name} -> {to_band.name} ({connection_type})")
    else:
        changes["connections_skipped"] += 1
        print(f"  = CONN (exists): {from_band.name} -> {to_band.name} ({connection_type})")


# =========================================================================
# MAIN
# =========================================================================

print("\n=== FRANCESCA ANI RESEARCH APPLICATION ===\n")

# Get the band
fran = Band.objects.get(id=119)
print(f"Band: {fran.name} (ID: {fran.pk})\n")

# =========================================================================
# 1. Update Band Fields
# =========================================================================
print("--- Updating Band Fields ---")

fran.active_years = "2014-present"
fran.bio_en = (
    "Francesca Ani (born Francesca Giorgianni, ~1999) is a Tampa, Florida-based "
    "Christian Contemporary singer-songwriter. She began performing at age 6 and "
    "initially performed country music before transitioning to Christian pop. "
    "In 2015 she won a Tampa Bay Talent Search. Her musical influences include "
    "Lauren Daigle and Carole King. She released her debut pop EP 'Open Your Arms' "
    "in 2016. She felt called to use her musical gifts for ministry and now focuses "
    "on Christian Contemporary music and youth worship. She works at a Catholic "
    "radio station in Tampa and serves as a music missionary with Catholic Mission Trips Inc. "
    "She has led mission trips to Harlan, KY; Lake Charles, LA; and Gallup, NM (Zuni reservation)."
)
fran.website = "https://francescaani.com/"
fran.city = "Tampa, Florida"
fran.save()
changes["fields_updated"] += 1
print(f"  Updated: active_years, bio_en, website, city")

# Add genre tags
genre_names = ["Christian Contemporary", "Pop", "Singer-Songwriter", "Worship"]
for gname in genre_names:
    g, created = GenreTag.objects.get_or_create(
        slug=slugify(gname),
        defaults={"name": gname}
    )
    fran.genre_tags.add(g)
    if created:
        print(f"  + GENRE: {gname}")
    else:
        print(f"  = GENRE (exists): {gname}")

# =========================================================================
# 2. Add Labels
# =========================================================================
print("\n--- Adding Labels ---")
# No known label for early releases — self-released/independent

# =========================================================================
# 3. Add Missing Links
# =========================================================================
print("\n--- Adding Links ---")

# Official Website
add_link(fran, "website", "https://francescaani.com/", "Official Website", "Official Francesca Ani website", is_primary=True)

# Social Media
add_link(fran, "social", "https://www.facebook.com/FrancescaAniii/", "Facebook", "Official Facebook page")
add_link(fran, "social", "https://www.instagram.com/p/COLSUpXhc7e/", "Instagram", "Instagram profile")

# Streaming Links
add_link(fran, "streaming", "https://open.spotify.com/artist/3Y2XCd5UPxNaJanzIGNsC3", "Spotify", "Official Spotify artist page")
add_link(fran, "streaming", "https://music.apple.com/us/artist/francesca-ani/1074158340", "Apple Music", "Official Apple Music artist page")
add_link(fran, "streaming", "https://music.youtube.com/channel/UCE01-IKBxfZ8zwHa7QQGr4Q", "YouTube Music", "YouTube Music channel")

# Video Links
add_link(fran, "video", "https://www.youtube.com/@FrancescaAni", "YouTube (Main)", "Official YouTube channel")
add_link(fran, "video", "https://www.youtube.com/channel/UCL9_md6DVyzz_aTx3zuLdDw", "YouTube (Channel)", "YouTube channel page")

# SoundCloud
add_link(fran, "streaming", "https://soundcloud.com/theoneandani", "SoundCloud", "SoundCloud profile")

# Archive / Reference
add_link(fran, "archive", "https://www.shazam.com/artist/francesca-ani/1074158340", "Shazam", "Artist info and music videos")
add_link(fran, "archive", "https://www.whosampled.com/Francesca-Ani/", "WhoSampled", "Covers and samples")
add_link(fran, "archive", "https://secondhandsongs.com/artist/109124+130448", "SecondHandSongs", "Covers database")
add_link(fran, "archive", "https://www.sofarsounds.com/artists/francesca-ani", "Sofar Sounds", "Live performances")
add_link(fran, "archive", "https://www.concertarchives.org/bands/francesca-ani", "Concert Archives", "Live performance history")
add_link(fran, "archive", "https://www.musixmatch.com/ko/artist/Francesca-Ani", "Musixmatch", "Lyrics database")
add_link(fran, "archive", "https://songbpm.com/@francesca-ani", "SongBPM", "Song BPM data")

# Press / Media
add_link(fran, "archive", "https://www.cleartrackstudios.com/about/testimonials", "Clear Track Studios", "Testimonial about working with producer Spencer Bradham")
add_link(fran, "archive", "https://catholicmissiontrips.net/fran-ani/", "Catholic Mission Trips", "Music missionary feature")

# =========================================================================
# 4. Add Releases (Discography)
# =========================================================================
print("\n--- Adding Releases ---")

# EPs
add_release(fran, "Open Your Arms", 2016, "", "Debut pop EP; 3 songs", "digital")

# Singles
add_release(fran, "This Christmas (feat. Ruben Colaci)", 2016, "", "Christmas single", "digital")
add_release(fran, "It Ain't Me", 2017, "", "Single", "digital")
add_release(fran, "Dream", 2017, "", "Single", "digital")
add_release(fran, "I'm Stuck", 2017, "", "Single", "digital")
add_release(fran, "What About Us", 2017, "", "Single", "digital")
add_release(fran, "Lay It on Me", 2017, "", "Single", "digital")
add_release(fran, "Anywhere", 2018, "", "Single", "digital")
add_release(fran, "Rescue", 2019, "", "Single; Lauren Daigle cover", "digital")
add_release(fran, "Build My Life", 2020, "", "Single; worship track", "digital")

# =========================================================================
# 5. Add Band Connections (scene peers / influences)
# =========================================================================
print("\n--- Adding Connections ---")

# Lauren Daigle is a major influence
try:
    lauren = Band.objects.get(name__icontains="Lauren Daigle")
    add_connection(fran, lauren, "influence", "Lauren Daigle is a primary musical influence; covered 'Rescue'")
except Band.DoesNotExist:
    print(f"  = SKIP: Lauren Daigle not in DB")

# =========================================================================
# 6. Summary
# =========================================================================
print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print(f"  Links added:       {changes['links_added']}")
print(f"  Links skipped:     {changes['links_skipped']}")
print(f"  Releases added:    {changes['releases_added']}")
print(f"  Releases skipped:  {changes['releases_skipped']}")
print(f"  Connections added: {changes['connections_added']}")
print(f"  Connections skipped: {changes['connections_skipped']}")
print(f"  Labels added:      {changes['labels_added']}")
print(f"  Labels skipped:    {changes['labels_skipped']}")
print(f"  Fields updated:    {changes['fields_updated']}")

# Final count check
fran.refresh_from_db()
print(f"\nFinal counts for {fran.name}:")
print(f"  Links: {fran.links.count()}")
print(f"  Releases: {fran.releases.count()}")
print(f"  Connections (from): {fran.connections_from.count()}")
print(f"  Connections (to): {fran.connections_to.count()}")
