# Created-by: forge | Date: 2026-09-21
from django.contrib import admin
from django.utils import timezone
from .models import (
    Band, GenreTag, Release, Track, Image,
    Playlist, PlaylistTrack, Flag, UserProfile, PlayLog,
    Link, Label, BandConnection, ContributorSubmission,
)


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1


class BandConnectionInline(admin.TabularInline):
    model = BandConnection
    extra = 1
    fk_name = 'from_band'


class TrackInline(admin.TabularInline):
    model = Track
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['band', 'link_type', 'title', 'url', 'is_primary', 'verification_level', 'verified_by', 'verified_at']
    list_filter = ['verification_level', 'link_type', 'verified_by']
    search_fields = ['band__name', 'title', 'url', 'verification_notes']
    readonly_fields = ['verified_at', 'verified_by', 'verification_level']
    actions = ['confirm_links', 'reject_links', 'flag_links']

    def confirm_links(self, request, queryset):
        """Bulk confirm selected links \u2192 Level 4."""
        count = queryset.update(
            verification_level=4,
            verified_by='admin',
            verified_at=timezone.now(),
            verification_notes='Bulk confirmed by admin',
        )
        self.message_user(request, f'{count} links confirmed at Level 4.')
    confirm_links.short_description = "Confirm selected links (Level 4)"

    def reject_links(self, request, queryset):
        """Bulk reject selected links \u2192 demote to Level 1."""
        count = queryset.update(
            verification_level=1,
            verified_by='',
            verified_at=None,
            verification_notes='Rejected by admin \u2014 demoted to Level 1',
        )
        self.message_user(request, f'{count} links rejected and demoted to Level 1.')
    reject_links.short_description = "Reject selected links (demote to Level 1)"

    def flag_links(self, request, queryset):
        """Flag selected links for manual review."""
        count = queryset.update(verification_notes='Flagged for manual review by admin')
        self.message_user(request, f'{count} links flagged for review.')
    flag_links.short_description = "Flag selected links for review"


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'status', 'founded_year']
    search_fields = ['name']


@admin.register(BandConnection)
class BandConnectionAdmin(admin.ModelAdmin):
    list_display = ['from_band', 'to_band', 'connection_type']


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'active_years', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'genre_tags']
    search_fields = ['name', 'city']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LinkInline, BandConnectionInline, ImageInline]


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


@admin.register(ContributorSubmission)
class ContributorSubmissionAdmin(admin.ModelAdmin):
    list_display = ['band', 'submission_type', 'suggested_url', 'status', 'created_at', 'reviewed_by']
    list_filter = ['status', 'submission_type']
    search_fields = ['band__name', 'suggested_url', 'comment', 'submitter_name']
    readonly_fields = ['created_at', 'math_captcha_answer', 'honeypot']
    actions = ['approve_submissions', 'reject_submissions']

    def approve_submissions(self, request, queryset):
        """Mark selected submissions as approved (applied)."""
        count = queryset.update(status='applied', reviewed_by='admin')
        self.message_user(request, f'{count} submissions approved and marked as applied.')
    approve_submissions.short_description = 'Approve selected (mark as applied)'

    def reject_submissions(self, request, queryset):
        """Reject selected submissions."""
        count = queryset.update(status='rejected', reviewed_by='admin')
        self.message_user(request, f'{count} submissions rejected.')
    reject_submissions.short_description = 'Reject selected'
