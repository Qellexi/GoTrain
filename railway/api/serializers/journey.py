from rest_framework import serializers

from railway.api.serializers.route import RouteRetrieveSerializer
from railway.api.serializers.train import TrainRetrieveSerializer
from railway.models.journey import Journey
from users.api.serializers.crew_profile import CrewProfileSerializer
from users.models import CrewProfile


class JourneySerializer(serializers.ModelSerializer):
    stations = serializers.SerializerMethodField()
    price_first_class = serializers.SerializerMethodField()
    price_second_class = serializers.SerializerMethodField()
    price_economy_class = serializers.SerializerMethodField()

    def get_price_first_class(self, obj):
        return obj.base_price * obj.first_class_multiplier
    def get_price_second_class(self, obj):
        return obj.base_price * obj.second_class_multiplier
    def get_price_economy_class(self, obj):
        return obj.base_price

    def get_stations(self, obj):
        return obj.route.route_stations.values_list(
            "station__name",
            flat=True  # to return a QuerySet of single values instead of 1-tuples
        )

    class Meta:
        model = Journey
        fields = (
            "id",
            "train",
            "route",
            "stations",
            "departure_time",
            "arrival_time",
            "price_economy_class",
            "price_second_class",
            "price_first_class",
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

class JourneyManagerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = (
            "departure_time",
            "arrival_time",
            "platform",
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
