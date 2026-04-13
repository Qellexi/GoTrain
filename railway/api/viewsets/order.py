from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from railway.api.serializers.order import OrderSerializer, OrderRetrieveSerializer, OrderCreateSerializer
from railway.models import Statuses
from railway.models.order import Order


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("tickets")

    def get_serializer_class(self):
        if self.action == "list":
            return OrderSerializer
        if self.action == "retrieve":
            return OrderRetrieveSerializer
        return OrderCreateSerializer

    @action(detail=True, methods=["post"], url_path="pay")
    def pay(self, request, pk=None):
        order = self.get_object()
        tickets = order.tickets.filter(status=Statuses.BOOKED)

        if not tickets.exists():
            return Response(
                {"detail": "No booked tickets in this order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_price = sum(t.price for t in tickets if t.price)
        profile = request.user.profile

        if profile.balance < total_price:
            return Response(
                {"detail": f"Insufficient balance. Required: {total_price}, available: {profile.balance}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # списуємо кошти
        profile.balance -= total_price
        profile.save(update_fields=["balance"])

        # міняємо статус всіх квитків
        tickets.update(status=Statuses.BOUGHT, bought_at=timezone.now())

        return Response({"detail": f"Order paid successfully. Total: {total_price}."})