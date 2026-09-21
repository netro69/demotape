import hashlib
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from .models import Band, GenreTag, Release, Track, Label, BandConnection, Link, Fanzine, ContributorSubmission
from .forms import ContributorSubmissionForm


def home(request):
    latest_bands = Band.objects.filter(status='published').order_by('-created_at')[:6]
    recent_releases = Release.objects.filter(status='published').order_by('-created_at')[:10]
    total_bands = Band.objects.filter(status='published').count()
    total_releases = Release.objects.filter(status='published').count()
    total_labels = Label.objects.count()
    # Count releases that are likely lost (cassette format, pre-2000)
    lost_count = Release.objects.filter(status='published', format='cassette').count()
    
    context = {
        'latest_bands': latest_bands,
        'recent_releases': recent_releases,
        'total_bands': total_bands,
        'total_releases': total_releases,
        'total_labels': total_labels,
        'lost_count': lost_count,
    }
    return render(request, 'core/home.html', context)


def about(request):
    from .models import Link, ContributorSubmission
    verified_count = Link.objects.filter(verification_level=4).count()
    pending_count = Link.objects.filter(verification_level__lt=4).count()
    community_count = ContributorSubmission.objects.filter(status='applied').count()
    context = {
        'verified_count': verified_count,
        'pending_count': pending_count,
        'community_count': community_count,
    }
    return render(request, 'core/about.html', context)


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
    links = band.links.all()
    # Get tracks that have audio files
    from .models import Track
    audio_tracks = Track.objects.filter(release__band=band, status='published', audio_file__isnull=False).exclude(audio_file='')
    
    # Build list of (type_display, links_list) for the template
    from collections import OrderedDict
    link_groups = OrderedDict()
    for link in links:
        link_groups.setdefault(link.link_type, []).append(link)
    
    link_sections = []
    for link_type, type_links in link_groups.items():
        display = dict(Link.LINK_TYPES).get(link_type, link_type)
        # Extract YouTube video IDs for embedding
        for link in type_links:
            link.youtube_id = _extract_youtube_id(link.url)
        link_sections.append((display, type_links))
    
    # Annotate links with matching audio tracks (by title similarity)
    for display, type_links in link_sections:
        for link in type_links:
            link.local_audio = None
            if link.title:
                for track in audio_tracks:
                    if track.title and (
                        track.title.lower() in link.title.lower()
                        or link.title.lower() in track.title.lower()
                    ):
                        link.local_audio = track
                        break
    
    # Prefetch fanzine reviews with fanzine data
    fanzine_reviews = band.fanzine_reviews.select_related('fanzine')
    
    # Prefetch connections (both directions)
    connections_from = band.connections_from.select_related('to_band')
    connections_to = band.connections_to.select_related('from_band')
    
    # Get labels from releases (matching Label objects by name)
    label_names = band.releases.filter(status='published').exclude(label='').values_list('label', flat=True).distinct()
    labels = Label.objects.filter(name__in=label_names)
    
    context = {
        'band': band,
        'releases': releases,
        'images': images,
        'link_sections': link_sections,
        'audio_tracks': audio_tracks,
        'fanzine_reviews': fanzine_reviews,
        'connections_from': connections_from,
        'connections_to': connections_to,
        'labels': labels,
    }
    return render(request, 'core/band_detail.html', context)


def fanzine_detail(request, slug):
    fanzine = get_object_or_404(Fanzine, slug=slug)
    reviews = fanzine.reviews.select_related('band')
    context = {'fanzine': fanzine, 'reviews': reviews}
    return render(request, 'core/fanzine_detail.html', context)


def label_detail(request, slug):
    label = get_object_or_404(Label, slug=slug)
    # Get bands whose releases mention this label name
    release_ids = Release.objects.filter(label=label.name, status='published').select_related('band').values_list('band', flat=True).distinct()
    bands = Band.objects.filter(pk__in=release_ids, status='published')
    releases = Release.objects.filter(label=label.name, status='published').select_related('band')
    context = {'label': label, 'releases': releases, 'bands': bands}
    return render(request, 'core/label_detail.html', context)


def _extract_youtube_id(url):
    """Extract YouTube video ID from various URL formats."""
    import re
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


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


