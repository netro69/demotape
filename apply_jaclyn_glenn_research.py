# Created-by: the-architect | Date: 2026-09-17
# Session: subagent-research
#!/usr/bin/env python3
"""
Apply all research findings for Jaclyn Glenn (Band ID: 118).

Adds: links (streaming, social, video, website, archive),
releases (singles/covers), and updates band fields (bio_en, active_years, website, city).

Run: cd ~/Projects/demotape && .venv/bin/python manage.py shell < apply_jaclyn_glenn_research.py
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

print("\n=== JACLYN GLENN RESEARCH APPLICATION ===\n")

# Get the band
jaclyn = Band.objects.get(id=118)
print(f"Band: {jaclyn.name} (ID: {jaclyn.pk})\n")

# =========================================================================
# 1. Update Band Fields
# =========================================================================
print("--- Updating Band Fields ---")

jaclyn.active_years = "2016-present"
jaclyn.bio_en = (
    "Jaclyn Glenn (also Jaclyn Frank) is a Los Angeles-based YouTuber and "
    "singer-songwriter from Studio City, California. She gained fame through her "
    "YouTube channel covering religious commentary, atheism, social activism, "
    "relationships, and lifestyle vlogs. She also performs and releases music — "
    "both original songs and covers — distributed through YouTube, Spotify, and "
    "other streaming platforms. She is engaged to David Michael Frank (Band 116) "
    "of Future Sunsets. Primary career is content creation; music is a side pursuit."
)
jaclyn.website = "http://jaclynglenn.com/"
jaclyn.city = "Studio City, Los Angeles, California"
jaclyn.save()
changes["fields_updated"] += 1
print(f"  Updated: active_years, bio_en, website, city")

# Add genre tags
genre_names = ["Pop", "Covers", "Singer-Songwriter", "YouTube", "Content Creator"]
for gname in genre_names:
    g, created = GenreTag.objects.get_or_create(
        slug=slugify(gname),
        defaults={"name": gname}
    )
    jaclyn.genre_tags.add(g)
    if created:
        print(f"  + GENRE: {gname}")
    else:
        print(f"  = GENRE (exists): {gname}")

# =========================================================================
# 2. Add Labels
# =========================================================================
print("\n--- Adding Labels ---")
# Independent/self-released

# =========================================================================
# 3. Add Missing Links
# =========================================================================
print("\n--- Adding Links ---")

# Official Website
add_link(jaclyn, "website", "http://jaclynglenn.com/", "Official Website", "Official Jaclyn Glenn website", is_primary=True)

# Social Media
add_link(jaclyn, "social", "https://www.instagram.com/jaclynglenn/", "Instagram", "Official Instagram profile")
add_link(jaclyn, "social", "https://twitter.com/jaclynglenn", "Twitter/X", "Official Twitter account")
add_link(jaclyn, "social", "https://www.facebook.com/JaclynGlenn", "Facebook", "Official Facebook page")
add_link(jaclyn, "social", "https://www.tiktok.com/@jaclynglenn", "TikTok", "TikTok profile")

# Streaming Links
add_link(jaclyn, "streaming", "https://open.spotify.com/artist/2mV9y2ChZl1J7GIVyziR4K", "Spotify", "Official Spotify artist page; 4K monthly listeners")
add_link(jaclyn, "streaming", "https://soundcloud.com/jaclynglenn", "SoundCloud", "SoundCloud profile")
add_link(jaclyn, "streaming", "https://music.apple.com/us/artist/jaclyn-glenn/1440444103", "Apple Music", "Apple Music artist page")

# Video Links
add_link(jaclyn, "video", "https://www.youtube.com/user/JaclynGlenn", "YouTube (Main Channel)", "826K+ subscribers; music + vlogs")
add_link(jaclyn, "video", "https://www.youtube.com/watch?v=H8MtReHo3R4", "Head Above Water (Cover)", "Avril Lavigne cover music video")
add_link(jaclyn, "video", "https://www.youtube.com/watch?v=5z7Sag38I2k", "Rain on Me (Cover)", "Lady Gaga/Ariana Grande cover with David Michael Frank")

# Fan/Secondary Platforms
add_link(jaclyn, "purchase", "https://www.patreon.com/Jaclyn", "Patreon", "Fan membership; 1,080 members")
add_link(jaclyn, "purchase", "https://www.cameo.com/jaclynglenn/book", "Cameo", "Personalized video messages")

# Archive / Reference
add_link(jaclyn, "archive", "https://www.shazam.com/artist/jaclyn-glenn/2mV9y2ChZl1J7GIVyziR4K", "Shazam", "Artist info and music videos")
add_link(jaclyn, "archive", "https://www.deezer.com/en/artist/9733602", "Deezer", "Artist profile on Deezer")
add_link(jaclyn, "archive", "https://genius.com/artists/Jaclyn-glenn", "Genius", "Lyrics catalog")
add_link(jaclyn, "archive", "https://secondhandsongs.com/artist/109124", "SecondHandSongs", "Covers database")
add_link(jaclyn, "archive", "https://archive.org/details/youtube-jeX64VeME8w", "Internet Archive", "Talk on coming out as atheist")

# =========================================================================
# 4. Add Releases (Singles & Notable Covers)
# =========================================================================
print("\n--- Adding Releases ---")

# Original singles
add_release(jaclyn, "Hump Trump (feat. TeraBrite)", 2016, description="Political satire single; independent release")

# Cover singles (significant enough to catalog)
add_release(jaclyn, "Praying", 2018, description="Kesha cover; released Jan 29, 2018")
add_release(jaclyn, "Head Above Water", 2018, description="Avril Lavigne cover; released Oct 23, 2018")

# =========================================================================
# 5. Add Connections (beyond existing DMF → Jaclyn Glenn)
# =========================================================================
print("\n--- Adding Connections ---")

# Jaclyn Glenn collaborated with Social Repose
try:
    sr = Band.objects.filter(name__icontains="Social Repose").first()
    if sr:
        add_connection(jaclyn, sr, "collaboration", "Paris (Acapella) (2017)")
    else:
        print("  Social Repose not in database - skipping connection")
except Exception as e:
    print(f"  Error finding Social Repose: {e}")

# Jaclyn Glenn collaborated with MikelWJ
try:
    mwj = Band.objects.filter(name__icontains="MikelWJ").first()
    if mwj:
        add_connection(jaclyn, mwj, "collaboration", "Somebody That I Used To Know feature")
    else:
        print("  MikelWJ not in database - skipping connection")
except Exception as e:
    print(f"  Error finding MikelWJ: {e}")

# Future Sunsets connection (through Rain on Me / Broken & Beautiful)
try:
    fs = Band.objects.filter(name__icontains="Future Sunsets").first()
    if fs:
        add_connection(jaclyn, fs, "collaboration", "Rain on Me (2020), Broken & Beautiful (2020)")
    else:
        print("  Future Sunsets not in database - skipping connection")
except Exception as e:
    print(f"  Error finding Future Sunsets: {e}")

# =========================================================================
# SUMMARY
# =========================================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  Links added: {changes['links_added']}")
print(f"  Links skipped (exists): {changes['links_skipped']}")
print(f"  Releases added: {changes['releases_added']}")
print(f"  Releases skipped: {changes['releases_skipped']}")
print(f"  Connections added: {changes['connections_added']}")
print(f"  Connections skipped: {changes['connections_skipped']}")
print(f"  Labels added: {changes['labels_added']}")
print(f"  Fields updated: {changes['fields_updated']}")
print("=" * 60)
print("DONE")
