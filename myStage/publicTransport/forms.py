from django import forms
from .models import Destination

class DestinationForm(forms.Form):
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), label="Where are you heading to?")