import pytest
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@pytest.mark.django_db
class TestProfileModel:
    def test_profile_created_with_user(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        assert hasattr(user, 'profile')
        assert user.profile.bio == ''

    def test_profile_str(self):
        user = User.objects.create_user(username='testuser2', password='testpass123')
        assert str(user.profile) == 'testuser2 profile'

    def test_profile_update(self):
        user = User.objects.create_user(username='testuser3', password='testpass123')
        user.profile.bio = 'Music enthusiast'
        user.profile.location = 'Milan'
        user.profile.save()
        assert user.profile.bio == 'Music enthusiast'
        assert user.profile.location == 'Milan'
