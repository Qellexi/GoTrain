from rest_framework import serializers

from railway.models.station import Station


class StationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = (
            "id",
            "name",
            "locality"
        )