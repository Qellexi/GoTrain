from datetime import timedelta

from django.db import models

from railway.models import Train
from railway.models.route import Route
from users.models.crew_profile import CrewProfile


class Journey(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="journeys",
    )
    train = models.ForeignKey(
        Train,
        on_delete=models.CASCADE,
        related_name="journeys",
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    staff = models.ManyToManyField(CrewProfile)

    def save(self, *args, **kwargs):
        if self.departure_time and self.route_id:
            self.arrival_time = self.departure_time + timedelta(minutes=self.route.time)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.route} | {self.train} | {self.departure_time}"