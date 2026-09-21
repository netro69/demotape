# Created-by: forge | Date: 2026-09-20
"""
Audio Archive Downloader for Demotape.
Queries DB for bands with downloadable links but no local audio.
Downloads audio from YouTube, Bandcamp, Internet Archive, and direct MP3 links.

Usage:
    cd ~/Projects/demotape && source .venv/bin/activate && python audio_archiver.py
"""

import os
import sys
import json
import time
import hashlib
import logging
import tempfile
import subprocess
import traceback
from pathlib import Path
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demotape.settings')
sys.path.insert(0, '/home/ubuntu/Projects/demotape')

import django
django.setup()

import requests
from django.conf import settings
from django.core.files import File
from django.db.models import Q
from django.utils.text import slugify

from apps.core.models import Band, Link, Release, Track

# Constants
MAX_DOWNLOADS_PER_RUN = 5
DELAY_BETWEEN_DOWNLOADS = 3  # seconds
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
MAX_FAILURES = 3

BASE_DIR = Path('/home/ubuntu/Projects/demotape')
DATA_DIR = BASE_DIR / 'data'
DEDUP_FILE = DATA_DIR / 'downloaded_urls.json'
LOG_FILE = Path.home() / 'Documents/Obsidian/Vault/projects/demotape-archive-log.md'

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)


