from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from railway.api.serializers.ticket import TicketSerializer, TicketRetrieveSerializer, \
    TicketBookingSerializer, TicketPurchaseSerializer
from railway.models.ticket import Ticket, TicketStatuses


class TicketViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TicketSerializer
        if self.action == "retrieve":
            return TicketRetrieveSerializer
        if self.request.method in ("PATCH", "PUT"):
            ticket = self.get_object()
            if ticket.status==TicketStatuses.BOOKED:
                return TicketPurchaseSerializer
        return TicketBookingSerializer

    def get_queryset(self):
        qs = self.queryset

        return qs