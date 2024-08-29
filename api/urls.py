from django.urls import path
from . import views

urlpatterns = [
    path('api/users/create', views.create_user, name='create_user'),
    path('api/users/<int:user_id>/events/create', views.create_event, name='create_event'),
    path('api/users/<int:user_id>/events/<int:event_id>/join', views.join_event, name='join_event'),
    path('api/users/<int:user_id>/events/<int:event_id>/leave', views.leave_event, name='leave_event'),
    path('api/users/<int:user_id>/events', views.get_user_events, name='user_events'),
    path('api/users/<int:user_id>/events/<int:event_id>', views.get_one_event, name='one_event'),
    path('api/users/<int:user_id>/events/<int:event_id>/delete', views.delete_event, name='delete_event'),
    path('api/events/<int:event_id>/attendees', views.users_attending_event, name='users_attending_event'),
]