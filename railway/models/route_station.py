from django.db import models

from railway.models.route import Route
from railway.models.station import Station


class RouteStation(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route_stations")
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["route", "order"],
                name="unique_order_per_route",
            )
        ]

    def __str__(self):
        pass
