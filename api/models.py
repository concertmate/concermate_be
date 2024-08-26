from django.db import models

# Create your models here.
class Event(models.Model):
    venue_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    artist = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    spotify_artist_id = models.CharField(max_length=100)
    ticketmaster_event_id = models.CharField(max_length=100)

