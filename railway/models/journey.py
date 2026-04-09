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

    platform = models.PositiveIntegerField(default=1)

    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    first_class_multiplier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=2  # перший клас = base_price * 2
    )
    second_class_multiplier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.5  # другий клас = base_price * 1.5
    )

    def save(self, *args, **kwargs):
        if self.departure_time and self.route_id and self.train_id:
            total_time = self.route.calculate_time(self.train)
            self.arrival_time = self.departure_time + timedelta(minutes=total_time)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.route} | {self.train} | {self.departure_time}"