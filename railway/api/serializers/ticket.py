from django.utils import timezone

from rest_framework import serializers

from railway.api.serializers.journey import JourneyRetrieveSerializer
from railway.api.serializers.passenger import PassengerSerializer
from railway.api.serializers.station import StationReadSerializer
from railway.models import Order
from railway.models.passenger import Passenger
from railway.models.ticket import Ticket, Statuses, SeatClass
from railway.tasks import delete_unpaid_ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "cargo",
            "seat",
            "journey",
            "order",
            "status",
            "booked_at",
            "bought_at",
        )


class TicketRetrieveSerializer(TicketSerializer):
    journey = JourneyRetrieveSerializer(read_only=True)
    station = StationReadSerializer(read_only=True)


class TicketBookingSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True)

    class Meta:
        model = Ticket
        fields = (
            "journey",
            "cargo",
            "seat",
            "journey",
            "seat_class",
            "passengers"
        )
        validators = []

    def create(self, validated_data):
        request = self.context['request']
        passengers_data = validated_data.pop('passengers')

        validated_data["status"] = Statuses.BOOKED
        validated_data["booked_at"] = timezone.now()
        ticket = Ticket.objects.create(**validated_data)

        for passenger in passengers_data:
            Passenger.objects.create(ticket=ticket, **passenger)

        delete_unpaid_ticket.apply_async(
            args=(ticket.id,),
            countdown=60 * 15,
        )

        return ticket

    def validate(self, data):
        journey = data["journey"]
        seat = data["seat"]
        cargo = data["cargo"]
        seat_class = data["seat_class"]

        # перевірка діапазону місць залежно від класу
        if seat_class == SeatClass.FIRST:
            max_seats = journey.train.first_class_places
        elif seat_class == SeatClass.SECOND:
            max_seats = journey.train.second_class_places
        else:
            max_seats = journey.train.economy_class_places

        if seat < 1 or seat > max_seats:
            raise serializers.ValidationError({
                "seat": f"Seat must be between 1 and {max_seats} for {seat_class} class."
            })

        already_taken = Ticket.objects.filter(
            journey=journey,
            seat=seat,
            cargo=cargo,
            seat_class=seat_class,
        ).exclude(status=Statuses.CANCELLED).exists()

        if already_taken:
            raise serializers.ValidationError({
                "seat": f"Seat {seat} in cargo {cargo} is already taken!"
            })
        return data


class TicketPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("payment_confirmation",)
    def validate(self, data):
        request = self.context['request']
        instance = self.instance

        if instance.price is None:
            raise serializers.ValidationError({
                "price": "Ticket price is not set!"
            })
        profile = request.user.profile
        if profile.balance < instance.price:
            raise serializers.ValidationError({
                "balance": "Insufficient balance!"
            })
        return data

    def update(self, instance, validated_data):
        request = self.context['request']
        profile = request.user.profile

        #списуємо кошти
        profile.balance -= instance.price
        profile.save(update_fields=["balance"])

        instance.status = Statuses.BOUGHT
        instance.bought_at = timezone.now()
        instance.payment_confirmation = validated_data["payment_confirmation"]
        instance.save()
        return instance

class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "cargo",
            "seat",
        )
        validators = []
    def validate(self, data):
        instance = self.instance # поточний Ticket з БД
        journey = instance.journey
        seat = data.get("seat", instance.seat) # новий seat або старий якщо не передали
        cargo = data.get("cargo", instance.cargo) # новий cargo або старий якщо не передали
        seat_class = data["seat_class"]

        already_taken = Ticket.objects.filter(
            journey=journey,
            seat=seat,
            cargo=cargo,
            seat_class=seat_class,
        ).exclude(status=Statuses.CANCELLED).exists()

        if already_taken:
            raise serializers.ValidationError({
                "seat": f"Seat {seat} in cargo {cargo} is already taken!"
            })
        return data

    def update(self, instance, validated_data):
        if instance.status != Statuses.BOOKED:
            raise serializers.ValidationError({
                "status": f"Ticket must be in {Statuses.BOOKED} status to be updated!"
            })
        if instance.order is not None:
            raise serializers.ValidationError({
                "order": f"Ticket must not have an order to be updated!"
            })
        return super().update(instance, validated_data)