from rest_framework import serializers

from railway.api.serializers.ticket import TicketRetrieveSerializer
from railway.models import Ticket, Statuses
from railway.models.order import Order
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user")


class OrderRetrieveSerializer(OrderSerializer):
    tickets = TicketRetrieveSerializer(many=True, read_only=True)


class OrderCreateSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.filter(status=Statuses.BOOKED),
        many=True,
    )
    class Meta:
        model = Order
        fields = ("tickets",)

    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        request = self.context['request']
        order = Order.objects.create(user=request.user, **validated_data)
        for ticket in tickets_data:
            ticket.order = order
            ticket.save(update_fields=['order'])
        delete_unpaid_ticket.apply_async(
            args=(ticket.id,),
            countdown=60 * 15,
        )
        return order