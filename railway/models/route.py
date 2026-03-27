from django.db import models

from railway.models.station import Station


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='routes_from',
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='routes_to',
    )
    distance = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.IntegerField()

    def __str__(self):
        return f"{self.source} -> {self.destination}"