def load_dedup_store():
    """Load URL deduplication store."""
    if DEDUP_FILE.exists():
        with open(DEDUP_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_dedup_store(store):
    """Save URL deduplication store."""
    with open(DEDUP_FILE, 'w') as f:
        json.dump(store, f, indent=2)


def url_hash(url):
    """Generate SHA256 hash of URL for deduplication."""
    return hashlib.sha256(url.encode('utf-8')).hexdigest()


def log_to_file(band_name, url, status, detail):
    """Append entry to archive log file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = (
        f"\n## {timestamp}\n"
        f"- **Band:** {band_name}\n"
        f"- **URL:** {url}\n"
        f"- **Status:** {status}\n"
        f"- **Detail:** {detail}\n"
    )

    log_path = Path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if log_path.exists():
        with open(log_path, 'a') as f:
            f.write(entry)
    else:
        with open(log_path, 'w') as f:
            f.write("# Demotape Archive Download Log\n\n")
            f.write(entry)


def get_bands_needing_audio():
    """
    Query bands that have downloadable links but no local audio tracks.
    Returns QuerySet of Band objects.
    """
    downloadable_types = ['video', 'streaming', 'archive']

    # Bands with published status that have downloadable links
    bands_with_links = Band.objects.filter(
        status='published',
        links__link_type__in=downloadable_types
    ).distinct()

    # Exclude bands that already have tracks with audio_file populated
    bands_with_audio = Band.objects.filter(
        status='published',
    ).filter(
        ~Q(releases__tracks__audio_file='') &
        Q(releases__tracks__audio_file__isnull=False)
    ).distinct()

    result = bands_with_links.exclude(
        id__in=bands_with_audio.values_list('id', flat=True)
    )

    return result


def get_links_for_band(band):
    """
    Get downloadable links for a band, ordered by priority.
    Priority: video (YouTube) > streaming (Bandcamp) > archive (IA) > direct MP3
    """
    downloadable_types = ['video', 'streaming', 'archive']
    return band.links.filter(
        link_type__in=downloadable_types
    ).order_by('link_type')


def download_with_ytdlp(url, output_path):
    """Download audio using yt-dlp CLI. Returns (title, actual_file_path)."""
    output_template = str(output_path.with_suffix(''))

    cmd = [
        'yt-dlp',
        '--format', 'bestaudio/best',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '192',
        '--output', f'{output_template}.%(ext)s',
        '--max-filesize', str(MAX_FILE_SIZE),
        '--quiet',
        '--no-warnings',
        '--print', 'title',
        url,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp failed (exit {result.returncode}): {result.stderr.strip()}")

    # Parse title from stdout (first line)
    title = result.stdout.strip().split('\n')[0] if result.stdout.strip() else 'Unknown Track'

    # Find the actual output file
    actual_path = output_path.with_suffix('.mp3')
    if not actual_path.exists():
        # yt-dlp may have used a sanitized filename
        candidates = list(output_path.parent.glob(f"{output_path.stem}*.mp3"))
        if candidates:
            actual_path = candidates[0]
        else:
            raise FileNotFoundError(f"yt-dlp output not found for {url}")

    return title, actual_path


def download_direct(url, output_path):
    """Download direct MP3 link with streaming. Returns actual_file_path."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }

    with requests.get(url, stream=True, headers=headers, timeout=60) as resp:
        resp.raise_for_status()

        # Check content length
        content_length = resp.headers.get('Content-Length')
        if content_length and int(content_length) > MAX_FILE_SIZE:
            raise ValueError(f"File too large: {content_length} bytes (max {MAX_FILE_SIZE})")

        # Check content type
        content_type = resp.headers.get('Content-Type', '')
        if 'audio' not in content_type and 'octet-stream' not in content_type:
            raise ValueError(f"Unexpected content type: {content_type}")

        # Download to temp file first
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            downloaded = 0
            for chunk in resp.iter_content(chunk_size=8192):
                downloaded += len(chunk)
                if downloaded > MAX_FILE_SIZE:
                    tmp.close()
                    os.unlink(tmp.name)
                    raise ValueError(f"Download exceeded max size: {MAX_FILE_SIZE}")
                tmp.write(chunk)
            tmp_path = tmp.name

    # Move to final location
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_path = output_path.with_suffix('.mp3')
    os.rename(tmp_path, final_path)

    return final_path


def get_or_create_release(band, source_hint='Archive Downloads'):
    """Get or create a digital release for archive downloads."""
    release = band.releases.filter(
        title__icontains='Archive Downloads',
        format='digital'
    ).first()

    if not release:
        release_slug = slugify(f"{band.slug}-archive-downloads")
        base_slug = release_slug
        counter = 1
        while Release.objects.filter(slug=release_slug).exists():
            release_slug = f"{base_slug}-{counter}"
            counter += 1

        release = Release.objects.create(
            band=band,
            title=source_hint,
            slug=release_slug,
            format='digital',
            year=datetime.now().year,
            status='published',
        )
        logger.info(f"Created release: {release.title} for {band.name}")

    return release


def create_track(release, title, audio_file_path):
    """Create a Track object with the downloaded audio file."""
    last_track = release.tracks.order_by('-track_number').first()
    next_number = (last_track.track_number + 1) if last_track else 1

    track_slug = slugify(title)[:50]

    track = Track(
        release=release,
        title=title[:255],
        track_number=next_number,
        status='published',
    )

    with open(audio_file_path, 'rb') as f:
        filename = f"{next_number:02d}_{track_slug}.mp3"
        track.audio_file.save(filename, File(f), save=False)

    track.save()
    logger.info(f"Created track: {track.title} (#{track.track_number}) for {release.band.name}")
    return track


def process_band(band, dedup_store, download_count):
    """
    Process a single band: find links, download audio, create tracks.
    Returns (new_download_count, should_continue)
    """
    logger.info(f"\nProcessing band: {band.name} (id={band.id})")

    links = get_links_for_band(band)
    if not links.exists():
        logger.info(f"No downloadable links for {band.name}")
        return download_count, True

    failure_counts = {}

    for link in links:
        if download_count >= MAX_DOWNLOADS_PER_RUN:
            logger.info(f"Reached max downloads per run ({MAX_DOWNLOADS_PER_RUN})")
            return download_count, False

        url = link.url
        url_h = url_hash(url)

        # Check dedup
        if url_h in dedup_store:
            logger.info(f"Skipping (already processed): {url}")
            continue

        # Check failure count
        if failure_counts.get(url, 0) >= MAX_FAILURES:
            logger.info(f"Skipping (too many failures): {url}")
            continue

        logger.info(f"Downloading: {url}")

        try:
            # Determine output path
            output_dir = Path(settings.MEDIA_ROOT) / 'audio' / band.slug
            output_dir.mkdir(parents=True, exist_ok=True)
            temp_path = output_dir / f"temp_{url_h[:12]}"

            # Determine download method
            url_lower = url.lower()
            is_ytdlp = (
                link.link_type == 'video' or
                'youtube' in url_lower or
                'vimeo' in url_lower or
                (link.link_type == 'streaming' and 'bandcamp' in url_lower)
            )
            is_direct_mp3 = (
                url_lower.endswith('.mp3') or
                'promodj' in url_lower or
                'punkdownload' in url_lower or
                'anarcho-punk' in url_lower or
                ('archive.org' in url_lower and '.mp3' in url_lower)
            )

            if is_ytdlp:
                title, actual_path = download_with_ytdlp(url, temp_path)
            elif is_direct_mp3:
                actual_path = download_direct(url, temp_path)
                title = link.title or f"{band.name} - {url.rstrip('/').split('/')[-1]}"
            else:
                # Default to yt-dlp for unknown types
                title, actual_path = download_with_ytdlp(url, temp_path)

            # Verify file
            if not actual_path.exists():
                raise FileNotFoundError(f"Downloaded file not found: {actual_path}")

            file_size = actual_path.stat().st_size
            if file_size > MAX_FILE_SIZE:
                actual_path.unlink()
                raise ValueError(f"File too large: {file_size} bytes")

            if file_size == 0:
                actual_path.unlink()
                raise ValueError("Downloaded file is empty")

            # Get or create release
            release = get_or_create_release(band)

            # Create track
            track = create_track(release, title, actual_path)

            # Clean up temp file if different
            if temp_path.exists() and temp_path != actual_path:
                temp_path.unlink()

            # Update dedup store
            dedup_store[url_h] = {
                'url': url,
                'downloaded_at': datetime.now().isoformat(),
                'file': str(track.audio_file.name),
                'status': 'success',
                'band': band.name,
            }
            save_dedup_store(dedup_store)

            # Log success
            log_to_file(band.name, url, 'SUCCESS',
                        f"File: {track.audio_file.name}, Size: {file_size} bytes")

            download_count += 1
            logger.info(f"Success: {title} ({file_size} bytes)")

            # Rate limiting
            time.sleep(DELAY_BETWEEN_DOWNLOADS)

        except Exception as e:
            failure_counts[url] = failure_counts.get(url, 0) + 1
            error_msg = f"{type(e).__name__}: {str(e)}"
            tb = traceback.format_exc()
            logger.error(f"Failed to download {url}: {error_msg}")
            logger.debug(tb)

            # Update dedup store with failure
            dedup_store[url_h] = {
                'url': url,
                'downloaded_at': datetime.now().isoformat(),
                'status': 'failed',
                'error': error_msg,
                'failure_count': failure_counts[url],
                'band': band.name,
            }
            save_dedup_store(dedup_store)

            # Log failure
            log_to_file(band.name, url, 'FAILURE',
                        f"{error_msg}\n```\n{tb}\n```")

            # Clean up temp files
            for p in [temp_path, temp_path.with_suffix('.mp3')]:
                if p.exists():
                    try:
                        p.unlink()
                    except Exception:
                        pass

            continue

    return download_count, True


def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("AUDIO ARCHIVE DOWNLOADER")
    logger.info("=" * 60)

    # Load dedup store
    dedup_store = load_dedup_store()
    logger.info(f"Loaded dedup store: {len(dedup_store)} URLs already processed")

    # Get bands needing audio
    bands = get_bands_needing_audio()
    band_count = bands.count()
    logger.info(f"Bands needing audio: {band_count}")

    if band_count == 0:
        logger.info("No bands need downloads. Exiting.")
        return

    download_count = 0
    processed_count = 0

    for band in bands:
        if download_count >= MAX_DOWNLOADS_PER_RUN:
            logger.info(f"Reached max downloads per run ({MAX_DOWNLOADS_PER_RUN}). Stopping.")
            break

        download_count, should_continue = process_band(band, dedup_store, download_count)
        processed_count += 1

        if not should_continue:
            break

    logger.info("=" * 60)
    logger.info(f"COMPLETE: Processed {processed_count} bands, downloaded {download_count} tracks")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
