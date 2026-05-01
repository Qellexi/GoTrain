from django.db import models

from railway.models import Ticket


class Passenger(models.Model):
    ticket = models.ForeignKey(
        "railway.Ticket",
        on_delete=models.CASCADE,
        related_name="passengers"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
