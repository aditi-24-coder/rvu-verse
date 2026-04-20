import pytest
from django.contrib.auth.models import User
from core.models import Post, Like

@pytest.mark.django_db
def test_post_like_count():
    user1 = User.objects.create_user(username='u1', password='pass')
    user2 = User.objects.create_user(username='u2', password='pass')
    post = Post.objects.create(user=user1, content="A new post")

    Like.objects.create(user=user2, post=post)

    assert post.get_likes_count() == 1
