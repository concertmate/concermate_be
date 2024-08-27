from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    venue_name = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    artist = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    spotify_artist_id = models.CharField(max_length=100)
    ticketmaster_event_id = models.CharField(max_length=100)


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_digest = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
