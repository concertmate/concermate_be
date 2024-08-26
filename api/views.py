from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from .models import Event

class EventView(View):

    def create(self, request):
        try:
            data = json.loads(request.body)
            event = Event.objects.create(
                venue_name=data['venue_name'],
                event_name=data['event_name'],
                date_time=data['date_time'],
                artist=data['artist'],
                location=data['location'],
                spotify_artist_id=data['spotify_artist_id'],
                ticketmaster_event_id=data['ticketmaster_event_id']
            )
            return JsonResponse({
                data: {
                    'venue_name': event.venue_name,
                    'event_name': event.event_name,
                    'date_time': event.date_time,
                    'artist': event.artist,
                    'location': event.location,
                    'spotify_artist_id': event.spotify_artist_id,
                    'ticketmaster_event_id': event.ticketmaster_event_id
                }
            }, status=201)
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("invalid json")
        



# def get_events(request):
#     return render(request, 'api/events.json') # This is a placeholder for now want to return json

