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
        ('other', 'Other'),
    ]
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='links')
    link_type = models.CharField(max_length=20, choices=LINK_TYPES)
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False, help_text='Main/official link')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['link_type', '-is_primary', 'title']

    def __str__(self):
        return f'{self.get_link_type_display()}: {self.title or self.url}'


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
