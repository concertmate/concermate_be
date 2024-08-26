from django.urls import path
from . import views

urlpatterns = [
    path('api/create', views.EventView.as_view(), name='create_event'),
]