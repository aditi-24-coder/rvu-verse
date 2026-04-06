import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_registration_with_rvu_email():
    # Valid email
    user = User.objects.create_user(username='rvu_user', email='student@rvu.edu.in', password='testpass123')
    assert user.email.endswith('@rvu.edu.in')

    # Invalid email
    user2 = User.objects.create_user(username='invalid_user', email='hacker@gmail.com', password='testpass123')
    assert not user2.email.endswith('@rvu.edu.in')
