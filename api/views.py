from django.shortcuts import render


# Create your views here.
def get_events(request):
    return render(request, 'api/events.json')
