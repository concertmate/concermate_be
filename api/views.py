from django.shortcuts import render
import json
from .models import Event, Attendee
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({
            'data': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })
    
@csrf_exempt
def create_event(request, user_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = get_object_or_404(User, id=user_id)
        
        event = Event.objects.create(
            venue_name=data.get('venue_name'),
            event_name=data.get('event_name'),
            date_time=data.get('date_time'),
            artist=data.get('artist'),
            location=data.get('location'),
            spotify_artist_id=data.get('spotify_artist_id'),
            ticketmaster_event_id=data.get('ticketmaster_event_id'),
            owner=user
        )
        
        return JsonResponse({
            'data': {
                'event_id': event.id,
                'event_name': event.event_name,
                'venue_name': event.venue_name,
                'date_time': event.date_time,
                'artist': event.artist,
                'location': event.location,
            }
        })

@csrf_exempt
def join_event(request, user_id, event_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        event = get_object_or_404(Event, id=event_id)
        
        attendee, created = Attendee.objects.get_or_create(user=user, event=event)
        
        if created:
            return JsonResponse({
                'data:': {
                    'user_id': user.id,
                    'event_id': event.id,
                    'username': user.username,
            }
            })
        else:
            return JsonResponse({
                'error': 'User is already attending this event'
            })

@csrf_exempt
def leave_event(request, user_id, event_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        event = get_object_or_404(Event, id=event_id)
        
        attendee = get_object_or_404(Attendee, user=user, event=event)
        attendee.delete()
        
        return JsonResponse({
            'data': {
                'user_id': user.id,
                'event_id': event.id,
                'username': user.username,
            }
        })

@csrf_exempt
def users_attending_event(request, event_id):
    if request.method == 'GET':
        event = get_object_or_404(Event, id=event_id)
        
        attendees = event.attendees.select_related('user').all()
        
        return JsonResponse({
            'data': {
                'event_id': event.id,
                'event_name': event.event_name,
                'attendees': [
                    {
                        'user_id': attendee.user.id,
                        'username': attendee.user.username,
                    }
                    for attendee in attendees
                ]
            }
        })