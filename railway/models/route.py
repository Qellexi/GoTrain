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

    def calculate_time(self, train):
        general_time = (self.distance / train.train_type.average_speed) * 60
        break_time = self.route_stations.aggregate(models.Sum('break_time'))['break_time__sum'] or 0
        return int (general_time + break_time)
