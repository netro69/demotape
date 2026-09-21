from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Status(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PUBLISHED = 'published', 'Published'
    FLAGGED = 'flagged', 'Flagged'


class ImageType(models.TextChoices):
    BAND_PHOTO = 'band_photo', 'Band Photo'
    COVER = 'cover', 'Cover Art'
    FLYER = 'flyer', 'Gig Flyer'
    POSTER = 'poster', 'Concert Poster'
    INSERT = 'insert', 'Insert/Booklet'
    PROMO = 'promo', 'Promo Photo'
    OTHER = 'other', 'Other'


class ReleaseFormat(models.TextChoices):
    VINYL = 'vinyl', 'Vinyl'
    CD = 'cd', 'CD'
    DEMOTAPE = 'demotape', 'Demotape'
    CASSETTE = 'cassette', 'Cassette'
    DIGITAL = 'digital', 'Digital'


class UserRole(models.TextChoices):
    FREE = 'free', 'Free'
    REGISTERED = 'registered', 'Registered'
    PRIVILEGED = 'privileged', 'Privileged'
    ADMIN = 'admin', 'Admin'


class Band(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    city = models.CharField(max_length=255, blank=True)
    active_years = models.CharField(max_length=50, blank=True)
    genre_tags = models.ManyToManyField('GenreTag', blank=True, related_name='bands')
    bio = models.TextField(blank=True)
    bio_en = models.TextField(blank=True)
    website = models.URLField(blank=True)
    discogs_id = models.CharField(max_length=100, blank=True)
    musicbrainz_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='bands_created')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class GenreTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Release(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='releases')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    format = models.CharField(max_length=20, choices=ReleaseFormat.choices, default=ReleaseFormat.DEMOTAPE)
    year = models.PositiveIntegerField()
    label = models.CharField(max_length=255, blank=True)
    catalog_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='releases_created')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-year', 'title']

    def __str__(self):
        return f'{self.band.name} — {self.title}'


class Track(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=255)
    track_number = models.PositiveIntegerField()
    duration = models.DurationField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True)
    lyrics = models.TextField(blank=True)
    lyrics_en = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='tracks_created')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['track_number']

    def __str__(self):
        return f'{self.track_number}. {self.title}'


class Image(models.Model):
    band = models.ForeignKey(Band, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    release = models.ForeignKey(Release, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    image_file = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=255, blank=True)
    image_type = models.CharField(max_length=20, choices=ImageType.choices, default=ImageType.OTHER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='images_created')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.caption or f'Image {self.pk}'


class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    tracks = models.ManyToManyField(Track, through='PlaylistTrack', related_name='playlists')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'slug']
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ['playlist', 'track']
        ordering = ['order']

    def __str__(self):
        return f'{self.playlist.title} — {self.track.title}'


class Flag(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    flagged_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='flags_created')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='flags_resolved')
    resolution_note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Flag on {self.content_type} #{self.object_id}'


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.FREE)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} profile'


class PlayLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='play_logs')
    session_key = models.CharField(max_length=40, blank=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='play_logs')
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-played_at']

    def __str__(self):
        return f'{self.track} played at {self.played_at}'


