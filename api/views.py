from django.shortcuts import get_object_or_404
import json
from .models import Event, Attendee
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            
            user = User.objects.create_user(username=username, email=email, password=password)
            
            return JsonResponse({
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def create_event(request, user_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        user = get_object_or_404(User, id=user_id)
        
        try:
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
                    'spotify_artist_id': event.spotify_artist_id,
                    'ticketmaster_event_id': event.ticketmaster_event_id,
                    'owner': user.username
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def join_event(request, user_id, event_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            event = get_object_or_404(Event, id=event_id)
            
            attendee, created = Attendee.objects.get_or_create(user=user, event=event)
            
            if created:
                return JsonResponse({
                    'data': {
                        'user_id': user.id,
                        'event_id': event.id,
                        'username': user.username,
                    }
                }, status=201)
            else:
                return JsonResponse({'error': 'User is already attending this event'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def leave_event(request, user_id, event_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            event = get_object_or_404(Event, id=event_id)
            
            try:
                attendee = Attendee.objects.get(user=user, event=event)
                attendee.delete()
                return JsonResponse({'message': 'User has left the event'}, status=200)
            except Attendee.DoesNotExist:
                return JsonResponse({'error': 'User is not attending this event'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def event_attendees(request, event_id):
    if request.method == 'GET':
        try:
            event = get_object_or_404(Event, id=event_id)
            attendees = Attendee.objects.filter(event=event)
            
            attendees_list = [{
                'user_id': attendee.user.id,
                'username': attendee.user.username
            } for attendee in attendees]
            
            return JsonResponse({'attendees': attendees_list}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def get_user_events(request, user_id):
    if request.method == 'GET':
        try:
            user = get_object_or_404(User, id=user_id)
            events = Event.objects.filter(owner=user)
            
            events_list = [{
                'event_id': event.id,
                'event_name': event.event_name,
                'venue_name': event.venue_name,
                'date_time': event.date_time,
                'artist': event.artist,
                'location': event.location,
                'spotify_artist_id': event.spotify_artist_id,
                'ticketmaster_event_id': event.ticketmaster_event_id,
                'owner': user.username
            } for event in events]
            
            return JsonResponse({'events': events_list}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_one_event(request, user_id, event_id):
    if request.method == 'GET':
        try:
            user = get_object_or_404(User, id=user_id)
            event = get_object_or_404(Event, id=event_id, owner=user)
            
            event_data = {
                'event_id': event.id,
                'event_name': event.event_name,
                'venue_name': event.venue_name,
                'date_time': event.date_time,
                'artist': event.artist,
                'location': event.location,
                'spotify_artist_id': event.spotify_artist_id,
                'ticketmaster_event_id': event.ticketmaster_event_id,
                'owner': user.username
            }
            
            return JsonResponse({'event': event_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@require_POST
def login_user(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return JsonResponse({'error': 'Missing username or password'}, status=400)
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return JsonResponse({
            'data': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'status': 'Logged in'
            }
        })
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
@require_POST
@login_required
def logout_user(request):
    user = request.user
    logout(request)
    return JsonResponse({
        'data': {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'status': 'Logged out'
        }
    })

@csrf_exempt
@require_GET
def current_session(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'No Users Logged in'
        }, status=401)

    user = request.user
    return JsonResponse({
        'data': {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'status': 'Logged in'
        }
    })
# might need add @login_required to event create so only logged in users can create events 
@csrf_exempt
def delete_event(request, user_id, event_id):
    if request.method == 'DELETE':
        try:
            user = get_object_or_404(User, id=user_id)
            event = get_object_or_404(Event, id=event_id, owner=user)
            event.delete()
            return JsonResponse({
                'message': 'Event deleted successfully',
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'deleted_event_id': event_id
                }
            }, status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found or user is not the owner'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)