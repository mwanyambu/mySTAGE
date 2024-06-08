from django.test import TestCase
from .models import TransportStation, Destination

class TransportStationModelTests(TestCase):

    def setUp(self):
        self.destination = Destination.objects.create(name='Test Destination')
        self.station = TransportStation.objects.create(
            station_name='Test Station',
            route_number='001',
            sacco_name='Test Sacco',
            latitude=1.2921,
            longitude=36.8219,
            destination=self.destination
        )

    def test_transport_station_creation(self):
        """
        Test that a TransportStation can be created and properly linked to a Destination
        """
        self.assertEqual(self.station.station_name, 'Test Station')
        self.assertEqual(self.station.route_number, '001')
        self.assertEqual(self.station.sacco_name, 'Test Sacco')
        self.assertEqual(self.station.latitude, 1.2921)
        self.assertEqual(self.station.longitude, 36.8219)
        self.assertEqual(self.station.destination, self.destination)

    def test_transport_station_str(self):
        """
        Test the string representation of the TransportStation model
        """
        expected_str = f"{self.station.station_name} ({self.station.route_number}) - {self.station.sacco_name} for {self.station.destination.name}"
        self.assertEqual(str(self.station), expected_str)

    def test_transport_station_update(self):
        """
        Test updating a TransportStation's information
        """
        self.station.station_name = 'Updated Station'
        self.station.save()
        self.assertEqual(self.station.station_name, 'Updated Station')

    def test_transport_station_deletion(self):
        """
        Test deleting a TransportStation
        """
        station_id = self.station.id
        self.station.delete()
        with self.assertRaises(TransportStation.DoesNotExist):
            TransportStation.objects.get(id=station_id)

class DestinationModelTests(TestCase):

    def setUp(self):
        self.destination = Destination.objects.create(name='Test Destination')

    def test_destination_creation(self):
        """
        Test that a Destination can be created
        """
        self.assertEqual(self.destination.name, 'Test Destination')

    def test_destination_str(self):
        """
        Test the string representation of the Destination model
        """
        self.assertEqual(str(self.destination), 'Test Destination')
