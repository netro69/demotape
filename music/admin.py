from django.contrib import admin
from .models import Band, Release, Track, Label, Genre


class TrackInline(admin.TabularInline):
    model = Track
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'is_self_released', 'created_at')
    list_filter = ('is_self_released', 'city')
    search_fields = ('name', 'city')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'province', 'active_years', 'created_at')
    list_filter = ('genres', 'city', 'province')
    search_fields = ('name', 'city', 'bio')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('genres',)


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'band', 'label', 'format', 'year', 'created_at')
    list_filter = ('format', 'year', 'label')
    search_fields = ('title', 'band__name', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TrackInline]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'release', 'track_number', 'duration')
    list_filter = ('release__format',)
    search_fields = ('title', 'release__title')
