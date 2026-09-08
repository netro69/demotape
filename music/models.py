from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Label(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    is_self_released = models.BooleanField(
        default=True,
        help_text='Most underground bands self-release'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Label'
        verbose_name_plural = 'Labels'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Band(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(
        max_length=100, blank=True, help_text='Italian province'
    )
    active_years = models.CharField(
        max_length=50, blank=True, help_text='e.g., 1985-1992'
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name='bands')
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Band'
        verbose_name_plural = 'Bands'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:band_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Release(models.Model):
    FORMAT_CHOICES = [
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
        ('demotape', 'Demotape'),
        ('cassette', 'Cassette'),
        ('digital', 'Digital'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    band = models.ForeignKey(
        Band, on_delete=models.CASCADE, related_name='releases'
    )
    label = models.ForeignKey(
        Label, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='releases'
    )
    format = models.CharField(
        max_length=20, choices=FORMAT_CHOICES, default='demotape'
    )
    year = models.IntegerField(null=True, blank=True)
    tracklist = models.TextField(
        blank=True, help_text='Plain text tracklist'
    )
    cover_image = models.ImageField(
        upload_to='covers/', blank=True, null=True
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'title']
        verbose_name = 'Release'
        verbose_name_plural = 'Releases'

    def __str__(self):
        return f'{self.band.name} — {self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Track(models.Model):
    release = models.ForeignKey(
        Release, on_delete=models.CASCADE, related_name='tracks'
    )
    title = models.CharField(max_length=300)
    track_number = models.IntegerField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    audio_file = models.FileField(
        upload_to='audio/', blank=True, null=True,
        help_text='Digitized track audio'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['track_number', 'title']
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'

    def __str__(self):
        if self.track_number:
            return f'{self.track_number}. {self.title}'
        return self.title
