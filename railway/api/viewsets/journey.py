from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from railway.api.serializers.journey import (
    JourneySerializer,
    JourneyRetrieveSerializer,
    TimetableSerializer, JourneyManagerUpdateSerializer,
)
from railway.filterset.journey import JourneyFilter
from railway.models.journey import Journey
from railway.permissions import IsManager


class JourneyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Journey.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = JourneyFilter

    def get_serializer_class(self):
        if self.action == "list":
            return JourneySerializer
        if self.action == "retrieve":
            return JourneyRetrieveSerializer
        if self.action in ("departures", "arrivals"):
            return TimetableSerializer
        if self.action == "partial_update" or self.action == "update":
            return JourneyManagerUpdateSerializer
        return JourneySerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsManager()]

    def get_serializer(self, *args, **kwargs):
        try:
            return super().get_serializer(*args, **kwargs)
        except Exception as e:
            raise

    def get_queryset(self):
        qs = Journey.objects.select_related(
            "train", "route__source", "route__destination"
        ).prefetch_related(
            "route__route_stations__station",
            "staff",
        )
        return qs

    @action(detail=False, methods=["get"], url_path="departures")
    def departures(self, request):
        """
        Returns journeys departing from a given station.
        Query param: ?station=<station_id>
        """
        station_id = request.query_params.get("station")
        now = timezone.now()
        qs = Journey.objects.select_related(
            "train", "route__source", "route__destination"
        ).filter(
            departure_time__gte=now
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
        now = timezone.now()
        qs = Journey.objects.select_related(
            "train", "route__source", "route__destination"
        ).filter(
            departure_time__gte=now
        ).order_by("arrival_time")

        if station_id:
            qs = qs.filter(route__destination__id=station_id)

        serializer = TimetableSerializer(qs, many=True)
        return Response(serializer.data)