@staff_member_required
def review_queue(request):
    """Admin review queue for Level-3 links pending confirmation."""
    from .models import Link
    from django.utils import timezone

    if request.method == 'POST':
        sub_id = request.POST.get('sub_id')
        sub_action = request.POST.get('sub_action')
        if sub_id and sub_action:
            submission = get_object_or_404(ContributorSubmission, id=sub_id)
            if sub_action == 'approve':
                submission.status = 'applied'
                submission.reviewed_by = 'admin'
                submission.review_notes = 'Approved by admin — applied to link'
                submission.save()
                # Apply the submission: update link or create new one at L1 with crossref
                if submission.link and submission.suggested_url:
                    submission.link.url = submission.suggested_url
                    submission.link.crossref_source = submission.suggested_url
                    if submission.link.verification_level < 2:
                        submission.link.verification_level = 2
                    submission.link.verification_notes = f'Updated via community submission #{submission.id}'
                    submission.link.save()
                elif submission.suggested_url:
                    # Create new link at L1 with community as crossref evidence
                    Link.objects.create(
                        band=submission.band,
                        link_type='other',
                        url=submission.suggested_url,
                        verification_level=1,
                        discovery_source=submission.suggested_url,
                        crossref_source=f'community-submission-{submission.id}',
                        verification_notes=f'Created from community submission #{submission.id}',
                    )
                return HttpResponse(f'<tr class="text-success"><td colspan="8">✓ Applied — {submission.band.name}</td></tr>')
            elif sub_action == 'reject':
                submission.status = 'rejected'
                submission.reviewed_by = 'admin'
                submission.save()
                return HttpResponse(f'<tr class="text-danger"><td colspan="8">✗ Rejected — {submission.band.name}</td></tr>')
        link_id = request.POST.get('link_id')
        action = request.POST.get('action')
        link = get_object_or_404(Link, id=link_id)

        if action == 'confirm':
            link.verification_level = 4
            link.verified_by = 'admin'
            link.verified_at = timezone.now()
            link.verification_notes = 'Confirmed by admin'
            link.save()
            return JsonResponse({'status': 'ok', 'level': 4})
        elif action == 'reject':
            link.verification_level = 1
            link.verified_by = ''
            link.verified_at = None
            link.verification_notes = 'Rejected by admin'
            link.save()
            return JsonResponse({'status': 'ok', 'level': 1})
        elif action == 'flag':
            link.verification_notes = 'Flagged for manual review'
            link.save()
            return JsonResponse({'status': 'ok', 'flagged': True})

    links = Link.objects.filter(verification_level=3).select_related('band').order_by('band__name', 'title')
    submissions = ContributorSubmission.objects.filter(
        status='pending'
    ).select_related('band', 'link').order_by('-created_at')[:50]
    return render(request, 'admin/review.html', {
        'links': links,
        'submissions': submissions,
    })


def _check_rate_limit(ip_address, limit=5, period=3600):
    """Check if IP has exceeded submission rate limit."""
    key = f"contrib_ratelimit:{ip_address}"
    count = cache.get(key, 0)
    if count >= limit:
        return False
    return True


def _increment_rate_limit(ip_address, period=3600):
    """Increment submission count for IP."""
    key = f"contrib_ratelimit:{ip_address}"
    count = cache.get(key, 0)
    cache.set(key, count + 1, period)


def _get_client_ip(request):
    """Extract client IP from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def contributor_submit(request, slug):
    """Handle contributor submission form (GET for form, POST for submission)."""
    band = get_object_or_404(Band, slug=slug, status='published')
    link_id = request.GET.get('link_id') or request.POST.get('link_id')
    link = None
    if link_id:
        try:
            link = Link.objects.get(id=int(link_id), band=band)
        except (Link.DoesNotExist, ValueError):
            link = None

    if request.method == 'POST':
        return _handle_contributor_post(request, band, link)
    return _render_contributor_form(request, band, link)


def _render_contributor_form(request, band, link):
    """Render the contributor submission form."""
    import random
    captcha_a = random.randint(1, 10)
    captcha_b = random.randint(1, 10)
    submission_type = 'link_fix' if link else 'band_update'
    context = {
        'band': band,
        'link': link,
        'link_id': link.id if link else None,
        'submission_type': submission_type,
        'captcha_a': captcha_a,
        'captcha_b': captcha_b,
        'captcha_answer': captcha_a + captcha_b,
    }
    return render(request, 'core/contributor_form.html', context)


def _handle_contributor_post(request, band, link):
    """Process contributor submission POST."""
    ip = _get_client_ip(request)

    # Rate limit check
    if not _check_rate_limit(ip):
        return HttpResponseBadRequest(
            b'Too many submissions from this IP. Please try again later.',
            content_type='text/plain'
        )

    # Honeypot check
    if request.POST.get('company'):
        # Bot detected — silently accept but don't save
        return render(request, 'core/contributor_success.html', {'band': band})

    # Captcha check
    try:
        user_answer = int(request.POST.get('captcha_answer', 0))
        expected = int(request.POST.get('captcha_expected', 0))
    except (ValueError, TypeError):
        user_answer = -1
        expected = 0

    if user_answer != expected:
        return HttpResponseBadRequest(
            b'Incorrect captcha answer. Please go back and try again.',
            content_type='text/plain'
        )

    # Validate required fields
    comment = request.POST.get('comment', '').strip()
    if not comment:
        return HttpResponseBadRequest(
            b'Please provide a description.',
            content_type='text/plain'
        )

    # Create submission
    submission = ContributorSubmission.objects.create(
        band=band,
        link=link,
        submission_type='link_fix' if link else 'band_update',
        suggested_url=request.POST.get('suggested_url', ''),
        comment=comment,
        submitter_name=request.POST.get('submitter_name', ''),
        submitter_email=request.POST.get('submitter_email', ''),
        math_captcha_answer=str(user_answer),
        honeypot=request.POST.get('company', ''),
        status='pending',
    )

    _increment_rate_limit(ip)
    return render(request, 'core/contributor_success.html', {'band': band})