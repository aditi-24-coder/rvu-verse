import pytest
from django.contrib.auth.models import User
from core.models import Follow

@pytest.mark.django_db
def test_follow_unfollow_functionality():
    user1 = User.objects.create_user(username='alice', password='pass')
    user2 = User.objects.create_user(username='bob', password='pass')

    # Follow
    follow = Follow.objects.create(follower=user1, following=user2)
    assert Follow.objects.filter(follower=user1, following=user2).exists()

    # Unfollow
    follow.delete()
    assert not Follow.objects.filter(follower=user1, following=user2).exists()