class Link(models.Model):
    """External links related to a band — videos, websites, purchase, social media."""
    LINK_TYPES = [
        ('video', 'Video (YouTube, Vimeo, etc.)'),
        ('website', 'Official Website'),
        ('social', 'Social Media'),
        ('purchase', 'Where to Buy'),
        ('streaming', 'Streaming'),
        ('archive', 'Archive / Reference'),
        # Extended types — added 2026-09-21 (PUR-1221): research scripts
        # introduced these values before the model was updated. Values match
        # the DB exactly; existing rows are NOT modified.
        ('article', 'Article / Press'),
        ('interview', 'Interview'),
        ('music', 'Music (Bandcamp, SoundCloud)'),
        ('review', 'Review'),
        ('news', 'News'),
        ('database', 'Database Entry'),
        ('official', 'Official Page'),
        ('festival', 'Festival / Event'),
        ('image', 'Image / Photo'),
        ('shop', 'Shop / Merch'),
        ('live', 'Live Recording'),
        ('radio', 'Radio / Podcast'),
        ('directory', 'Directory Listing'),
        ('fanzine', 'Fanzine'),
        ('profile', 'Profile Page'),
        ('other', 'Other'),
    ]
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='links')
    link_type = models.CharField(max_length=20, choices=LINK_TYPES)
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False, help_text='Main/official link')
    # Verification system — 4-level source verification (added 2026-09-21)
    verification_level = models.IntegerField(
        default=1,
        choices=[
            (1, 'Level 1 — Discovered'),
            (2, 'Level 2 — Cross-Referenced'),
            (3, 'Level 3 — Auto-Verified'),
            (4, 'Level 4 — Admin Confirmed'),
        ],
        help_text='Verification level: 1=discovered, 2=cross-ref, 3=auto-checked, 4=admin-confirmed'
    )
    discovery_source = models.URLField(
        blank=True,
        help_text='URL where this link was first found (Level 1 evidence)'
    )
    crossref_source = models.URLField(
        blank=True,
        help_text='Second independent source confirming this link (Level 2 evidence)'
    )
    verified_at = models.DateTimeField(
        null=True, blank=True,
        help_text='When this link was last verified'
    )
    verified_by = models.CharField(
        max_length=50, blank=True,
        help_text='Who verified: "auto-checker" or "admin"'
    )
    verification_notes = models.TextField(
        blank=True,
        help_text='Failure reasons, ambiguity notes, evidence summary'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-verification_level', 'link_type', '-is_primary', 'title']

    def __str__(self):
        return f'{self.link_type}: {self.title or self.url}'


class ContributorSubmission(models.Model):
    """External community submissions — link fixes, band updates."""

    class SubmissionType(models.TextChoices):
        LINK_FIX = 'link_fix', 'Link Fix / Report Issue'
        BAND_UPDATE = 'band_update', 'Band Update / Missing Links'

    class MetaStatus(models.TextChoices):
        PENDING = 'pending', 'Pending Review'
        REVIEWED = 'reviewed', 'Reviewed'
        APPLIED = 'applied', 'Applied'
        REJECTED = 'rejected', 'Rejected'

    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='contributor_submissions')
    link = models.ForeignKey(Link, on_delete=models.SET_NULL, null=True, blank=True, related_name='contributor_submissions')
    submission_type = models.CharField(max_length=20, choices=SubmissionType.choices)
    suggested_url = models.URLField(blank=True)
    comment = models.TextField(blank=True)
    submitter_name = models.CharField(max_length=100, blank=True)
    submitter_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=MetaStatus.choices, default=MetaStatus.PENDING)
    reviewed_by = models.CharField(max_length=50, blank=True)
    review_notes = models.TextField(blank=True)
    # Spam protection fields
    math_captcha_answer = models.CharField(max_length=10, blank=True)
    honeypot = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_submission_type_display()} for {self.band.name}'


class Label(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    city = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('defunct', 'Defunct'),
        ('unknown', 'Unknown'),
    ], default='unknown')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class BandConnection(models.Model):
    from_band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='connections_from')
    to_band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='connections_to')
    connection_type = models.CharField(max_length=50, choices=[
        ('shared_member', 'Shared Member'),
        ('scene_peer', 'Scene Peer'),
        ('influence', 'Influence'),
        ('label_mate', 'Label Mate'),
        ('venue_regular', 'Venue Regular'),
        ('successor', 'Successor Band'),
        ('collaboration', 'Collaboration'),
    ])
    source = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['from_band', 'to_band', 'connection_type']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.from_band.name} → {self.to_band.name} ({self.connection_type})'


class Fanzine(models.Model):
    """Italian underground fanzines — independent magazines that reviewed bands."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    city = models.CharField(max_length=255, blank=True)
    active_years = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to='fanzines/', blank=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('defunct', 'Defunct'),
        ('unknown', 'Unknown'),
    ], default='unknown')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class FanzineReview(models.Model):
    """Reviews of bands published in fanzines."""
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='fanzine_reviews')
    fanzine = models.ForeignKey(Fanzine, on_delete=models.CASCADE, related_name='reviews')
    issue_number = models.CharField(max_length=50, blank=True)
    review_text = models.TextField(blank=True)
    page_number = models.CharField(max_length=20, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    digitized_url = models.URLField(blank=True, help_text='Link to digitized version if available online')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', 'fanzine__name', 'issue_number']
        unique_together = ['band', 'fanzine', 'issue_number']

    def __str__(self):
        return f'{self.band.name} in {self.fanzine.name} #{self.issue_number}'
