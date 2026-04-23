import pytest
from django.contrib.auth.models import User
from core.models import Post

@pytest.mark.django_db
def test_post_hashtag_extraction():
    user = User.objects.create_user(username='u1', password='pass')
    post = Post.objects.create(user=user, content="Test", hashtags="tag1, tag2, tag3")

    hashtags = post.extract_hashtags()
    assert hashtags == ['tag1', 'tag2', 'tag3']
