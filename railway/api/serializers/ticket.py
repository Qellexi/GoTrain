from datetime import timezone

from rest_framework import serializers

from railway.api.serializers.journey import JourneyRetrieveSerializer
from railway.api.serializers.station import StationReadSerializer
from railway.models.ticket import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "cargo",
            "seat",
            "journey",
            "order",
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

    def create(self, validated_data):
        validated_data["status"] = "booked"
        validated_data["booked_at"] = timezone.now()
        return super().create(validated_data)


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
