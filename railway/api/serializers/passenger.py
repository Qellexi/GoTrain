from rest_framework import serializers

from railway.models.passenger import Passenger


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("first_name", "last_name", "age")