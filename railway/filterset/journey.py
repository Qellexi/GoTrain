from django_filters import rest_framework as filters

from railway.models import Journey


class JourneyFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="departure_time", lookup_expr="date")
    source = filters.CharFilter(field_name="route__source__id")
    destination = filters.CharFilter(field_name="route__destination__id")

    class Meta:
        model = Journey
        fields = ["date", "source", "destination"]
