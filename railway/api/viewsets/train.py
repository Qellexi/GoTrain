from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from railway.api.serializers.train import TrainSerializer, TrainRetrieveSerializer
from railway.models import Train, Ticket, Statuses


class TrainViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Train.objects.all()


    def get_serializer_class(self):
        if self.action == "list":
            return TrainSerializer
        elif self.action == "retrieve":
            return TrainRetrieveSerializer
        return TrainSerializer

    @action(detail=True, methods=["get"], url_path="seats")
    def seats(self, request, pk=None):
        train = self.get_object()
        cargo = request.query_params.get("cargo")
        journey_id = request.query_params.get("journey")
        max_seats = train.places_in_cargo
        taken = set(
            Ticket.objects.filter(
                journey_id=journey_id,
                cargo=cargo
            ).exclude(status=Statuses.CANCELLED).values_list("seat", flat=True)
        )
        seats = set(range(1, max_seats + 1)) - taken
        return Response({"cargo": cargo, "seats": list(seats)})