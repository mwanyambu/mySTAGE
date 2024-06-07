from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import TransportStation, Destination
from .forms import DestinationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import requests
import json
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotAllowed

"""
This module contains the view functions for the application.

Functions:
1. home(request): Renders the home page with a destination form.
2. get_nearest_station(request): Retrieves the nearest transport station for a given destination.
3. signup(request): Handles user signup using the UserCreationForm.
4. login_view(request): Handles user login using the AuthenticationForm.

"""

def home(request):
    """
    Renders the home page with a destination form.
    
    Returns:
    Rendered HTML template with the destination form.
    """
    form = DestinationForm()
    context = {
        'form': form,
        'google_api_key': settings.GOOGLE_API_KEY
    }
    return render(request, 'finder/home.html', context)

def get_nearest_station(request):
    """
    Retrieves the nearest transport station for a given destination.
    Returns:
    JSON response containing the latitude and longitude of the nearest station,
    or an error message if no station is found.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        destination_id = data.get('destination_id', '')

        try:
            destination = Destination.objects.get(id=destination_id)
            station = TransportStation.objects.filter(destination=destination).first()
            if station:
                response_data = {
                    'latitude': station.latitude,
                    'longitude': station.longitude
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'error': 'No station found for this destination'}, status=404)
        except Destination.DoesNotExist:
            return JsonResponse({'error': 'No destination found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def signup(request):
    """
    Handles user signup using the UserCreationForm.

    Returns:
    Rendered HTML template with the signup form.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/signup.html', {'form': form})

def login_view(request):
    """
    Handles user login using the AuthenticationForm.

    Returns:
    Rendered HTML template with the login form.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

def get_sacco_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        destination_id = data.get('destination_id', '')

        try:
            station = TransportStation.objects.get(destination_id=destination_id)
            sacco_info = {
                'sacco_name': station.sacco_name,
                'sacco_number': station.route_number
            }
            return JsonResponse(sacco_info)
        except TransportStation.DoesNotExist:
            return JsonResponse({'error': 'No station found for the specified destination'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def logout_view(request):
    """
    Custom logout view.
    """
    if request.user.is_authenticated:
        # If the user is authenticated, log them out
        from django.contrib.auth import logout
        logout(request)
    # Redirect to the home page after logout
    return redirect('home')