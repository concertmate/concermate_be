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

    def test_create_user_success(self):
        url = reverse('create_user')

        data = {
            'username': 'newuser',
            'email': 'test@email.com',
            'password': 'newpass'
        }

        response = self.client.post(url, data, content_type='application/json')

        # Check that the response is 201 Created
        self.assertEqual(response.status_code, 201)

        # Check that the user was created
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'test@email.com')
        self.assertEqual(user.check_password('newpass'), True)

        # Check that the response contains the user data
        self.assertEqual(response.json()['data']['user_id'], user.id)
        self.assertEqual(response.json()['data']['username'], user.username)
        self.assertEqual(response.json()['data']['email'], user.email)

    def test_create_event_success(self):
        url = reverse('create_event', kwargs={'user_id': self.user.id})

        data = {
            'venue_name': 'venue3',
            'event_name': 'event3',
            'date_time': '2021-10-12T10:00:00Z',
            'artist': 'artist3',
            'location': 'location3',
            'spotify_artist_id': 'spotify_artist_id3',
            'ticketmaster_event_id': 'ticketmaster_event_id3',
            'owner': self.user.username
        }

        response = self.client.post(url, data, content_type='application/json')

        # Check that the response is 201 Created
        self.assertEqual(response.status_code, 201)

        # Check that the event was created
        event = Event.objects.get(venue_name='venue3')
        self.assertEqual(event.event_name, 'event3')
        self.assertEqual(event.artist, 'artist3')
        self.assertEqual(event.location, 'location3')
        self.assertEqual(event.spotify_artist_id, 'spotify_artist_id3')
        self.assertEqual(event.ticketmaster_event_id, 'ticketmaster_event_id3')
        self.assertEqual(event.owner, self.user)

        # Check that the response contains the event data
        self.assertEqual(response.json()['data']['event_id'], event.id)
        self.assertEqual(response.json()['data']['event_name'], event.event_name)
        self.assertEqual(response.json()['data']['venue_name'], event.venue_name)
        self.assertEqual(response.json()['data']['artist'], event.artist)
        self.assertEqual(response.json()['data']['location'], event.location)
        self.assertEqual(response.json()['data']['spotify_artist_id'], event.spotify_artist_id)
        self.assertEqual(response.json()['data']['ticketmaster_event_id'], event.ticketmaster_event_id)
        self.assertEqual(response.json()['data']['owner'], self.user.username)

    def test_join_event_success(self):
        url = reverse('join_event', kwargs={'user_id': self.user.id, 'event_id': self.event1.id})

        response = self.client.post(url)

        # Check that the response is 201 Created
        self.assertEqual(response.status_code, 201)

        # Check that the user is now an attendee of the event
        self.assertEqual(self.event1.attendees.filter(id=self.user.id).exists(), True)

        # Check that the response contains the correct data
        self.assertEqual(response.json()['data']['user_id'], self.user.id)
        self.assertEqual(response.json()['data']['event_id'], self.event1.id)
        self.assertEqual(response.json()['data']['username'], self.user.username)

    def test_leave_event_success(self):
        # Join the event first
        join_url = reverse('join_event', kwargs={'user_id': self.user.id, 'event_id': self.event1.id})
        self.client.post(join_url)

        # Leave event
        url = reverse('leave_event', kwargs={'user_id': self.user.id, 'event_id': self.event1.id})

        response = self.client.post(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the user is no longer an attendee of the event
        self.assertEqual(self.event1.attendees.filter(id=self.user.id).exists(), False)

        # Check that the response contains the correct data
        self.assertEqual(response.json()['message'], 'User has left the event')

    def test_get_event_attendees_success(self):
        # Join the event first
        join_url = reverse('join_event', kwargs={'user_id': self.user.id, 'event_id': self.event1.id})
        self.client.post(join_url)

        url = reverse('users_attending_event', kwargs={'event_id': self.event1.id})

        response = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Get the attendees from the response
        attendees = response.json()['attendees']

        # Assert that there is one attendee for the event
        self.assertEqual(len(attendees), 1)
        self.assertEqual(attendees[0]['user_id'], self.user.id)
        self.assertEqual(attendees[0]['username'], self.user.username)

    def test_get_all_events_for_user_success(self):
        url = reverse('user_events', kwargs={'user_id': self.user.id})

        response = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Get the events from the response
        events = response.json()['events']

        # Assert that there are two events associated with user
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]['owner'], self.user.username)
        self.assertEqual(events[1]['owner'], self.user.username)

    def test_get_one_event_success(self):
        url = reverse('one_event', kwargs={'user_id': self.user.id, 'event_id': self.event1.id})

        response = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the correct data
        self.assertEqual(response.json()['event']['event_id'], self.event1.id)
        self.assertEqual(response.json()['event']['owner'], self.user.username)
        self.assertEqual(response.json()['event']['venue_name'], self.event1.venue_name)
        self.assertEqual(response.json()['event']['event_name'], self.event1.event_name)
        self.assertEqual(response.json()['event']['artist'], self.event1.artist)
        self.assertEqual(response.json()['event']['location'], self.event1.location)
        self.assertEqual(response.json()['event']['spotify_artist_id'], self.event1.spotify_artist_id)
        self.assertEqual(response.json()['event']['ticketmaster_event_id'], self.event1.ticketmaster_event_id)

    def test_login_user_success(self):
        url = reverse('login_user')

        data = {
            'username': 'testuser',
            'password': 'testpass'
        }

        response = self.client.post(url, data, content_type='application/json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the correct data
        self.assertEqual(response.json()['data']['user_id'], self.user.id)
        self.assertEqual(response.json()['data']['username'], self.user.username)
        self.assertEqual(response.json()['data']['email'], self.user.email)
        self.assertEqual(response.json()['data']['status'], 'Logged in')

    def test_logout_user_success(self):
        # Log in User
        login_url = reverse('login_user')

        data = {
            'username': 'testuser',
            'password': 'testpass'
        }

        response = self.client.post(login_url, data, content_type='application/json')

        url = reverse('logout_user')

        response = self.client.post(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the correct data
        self.assertEqual(response.json()['data']['user_id'], self.user.id)
        self.assertEqual(response.json()['data']['username'], self.user.username)
        self.assertEqual(response.json()['data']['email'], self.user.email)
        self.assertEqual(response.json()['data']['status'], 'Logged out')

    def test_current_session_success(self):
        # Log in User
        login_url = reverse('login_user')

        data = {
            'username': 'testuser',
            'password': 'testpass'
        }

        response = self.client.post(login_url, data, content_type='application/json')

        url = reverse('current_session')

        response = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the correct data
        self.assertEqual(response.json()['data']['user_id'], self.user.id)
        self.assertEqual(response.json()['data']['username'], self.user.username)
        self.assertEqual(response.json()['data']['email'], self.user.email)
        self.assertEqual(response.json()['data']['status'], 'Logged in')

    def test_delete_event_success(self):
        url = reverse('delete_event', kwargs={'user_id': self.user.id, 'event_id': self.event1.id})

        response = self.client.delete(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the event was deleted
        self.assertEqual(Event.objects.filter(id=self.event1.id).exists(), False)

        # Check that the response contains the correct data
        self.assertEqual(response.json()['message'], 'Event deleted successfully')
        self.assertEqual(response.json()['data']['user_id'], self.user.id)
        self.assertEqual(response.json()['data']['username'], self.user.username)
        self.assertEqual(response.json()['data']['deleted_event_id'], self.event1.id)