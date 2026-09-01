from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Band, Release, Track, GenreTag


def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')


def band_list(request):
    bands = Band.objects.filter(status='published').prefetch_related('genre_tags')

    # Filter by genre
    genre = request.GET.get('genre')
    if genre:
        bands = bands.filter(genre_tags__slug=genre)

    # Filter by city
    city = request.GET.get('city')
    if city:
        bands = bands.filter(city__iexact=city)

    # Filter by format (through releases)
    fmt = request.GET.get('format')
    if fmt:
        bands = bands.filter(releases__format=fmt).distinct()

    # Filter by decade
    decade = request.GET.get('decade')
    if decade:
        try:
            decade_int = int(decade)
            bands = bands.filter(
                releases__year__gte=decade_int,
                releases__year__lt=decade_int + 10
            ).distinct()
        except ValueError:
            pass

    # Pagination
    paginator = Paginator(bands, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options
    genres = GenreTag.objects.all().order_by('name')
    cities = Band.objects.filter(status='published').exclude(city='').values_list('city', flat=True).distinct().order_by('city')
    decades = [1970, 1980, 1990, 2000, 2010, 2020]

    context = {
        'page_obj': page_obj,
        'genres': genres,
        'cities': cities,
        'decades': decades,
        'selected_genre': genre,
        'selected_city': city,
        'selected_format': fmt,
        'selected_decade': decade,
    }
    return render(request, 'core/band_list.html', context)


def band_detail(request, slug):
    band = get_object_or_404(Band, slug=slug, status='published')
    releases = band.releases.filter(status='published').prefetch_related('tracks')
    images = band.images.filter(status='published')

    context = {
        'band': band,
        'releases': releases,
        'images': images,
    }
    return render(request, 'core/band_detail.html', context)


def release_detail(request, slug):
    release = get_object_or_404(Release, slug=slug, status='published')
    tracks = release.tracks.filter(status='published')
    images = release.images.filter(status='published')

    context = {
        'release': release,
        'tracks': tracks,
        'images': images,
    }
    return render(request, 'core/release_detail.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        search_vector = (
            SearchVector('name', weight='A') +
            SearchVector('bio', weight='B') +
            SearchVector('city', weight='C')
        )
        search_query = SearchQuery(query)

        band_results = Band.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query, status='published').order_by('-rank')

        release_vector = (
            SearchVector('title', weight='A') +
            SearchVector('description', weight='B') +
            SearchVector('label', weight='C')
        )
        release_results = Release.objects.annotate(
            search=release_vector,
            rank=SearchRank(release_vector, search_query)
        ).filter(search=search_query, status='published').order_by('-rank')

        track_vector = (
            SearchVector('title', weight='A') +
            SearchVector('lyrics', weight='B')
        )
        track_results = Track.objects.annotate(
            search=track_vector,
            rank=SearchRank(track_vector, search_query)
        ).filter(search=search_query, status='published').order_by('-rank')

        results = {
            'bands': band_results[:10],
            'releases': release_results[:10],
            'tracks': track_results[:10],
        }

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'core/search.html', context)