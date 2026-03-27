from django.db import models

from railway.models.journey import Journey
from railway.models.order import Order

class TicketStatuses(models.TextChoices):
    BOOKED = "booked"
    BOUGHT = "bought"
    CANCELLED = "cancelled"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(
        Journey,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        choices=TicketStatuses.choices,
    )
    booked_at = models.DateTimeField(auto_now_add=True)
    bought_at = models.DateTimeField(auto_now_add=True)
    payment_confirmation = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["journey", "cargo", "seat"],
                name="unique_seat_per_journey",
            )
        ]

    def __str__(self):
        return (f"Journey {self.journey.route.source}-{self.journey.route.destination}"
                f" | Cargo {self.cargo} | Seat {self.seat}")
