from django import forms
from .models import Destination

"""
Module: forms.py

This module contains the form definitions for the application.

Forms:
1. DestinationForm: Form for selecting a destination.

"""

class DestinationForm(forms.Form):
    """
    Form for selecting a destination.

    Fields:
    - destination: A dropdown field allowing users to select a destination.
    """
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), label="Where are you heading to?")