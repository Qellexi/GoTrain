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
        # max_seats = train.places_in_cargo
        taken_by_class = {}
        for seat_class in ["first_class", "second_class", "economy"]:
            taken_by_class[seat_class] = set(
                Ticket.objects.filter(
                    journey_id=journey_id,
                    cargo=cargo,
                    seat_class=seat_class
                ).exclude(status=Statuses.CANCELLED).values_list("seat", flat=True)
            )

        result = {
            "cargo": cargo,
            "first_class": [
                {"seat": i, "is_taken": i in taken_by_class["first_class"]}
                for i in range(1, train.places_in_first_class + 1)
            ],
            "second_class": [
                {"seat": i, "is_taken": i in taken_by_class["second_class"]}
                for i in range(1, train.places_in_second_class + 1)
            ],
            "economy": [
                {"seat": i, "is_taken": i in taken_by_class["economy"]}
                for i in range(1, train.economy_places + 1)
            ],
        }
        return Response(result)
