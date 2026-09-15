"""
Apply structured research findings to the Demotape database.

Usage:
    python manage.py apply_findings <findings.json>

Findings JSON format:
{
  "findings": [
    {
      "band_name": "Bartòk",
      "links": [
        {"url": "...", "link_type": "video", "title": "...", "description": "..."}
      ],
      "bio_additions": "...",
      "connections": [
        {"to_band": "Clark Nova", "connection_type": "scene_peer", "notes": "..."}
      ],
      "releases": [
        {"title": "...", "year": 1995, "format": "demotape", "label": "..."}
      ],
      "genre_tags": ["punk", "hardcore"],
      "website": "...",
      "discogs_id": "..."
    }
  ]
}

Idempotent: skips duplicate URLs, merges bio additions, deduplicates connections.
"""

import json
import sys
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.core.models import (
    Band,
    Link,
    BandConnection,
    Release,
    Label,
    GenreTag,
    Status,
    ReleaseFormat,
)


# Valid link types from the Link model
VALID_LINK_TYPES = {
    "video", "social", "shop", "image", "article", "forum", "music",
}

# Valid connection types from BandConnection model
VALID_CONNECTION_TYPES = {
    "scene_peer", "label_mate", "influenced_by", "split_from",
    "side_project", "touring_partner", "producer",
}

# Valid release formats
VALID_RELEASE_FORMATS = {
    "vinyl", "cd", "demotape", "cassette", "digital",
}


