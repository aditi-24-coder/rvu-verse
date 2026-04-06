import pytest
from django.contrib.auth.models import User
from core.models import Profile

@pytest.mark.django_db
def test_profile_created_with_user():
    user = User.objects.create_user(username='testuser', password='password123')
    assert hasattr(user, 'profile')
    assert isinstance(user.profile, Profile)
    assert user.profile.bio == ''  # default blank
