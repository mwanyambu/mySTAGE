from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import TransportStation, Destination
from .forms import DestinationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import requests
import json

def home(request):
    form = DestinationForm()
    context = {'form': form}
    return render(request, 'transportation/home.html', context)

def get_nearest_station(request):
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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})