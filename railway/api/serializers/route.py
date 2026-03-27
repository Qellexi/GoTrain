from rest_framework import serializers

from railway.api.serializers.station import StationReadSerializer
from railway.models.route import Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance", "time")


class RouteRetrieveSerializer(RouteSerializer):
    source = StationReadSerializer(read_only=True)
    destination = StationReadSerializer(read_only=True)
    stations = serializers.SerializerMethodField()
    def get_stations(self, obj):
        return obj.route_stations.values_list(
            "station__name",
            flat=True  #to return a QuerySet of single values instead of 1-tuples
        )
    class Meta:
        model = Route
        fields = ["id", "source", "destination", "stations"]
