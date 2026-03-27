from rest_framework import serializers

from railway.api.serializers.ticket import TicketRetrieveSerializer
from railway.models.order import Order
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user")


class OrderRetrieveSerializer(OrderSerializer):
    tickets = TicketRetrieveSerializer(many=True, read_only=True)
