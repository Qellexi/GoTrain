from unittest.mock import patch

from django.utils import timezone
from datetime import datetime, timezone as tz

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from railway.models.journey import Journey
from railway.models.route import Route
from railway.models.station import Station
from railway.models.ticket import Ticket, Statuses, SeatClass
from railway.models.train import Train, TrainType

User = get_user_model()


class TicketBookingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gotrain.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

        self.train_type = TrainType.objects.create(
            name="Intercity",
            average_speed=120,
        )
        self.train = Train.objects.create(
            name="Test Train",
            train_type=self.train_type,
            cargo_num=5,
            first_class_places=10,
            second_class_places=20,
            economy_places=30,
        )
        self.source = Station.objects.create(
            name="Kyiv", latitude=50.44, longitude=30.48, locality="Kyiv"
        )
        self.destination = Station.objects.create(
            name="Lviv", latitude=49.83, longitude=24.02, locality="Lviv"
        )
        self.route = Route.objects.create(
            source=self.source,
            destination=self.destination,
            distance=540,
            time=330,
        )
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time=datetime(2026, 6, 1, 7, 0, tzinfo=tz.utc),
            base_price=250,
            first_class_multiplier=1.5,
            second_class_multiplier=1.2,
        )

    @patch('railway.signals.delete_unpaid_ticket.apply_async')
    def test_book_ticket(self, mock_celery):
        response = self.client.post(reverse("railway:tickets-list"), {
            "journey": self.journey.id,
            "cargo": 1,
            "seat": 1,
            "seat_class": SeatClass.ECONOMY,
            "passengers": [
                {"first_name": "Test", "last_name": "User", "age": 25}
            ]
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().status, Statuses.BOOKED)

    @patch('railway.signals.delete_unpaid_ticket.apply_async')
    def test_book_already_taken_seat(self, mock_celery):
        # бронюємо перший раз
        self.client.post(reverse("railway:tickets-list"), {
            "journey": self.journey.id,
            "cargo": 1,
            "seat": 1,
            "seat_class": SeatClass.ECONOMY,
            "passengers": [
                {"first_name": "Test", "last_name": "User", "age": 25}
            ]
        }, format="json")

        # бронюємо те саме місце вдруге
        response = self.client.post(reverse("railway:tickets-list"), {
            "journey": self.journey.id,
            "cargo": 1,
            "seat": 1,
            "seat_class": SeatClass.ECONOMY,
            "passengers": [
                {"first_name": "Other", "last_name": "User", "age": 30}
            ]
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('railway.signals.delete_unpaid_ticket.apply_async')
    def test_book_seat_out_of_range(self, mock_celery):
        response = self.client.post(reverse("railway:tickets-list"), {
            "journey": self.journey.id,
            "cargo": 1,
            "seat": 999,
            "seat_class": SeatClass.ECONOMY,
            "passengers": [
                {"first_name": "Test", "last_name": "User", "age": 25}
            ]
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse("railway:tickets-list"), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('railway.signals.delete_unpaid_ticket.apply_async')
    def test_only_own_tickets_visible(self, mock_celery):
        # створюємо квиток для першого юзера
        self.client.post(reverse("railway:tickets-list"), {
            "journey": self.journey.id,
            "cargo": 1,
            "seat": 1,
            "seat_class": SeatClass.ECONOMY,
            "passengers": [
                {"first_name": "Test", "last_name": "User", "age": 25}
            ]
        }, format="json")

        # логінимось як інший юзер
        other_user = User.objects.create_user(
            email="other@gotrain.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=other_user)

        response = self.client.get(reverse("railway:tickets-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
