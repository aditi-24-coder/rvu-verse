import pytest
from django.contrib.auth.models import User
from core.models import Post, Comment

@pytest.mark.django_db
def test_create_comment_on_post():
    user = User.objects.create_user(username='commentuser', password='password')
    post = Post.objects.create(user=user, content='Test post')
    comment = Comment.objects.create(post=post, user=user, content='Nice post!')

    assert comment.content == 'Nice post!'
    assert comment.post == post
    assert comment.user == user
