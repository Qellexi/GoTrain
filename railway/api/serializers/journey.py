from rest_framework import serializers

from railway.api.serializers.route import RouteRetrieveSerializer
from railway.api.serializers.train import TrainRetrieveSerializer
from railway.models.journey import Journey
from users.api.serializers.crew_profile import CrewProfileSerializer
from users.models import CrewProfile


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = (
            "id",
            "train",
            "route",
            "departure_time",
            "arrival_time",
        )

        read_only_fields = ("arrival_time",)

class JourneyRetrieveSerializer(JourneySerializer):
    route = RouteRetrieveSerializer(read_only=True)
    train = TrainRetrieveSerializer(read_only=True)

    staff = CrewProfileSerializer(many=True, read_only=True)

    class Meta(JourneySerializer.Meta):
        fields = JourneySerializer.Meta.fields + ("staff",)


class JourneyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "train",
            "departure_time",
            "staff",
        )


class TimetableSerializer(serializers.ModelSerializer):
    source_station = serializers.CharField(source="route.source", read_only=True)
    destination_station = serializers.CharField(source="route.destination", read_only=True)
    train_name = serializers.CharField(source="train.name", read_only=True)

    class Meta:
        model = Journey
        fields = (
            "id",
            "train_name",
            "source_station",
            "destination_station",
            "departure_time",
            "arrival_time",
        )
