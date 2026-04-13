from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from railway.api.serializers.ticket import TicketSerializer, TicketRetrieveSerializer, \
    TicketBookingSerializer, TicketUpdateSerializer
from railway.models.ticket import Ticket, Statuses


class TicketViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return TicketSerializer
        if self.action == "retrieve":
            return TicketRetrieveSerializer
        if self.request.method in ("PATCH", "PUT"):
            ticket = self.get_object()
            if ticket.status==Statuses.BOOKED and ticket.order is None:
                return TicketUpdateSerializer
        return TicketBookingSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()
        return Response({
            "detail": "Ticket booked successfully",
            "ticket": TicketSerializer(ticket).data
        }, status=status.HTTP_201_CREATED)
