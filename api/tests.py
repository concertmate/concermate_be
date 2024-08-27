from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Event

# Create your tests here.

class EventViewTest(TestCase):
    def setUp(self):
        # Set up test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.event1 = Event.objects.create(
            venue_name='venue1',
            event_name='event1',
            date_time='2021-10-10T10:00:00Z',
            artist='artist1',
            location='location1',
            spotify_artist_id='spotify_artist_id1',
            ticketmaster_event_id='ticketmaster_event_id1',
            owner=self.user
        )

        self.event2 = Event.objects.create(
            venue_name='venue2',
            event_name='event2',
            date_time='2021-10-11T10:00:00Z',
            artist='artist2',
            location='location2',
            spotify_artist_id='spotify_artist_id2',
            ticketmaster_event_id='ticketmaster_event_id2',
            owner=self.user
        )

    def test_get_all_events_for_user(self):
        url = reverse('user_events', kwargs={'user_id': self.user.id})

        response = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Get the events from the response
        events = response.json()['data']['events']

        # Assert that there are two events associated with user
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]['owner'], self.user.id)
        self.assertEqual(events[1]['owner'], self.user.id)