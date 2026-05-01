from django.db import models

from railway.models.route import Route
from railway.models.station import Station


class RouteStation(models.Model):
    route = models.ForeignKey("railway.Route", on_delete=models.CASCADE, related_name="route_stations")
    station = models.ForeignKey("railway.Station", on_delete=models.CASCADE)
    order = models.IntegerField()
    break_time = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["route", "order"],
                name="unique_order_per_route",
            )
        ]

    def __str__(self):
        return f"{self.station.name} (order: {self.order})"
