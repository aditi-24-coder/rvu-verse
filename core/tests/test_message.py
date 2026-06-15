import pytest
from django.contrib.auth.models import User
from core.models import Message

@pytest.mark.django_db
def test_message_creation_default_unread():
    sender = User.objects.create_user(username='sender', password='password')
    receiver = User.objects.create_user(username='receiver', password='password')
    
    message = Message.objects.create(
        sender=sender,
        receiver=receiver,
        content="Hello there!"
    )
    
    assert message.content == "Hello there!"
    assert message.is_read is False
