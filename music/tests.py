import pytest
from .models import Band, Release, Track, Label, Genre


@pytest.mark.django_db
class TestGenreModel:
    def test_create_genre(self):
        genre = Genre.objects.create(name='Punk')
        assert genre.name == 'Punk'
        assert genre.slug == 'punk'

    def test_genre_str(self):
        genre = Genre.objects.create(name='Hardcore')
        assert str(genre) == 'Hardcore'


@pytest.mark.django_db
class TestLabelModel:
    def test_create_label(self):
        label = Label.objects.create(name='Self-Released', is_self_released=True)
        assert label.name == 'Self-Released'
        assert label.is_self_released is True
        assert label.slug == 'self-released'

    def test_label_str(self):
        label = Label.objects.create(name='Test Label')
        assert str(label) == 'Test Label'


@pytest.mark.django_db
class TestBandModel:
    def test_create_band(self):
        band = Band.objects.create(name='Test Band', city='Rome')
        assert band.name == 'Test Band'
        assert band.slug == 'test-band'
        assert band.city == 'Rome'

    def test_band_with_genres(self):
        genre = Genre.objects.create(name='Crust')
        band = Band.objects.create(name='Crust Band')
        band.genres.add(genre)
        assert band.genres.count() == 1

    def test_band_str(self):
        band = Band.objects.create(name='Noisy Band')
        assert str(band) == 'Noisy Band'

    def test_band_absolute_url(self):
        band = Band.objects.create(name='URL Band')
        assert band.get_absolute_url() == '/music/url-band/'


@pytest.mark.django_db
class TestReleaseModel:
    def test_create_release(self):
        band = Band.objects.create(name='Release Band')
        release = Release.objects.create(
            title='First Demo', band=band, format='demotape', year=1985
        )
        assert release.title == 'First Demo'
        assert release.slug == 'first-demo'
        assert release.format == 'demotape'

    def test_release_str(self):
        band = Band.objects.create(name='Band X')
        release = Release.objects.create(title='Demo 1', band=band)
        assert str(release) == 'Band X — Demo 1'

    def test_release_with_label(self):
        band = Band.objects.create(name='Label Band')
        label = Label.objects.create(name='Underground Records')
        release = Release.objects.create(title='EP', band=band, label=label)
        assert release.label.name == 'Underground Records'


@pytest.mark.django_db
class TestTrackModel:
    def test_create_track(self):
        band = Band.objects.create(name='Track Band')
        release = Release.objects.create(title='Album', band=band)
        track = Track.objects.create(
            title='First Song', release=release, track_number=1
        )
        assert track.title == 'First Song'
        assert str(track) == '1. First Song'

    def test_track_without_number(self):
        band = Band.objects.create(name='Track Band 2')
        release = Release.objects.create(title='Album 2', band=band)
        track = Track.objects.create(title='Mystery Track', release=release)
        assert str(track) == 'Mystery Track'
