from django.contrib import admin
from .models import (
    Band, GenreTag, Release, Track, Image,
    Playlist, PlaylistTrack, Flag, UserProfile, PlayLog,
)


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'active_years', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'genre_tags']
    search_fields = ['name', 'city']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GenreTag)
class GenreTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'band', 'format', 'year', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'format', 'year']
    search_fields = ['title', 'band__name']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'release', 'track_number', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'release__title']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image_type', 'band', 'release', 'status', 'created_at']
    list_filter = ['status', 'image_type']
    search_fields = ['caption']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_public', 'created_at']
    list_filter = ['is_public']
    search_fields = ['title', 'user__username']


@admin.register(PlaylistTrack)
class PlaylistTrackAdmin(admin.ModelAdmin):
    list_display = ['playlist', 'track', 'order']


@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'flagged_by', 'resolved', 'created_at']
    list_filter = ['resolved', 'content_type']
    search_fields = ['reason']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']


@admin.register(PlayLog)
class PlayLogAdmin(admin.ModelAdmin):
    list_display = ['track', 'user', 'session_key', 'played_at']
    search_fields = ['track__title', 'user__username']
