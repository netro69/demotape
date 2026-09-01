from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Band, GenreTag, Release, Track


def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')


def band_list(request):
    bands = Band.objects.filter(status='published').distinct()
    genre_list = GenreTag.objects.all().order_by('name')
    city_list = Band.objects.filter(status='published').exclude(city='').values_list('city', flat=True).distinct().order_by('city')

    genre = request.GET.get('genre')
    city = request.GET.get('city')
    format_ = request.GET.get('format')
    decade = request.GET.get('decade')

    if genre:
        bands = bands.filter(genre_tags__slug=genre)
    if city:
        bands = bands.filter(city__iexact=city)
    if format_:
        bands = bands.filter(releases__format=format_)
    if decade:
        start = int(decade)
        bands = bands.filter(releases__year__gte=start, releases__year__lt=start + 10)

    paginator = Paginator(bands, 24)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'genre_list': genre_list,
        'city_list': city_list,
        'selected_genre': genre,
        'selected_city': city,
        'selected_format': format_,
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
    tracks = release.tracks.all()
    images = release.images.filter(status='published')
    context = {
        'release': release,
        'tracks': tracks,
        'band': release.band,
        'images': images,
    }
    return render(request, 'core/release_detail.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        search_query = SearchQuery(query)

        band_vector = SearchVector('name', weight='A') + SearchVector('city', weight='B')
        band_qs = Band.objects.filter(status='published').annotate(
            search=band_vector,
            rank=SearchRank(band_vector, search_query)
        ).filter(search=search_query).order_by('-rank')[:50]

        release_vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
        release_qs = Release.objects.filter(status='published').annotate(
            search=release_vector,
            rank=SearchRank(release_vector, search_query)
        ).filter(search=search_query).order_by('-rank')[:50]

        track_vector = SearchVector('title', weight='A')
        track_qs = Track.objects.filter(status='published').annotate(
            search=track_vector,
            rank=SearchRank(track_vector, search_query)
        ).filter(search=search_query).order_by('-rank')[:50]

        for band in band_qs:
            results.append({'type': 'Band', 'object': band, 'rank': band.rank})
        for release in release_qs:
            results.append({'type': 'Release', 'object': release, 'rank': release.rank})
        for track in track_qs:
            results.append({'type': 'Track', 'object': track, 'rank': track.rank})

        results.sort(key=lambda x: x['rank'], reverse=True)
        results = results[:50]

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'core/search.html', context)
