from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    venue_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    artist = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    spotify_artist_id = models.CharField(max_length=100)
    ticketmaster_event_id = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_owner')

    def __str__(self):
        return f"{self.owner} created event for {self.artist} at {self.venue_name} on {self.date_time}"

class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_attending')

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} attending {self.event.concert.title}"
    
class Token(models.Model):
    user = models.CharField(unique = True, max_length=50)
    createed_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} token is {self.token}"