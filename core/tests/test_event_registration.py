import pytest
from django.contrib.auth.models import User
from core.models import Event, EventRegistration
from django.utils import timezone

@pytest.mark.django_db
def test_event_registration_status():
    user = User.objects.create_user(username='u1', password='pass')
    event = Event.objects.create(
        title="Test Event",
        description="Event Description",
        organizer=user,
        location="Somewhere",
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(hours=2)
    )

    registration = EventRegistration.objects.create(user=user, event=event)
    assert registration.status == 'registered'
