import traceback

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from railway.api.serializers.journey import (
    JourneySerializer,
    JourneyRetrieveSerializer,
    TimetableSerializer,
)
from railway.models.journey import Journey


class JourneyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Journey.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return JourneySerializer
        elif self.action == "retrieve":
            return JourneyRetrieveSerializer
        elif self.action in ("departures", "arrivals"):
            return TimetableSerializer
        return JourneySerializer

    def get_serializer(self, *args, **kwargs):
        try:
            return super().get_serializer(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            raise

    def get_queryset(self):
        qs = self.queryset

        if self.action in ("list", "retrieve"):
            return qs.prefetch_related("train")

        return qs.distinct()

    @action(detail=False, methods=["get"], url_path="departures")
    def departures(self, request):
        """
        Returns journeys departing from a given station.
        Query param: ?station=<station_id>
        """
        station_id = request.query_params.get("station")
        qs = Journey.objects.select_related(
            "train", "route__source", "route__destination"
        ).order_by("departure_time")

        if station_id:
            qs = qs.filter(route__source__id=station_id)

        serializer = TimetableSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="arrivals")
    def arrivals(self, request):
        """
        Returns journeys arriving at a given station.
        Query param: ?station=<station_id>
        """
        station_id = request.query_params.get("station")
        qs = Journey.objects.select_related(
            "train", "route__source", "route__destination"
        ).order_by("arrival_time")

        if station_id:
            qs = qs.filter(route__destination__id=station_id)

        serializer = TimetableSerializer(qs, many=True)
        return Response(serializer.data)