from django.db import models

"""
Module: models.py

This module contains the database models for the application.

Models:
1. Destination: Represents a destination.
2. TransportStation: Represents a transport station.

"""

class Destination(models.Model):
    """
    Represents a destination.

    Attributes:
    - name: A character field representing the name of the destination.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns the string representation of the destination.

        Returns:
        String: Name of the destination.
        """
        return self.name

class TransportStation(models.Model):
    """
    Represents a transport station.

    Attributes:
    - station_name: A character field representing the name of the station.
    - route_number: A character field representing the route number.
    - sacco_name: A character field representing the name of the sacco.
    - latitude: A float field representing the latitude of the station.
    - longitude: A float field representing the longitude of the station.
    - destination: A foreign key relationship to the Destination model, representing the destination associated with the station.
    """
    station_name = models.CharField(max_length=255)
    route_number = models.CharField(max_length=20)
    sacco_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns the string representation of the transport station.

        Returns:
        String: Name of the station, route number, sacco name, and destination name.
        """
        return f"{self.station_name} ({self.route_number}) - {self.sacco_name} for {self.destination.name}"
