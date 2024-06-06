from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TransportStation(models.Model):
    route_name = models.CharField(max_length=255)
    route_number = models.CharField(max_length=20)
    sacco_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.route_name} ({self.route_number}) - {self.sacco_name} for {self.destination.name}"
