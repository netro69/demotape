#!/usr/bin/env python3
"""
Apply research findings for Lynn (id=109) to the Demotape database.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, os.path.expanduser('~/Projects/demotape'))
django.setup()

from apps.core.models import Band, Link, BandConnection, GenreTag

print("=" * 60)
print("APPLYING LYNN RESEARCH (id=109)")
print("=" * 60)

lynn = Band.objects.get(id=109)
print(f"\nTarget: {lynn.name} (id={lynn.id})")

# Update band info
lynn.bio = (
    "Israeli pop singer, songwriter, and producer. Began releasing music at age 17. "
    "Debut single \"Can't Let Go\" (August 2016) co-written and composed with producer "
    "Yoad Nevo (known for work with Sia, Goldfrapp, Morcheeba) at Nevo Sound Studios London. "
    "Follow-up singles: \"Rise High\" (March 2017, produced by Yoad Nevo), "
    "\"I Used to Cry\" (June 2017, anti-bullying message, went viral on Facebook), "
    "\"Paradise\" (July 2017, with Yoad Nevo remix via Spinnin' Records), "
    "\"Where Do We Go\" (January 2018), \"Lonely Hearts\" (October 2018), "
    "\"Look At Him Go\" (2019), \"Stay\" (2023, psytrance collaboration with Omiki & Skazi), "
    "\"Enemy\" (May 2024, produced by Amit Sagie), and \"Sinner\" (July 2026, from upcoming EP). "
    "Also featured vocalist on \"Survive\" by To You Mom: from the album 'We Are Lions' "
    "(Ghost Records, 2015). Collaborated with psytrance artists Asher Swissa (Skazi) "
    "on multiple tracks including \"Poison\", \"Savage\", and \"Restless\" (with Ahmet Kilic). "
    "Genre: Pop, Electronic, Psytrance (collaborations). Active 2015-present."
)
lynn.active_years = "2015-present"
lynn.save()
print(f"  Updated bio ({len(lynn.bio)} chars), active_years=2015-present")

# Add genre tags (use existing ones from DB)
genre_slugs = ["pop", "electronic", "psytrance", "synthpop", "dance"]
for gslug in genre_slugs:
    g = GenreTag.objects.filter(slug=gslug).first()
    if g:
        lynn.genre_tags.add(g)
    else:
        # Fallback: find by name
        gname = gslug.replace('-', ' ').title()
        g = GenreTag.objects.filter(name__iexact=gname).first()
        if g:
            lynn.genre_tags.add(g)
        else:
            g, created = GenreTag.objects.get_or_create(name=gname.lower(), defaults={'slug': gslug})
            lynn.genre_tags.add(g)
print(f"  Genre tags: {list(lynn.genre_tags.values_list('name', flat=True))}")

# Add links
links = [
    ("website", "Lynn Music Official Website", "https://www.lynnmusic.com/", "Official site"),
    ("streaming", "Spotify", "https://open.spotify.com/artist/7nzbcK2bzEtoMgTQAwHQVl", "199.9K monthly listeners"),
    ("streaming", "Apple Music", "https://music.apple.com/us/artist/lynn/1438537561", "Artist profile"),
    ("streaming", "SoundCloud", "https://soundcloud.com/lynnofficial", "Official SoundCloud"),
    ("social", "Instagram @lynnmusicnow", "https://www.instagram.com/lynnmusicnow/", "4.7K+ followers"),
    ("social", "X/Twitter @lynnmusicnow", "https://x.com/lynnmusicnow", "Singer-songwriter-producer"),
    ("social", "YouTube @LynnMusic", "https://www.youtube.com/@LynnMusic", "14.4K subscribers, 24+ videos"),
    ("video", "Can't Let Go (Debut Single)", "https://www.youtube.com/watch?v=vDYP7-8UBGU", "Aug 2016, debut single with Yoad Nevo"),
    ("video", "Rise High (Official Music Video)", "https://www.youtube.com/watch?v=vDYP7-8UBGU", "March 2017"),
    ("video", "Paradise (Yoad Nevo Remix)", "https://www.youtube.com/watch?v=wLVZjfVpWdA", "July 2017"),
    ("video", "Where Do We Go (Official Video)", "https://www.youtube.com/watch?v=BE5eNLEJ2rk", "Jan 2018"),
    ("video", "Lonely Hearts (Official Video)", "https://www.youtube.com/watch?v=-8Lh3r4H_t4", "Oct 2018"),
    ("video", "Enemy (Official Music Video)", "https://www.youtube.com/watch?v=DoqJU6RXQn4", "May 2024, produced by Amit Sagie"),
    ("video", "Sinner (Official Music Video)", "https://www.youtube.com/watch?v=sm0be0m_8II", "July 2026, from upcoming EP"),
    ("video", "We Were Never Okay (with David Micheal Frank)", "https://www.youtube.com/watch?v=Za4zK4dsa3M", "Collaboration track"),
    ("video", "Survive (feat. Lynn) - To You Mom:", "https://ghostrecords.bandcamp.com/track/survive", "Ghost Records, March 2015"),
    ("streaming", "Survive on Spotify", "https://open.spotify.com/track/3Y8H8RpGg8q2ywEwdjJYw2", "To You Mom: feat. Lynn"),
    ("video", "Stay - Omiki, Skazi & Lynn", "https://www.youtube.com/watch?v=a7tUtDEUCjU", "2023 psytrance collaboration"),
    ("streaming", "Stay on Spotify", "https://open.spotify.com/track/32gHdwjfwcyOGd0jW6xLnP", "Omiki, Skazi & Lynn"),
    ("video", "Poison - Asher Swissa & Lynn", "https://www.facebook.com/100044377541364/videos/1059049888929679/", "Aug 2024, Reborn Records"),
    ("archive", "Genius - Rise High Lyrics", "https://genius.com/Lynn-rise-high-lyrics", "Lyrics & credits"),
    ("archive", "Discogs - Lynn Music label", "https://www.discogs.com/label/676472-Lynn-Music-3", "Label page"),
    ("archive", "Spinnin' Records - Rise High", "https://spinninrecords.com/talentpool/artist/lynnmusic/track/2017-03-rise-high", "Second single"),
    ("archive", "Amazon Music", "https://music.amazon.de/artists/B09L8LNWCL/lynn", "Artist page"),
    ("archive", "Rockit - We Are Lions review", "https://www.rockit.it/toyoumom/album/we-are-lions/28053", "Italian music press"),
    ("archive", "Qobuz - We Are Lions", "https://www.qobuz.com/it-it/interpreter/to-you-mom-1/2134528", "Album page"),
    ("article", "Lynn Shares New Single 'Sinner'", "https://www.caesarlivenloud.com/2026/07/lynn-shares-new-single-sinner.html", "July 2026 review"),
    ("article", "Daily Dig: Lynn – musicismyradar", "https://themusicismyradar.wordpress.com/2017/07/21/daily-dig-lynn-lynnmusicnow/", "July 2017"),
    ("article", "Soundkartell - Rise High Review", "https://www.soundkartell.de/lynn/", "German music blog review"),
]

link_count = 0
skip_count = 0
for link_type, title, url, desc in links:
    existing = lynn.links.filter(url=url).first()
    if not existing:
        Link.objects.create(
            band=lynn,
            link_type=link_type,
            title=title,
            url=url,
            description=desc,
        )
        link_count += 1
        print(f"  + LINK [{link_type}]: {title}")
    else:
        skip_count += 1
        print(f"  = SKIP (exists): {title}")

# Add connections
connections = [
    ("To You Mom:", "collaboration", "Featured vocalist on 'Survive' from We Are Lions (2015)"),
    ("Ghost Records & Publishing S.n.C.", "label_mate", "Appeared on Ghost Records release GHST053 (To You Mom: - We Are Lions)"),
    ("Yoad Nevo", "collaboration", "Co-writer/producer on debut single 'Can't Let Go' and 'Rise High'"),
    ("Asher Swissa", "collaboration", "Featured vocalist on 'Poison', 'Savage', and psytrance tracks"),
    ("Omiki", "collaboration", "Vocalist on 'Stay' (2023) psytrance track with Omiki & Skazi"),
    ("David Micheal Frank", "collaboration", "Co-creator on 'We Were Never Okay'"),
    ("Casa Del Mirto", "scene_peer", "Connected via To You Mom: (origin) and Ghost Records scene"),
]

conn_count = 0
for target_name, conn_type, notes in connections:
    try:
        target = Band.objects.get(name=target_name)
        existing = BandConnection.objects.filter(
            from_band=lynn, to_band=target, connection_type=conn_type
        ).first()
        reverse = BandConnection.objects.filter(
            from_band=target, to_band=lynn, connection_type=conn_type
        ).first()
        if not existing and not reverse:
            BandConnection.objects.create(
                from_band=lynn,
                to_band=target,
                connection_type=conn_type,
                notes=notes,
            )
            conn_count += 1
            print(f"  + CONN: Lynn → {target_name} ({conn_type})")
        else:
            print(f"  = SKIP (exists): Lynn → {target_name}")
    except Band.DoesNotExist:
        print(f"  ! TARGET NOT FOUND: {target_name}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
lynn.refresh_from_db()
print(f"Links added: {link_count}, skipped: {skip_count}, total: {lynn.links.count()}")
print(f"Connections added: {conn_count}")
print(f"Connections from: {lynn.connections_from.count()}")
print(f"Connections to: {lynn.connections_to.count()}")
print(f"Genre tags: {list(lynn.genre_tags.values_list('name', flat=True))}")
print(f"Active years: {lynn.active_years}")
print(f"Bio length: {len(lynn.bio)} chars")