class Command(BaseCommand):
    help = "Apply structured research findings (JSON) to the Demotape database"

    def add_arguments(self, parser):
        parser.add_argument("findings_file", type=str, help="Path to findings JSON file")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without writing to database",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Print detailed change log",
        )

    def handle(self, *args, **options):
        findings_path = Path(options["findings_file"])
        dry_run = options["dry_run"]
        verbose = options["verbose"]

        if not findings_path.exists():
            self.stderr.write(f"ERROR: File not found: {findings_path}")
            sys.exit(1)

        with open(findings_path) as f:
            data = json.load(f)

        findings = data.get("findings", [])
        if not findings:
            self.stderr.write("ERROR: No findings in JSON file")
            sys.exit(1)

        self.stdout.write(f"Processing {len(findings)} band findings...")

        stats = {
            "bands_processed": 0,
            "links_added": 0,
            "links_skipped": 0,
            "bios_updated": 0,
            "connections_added": 0,
            "connections_skipped": 0,
            "releases_added": 0,
            "releases_skipped": 0,
            "genres_added": 0,
            "labels_added": 0,
            "bands_not_found": [],
            "errors": [],
        }

        for finding in findings:
            band_name = finding.get("band_name", "").strip()
            if not band_name:
                continue

            try:
                band = Band.objects.get(name__iexact=band_name)
            except Band.DoesNotExist:
                stats["bands_not_found"].append(band_name)
                if verbose:
                    self.stdout.write(f"  SKIP: Band not found: {band_name}")
                continue

            stats["bands_processed"] += 1

            # --- LINKS ---
            for link_data in finding.get("links", []):
                url = link_data.get("url", "").strip()
                if not url:
                    continue

                link_type = link_data.get("link_type", "article")
                if link_type not in VALID_LINK_TYPES:
                    link_type = "article"

                # Idempotency: skip if URL already exists for this band
                if Link.objects.filter(band=band, url=url).exists():
                    stats["links_skipped"] += 1
                    if verbose:
                        self.stdout.write(f"  SKIP link (exists): {band.name} -> {url}")
                    continue

                if not dry_run:
                    Link.objects.create(
                        band=band,
                        url=url,
                        link_type=link_type,
                        title=link_data.get("title", ""),
                        description=link_data.get("description", ""),
                    )
                stats["links_added"] += 1
                if verbose:
                    self.stdout.write(f"  ADD link: {band.name} -> {url}")

            # --- BIO ---
            bio_addition = finding.get("bio_additions", "").strip()
            if bio_addition:
                current_bio = band.bio or ""
                # Avoid duplicating if the addition is already in the bio
                if bio_addition not in current_bio:
                    if not dry_run:
                        band.bio = f"{current_bio}\n\n{bio_addition}".strip()
                        band.save(update_fields=["bio"])
                    stats["bios_updated"] += 1
                    if verbose:
                        self.stdout.write(f"  UPDATE bio: {band.name}")

            # --- WEBSITE ---
            website = finding.get("website", "").strip()
            if website and not band.website:
                if not dry_run:
                    band.website = website
                    band.save(update_fields=["website"])
                if verbose:
                    self.stdout.write(f"  SET website: {band.name} -> {website}")

            # --- DISCOGS ID ---
            discogs_id = finding.get("discogs_id", "").strip()
            if discogs_id and not band.discogs_id:
                if not dry_run:
                    band.discogs_id = discogs_id
                    band.save(update_fields=["discogs_id"])
                if verbose:
                    self.stdout.write(f"  SET discogs_id: {band.name} -> {discogs_id}")

            # --- CONNECTIONS ---
            for conn_data in finding.get("connections", []):
                to_band_name = conn_data.get("to_band", "").strip()
                if not to_band_name:
                    continue

                try:
                    to_band = Band.objects.get(name__iexact=to_band_name)
                except Band.DoesNotExist:
                    if verbose:
                        self.stdout.write(f"  SKIP connection: {to_band_name} not found")
                    continue

                conn_type = conn_data.get("connection_type", "scene_peer")
                if conn_type not in VALID_CONNECTION_TYPES:
                    conn_type = "scene_peer"

                # Idempotency: skip if connection already exists
                if BandConnection.objects.filter(
                    from_band=band, to_band=to_band, connection_type=conn_type
                ).exists():
                    stats["connections_skipped"] += 1
                    if verbose:
                        self.stdout.write(f"  SKIP connection (exists): {band.name} -> {to_band_name}")
                    continue

                if not dry_run:
                    BandConnection.objects.create(
                        from_band=band,
                        to_band=to_band,
                        connection_type=conn_type,
                        notes=conn_data.get("notes", ""),
                        source=conn_data.get("source", ""),
                    )
                stats["connections_added"] += 1
                if verbose:
                    self.stdout.write(f"  ADD connection: {band.name} -> {to_band_name} ({conn_type})")

            # --- RELEASES ---
            for rel_data in finding.get("releases", []):
                title = rel_data.get("title", "").strip()
                if not title:
                    continue

                year = rel_data.get("year")
                if not year:
                    continue

                # Idempotency: skip if release with same title+year exists
                if Release.objects.filter(band=band, title__iexact=title, year=year).exists():
                    stats["releases_skipped"] += 1
                    if verbose:
                        self.stdout.write(f"  SKIP release (exists): {band.name} - {title} ({year})")
                    continue

                fmt = rel_data.get("format", "demotape")
                if fmt not in VALID_RELEASE_FORMATS:
                    fmt = "demotape"

                label_name = rel_data.get("label", "").strip()
                if label_name and not dry_run:
                    label_obj, created = Label.objects.get_or_create(
                        name__iexact=label_name,
                        defaults={"name": label_name, "slug": slugify(label_name)},
                    )
                    if created:
                        stats["labels_added"] += 1

                if not dry_run:
                    Release.objects.create(
                        band=band,
                        title=title,
                        slug=f"{slugify(band.name)}-{slugify(title)}-{year}",
                        format=fmt,
                        year=year,
                        label=label_name,
                        catalog_number=rel_data.get("catalog_number", ""),
                        description=rel_data.get("description", ""),
                    )
                stats["releases_added"] += 1
                if verbose:
                    self.stdout.write(f"  ADD release: {band.name} - {title} ({year})")

            # --- GENRE TAGS ---
            for tag_name in finding.get("genre_tags", []):
                tag_name = tag_name.strip()
                if not tag_name:
                    continue

                if not dry_run:
                    tag_obj, created = GenreTag.objects.get_or_create(
                        name__iexact=tag_name,
                        defaults={"name": tag_name, "slug": slugify(tag_name)},
                    )
                    if created:
                        stats["genres_added"] += 1
                    band.genre_tags.add(tag_obj)
                else:
                    if not GenreTag.objects.filter(name__iexact=tag_name).exists():
                        stats["genres_added"] += 1
                if verbose:
                    self.stdout.write(f"  ADD genre: {band.name} -> {tag_name}")

        # --- SUMMARY ---
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("APPLY FINDINGS SUMMARY")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Bands processed:     {stats['bands_processed']}")
        self.stdout.write(f"Links added:         {stats['links_added']}")
        self.stdout.write(f"Links skipped:       {stats['links_skipped']}")
        self.stdout.write(f"Bios updated:        {stats['bios_updated']}")
        self.stdout.write(f"Connections added:   {stats['connections_added']}")
        self.stdout.write(f"Connections skipped: {stats['connections_skipped']}")
        self.stdout.write(f"Releases added:      {stats['releases_added']}")
        self.stdout.write(f"Releases skipped:    {stats['releases_skipped']}")
        self.stdout.write(f"Genres added:        {stats['genres_added']}")
        self.stdout.write(f"Labels added:        {stats['labels_added']}")

        if stats["bands_not_found"]:
            self.stdout.write(f"\nBands NOT found ({len(stats['bands_not_found'])}):")
            for name in stats["bands_not_found"]:
                self.stdout.write(f"  - {name}")

        if stats["errors"]:
            self.stdout.write(f"\nErrors ({len(stats['errors'])}):")
            for err in stats["errors"]:
                self.stdout.write(f"  - {err}")

        if dry_run:
            self.stdout.write("\n*** DRY RUN — no changes written to database ***")
        else:
            self.stdout.write("\nChanges committed to database.")
