import pytest
from django.contrib.auth.models import User
from core.models import Notification, Post

@pytest.mark.django_db
def test_notification_creation():
    user1 = User.objects.create_user(username='u1', password='pass')
    user2 = User.objects.create_user(username='u2', password='pass')
    post = Post.objects.create(user=user1, content="Post content")

    notif = Notification.objects.create(
        user=user1,
        from_user=user2,
        notification_type='like',
        post=post,
        text='u2 liked your post'
    )

    assert notif.notification_type == 'like'
    assert notif.user == user1
    assert notif.post == post
