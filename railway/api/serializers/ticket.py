from django.utils import timezone

from rest_framework import serializers

from railway.api.serializers.journey import JourneyRetrieveSerializer
from railway.api.serializers.station import StationReadSerializer
from railway.models import Order
from railway.models.ticket import Ticket, Statuses
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
    class Meta:
        model = Ticket
        fields = (
            "cargo",
            "seat",
            "journey"
        )
        validators = []

    def create(self, validated_data):
        request = self.context['request']
        validated_data["status"] = Statuses.BOOKED
        validated_data["booked_at"] = timezone.now()
        ticket = Ticket.objects.create(**validated_data)

        return ticket

    def validate(self, data):
        journey = data["journey"]
        seat = data["seat"]
        cargo = data["cargo"]

        already_taken = Ticket.objects.filter(
            journey=journey,
            seat=seat,
            cargo=cargo,
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

    def update(self, instance, validated_data):
        instance.status = "bought"
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
        already_taken = Ticket.objects.filter(
            journey=journey,
            seat=seat,
            cargo=cargo,
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