from django.db import models

from railway.models.journey import Journey
from railway.models.order import Order

class Statuses(models.TextChoices):
    PENDING = "pending"
    BOOKED = "booked"
    BOUGHT = "bought"
    CANCELLED = "cancelled"


class Ticket(models.Model):
    STATUS_TRANSITIONS = {
        Statuses.PENDING: [Statuses.BOOKED, Statuses.CANCELLED],
        Statuses.BOOKED: [Statuses.BOUGHT, Statuses.CANCELLED],
        Statuses.BOUGHT: [],
        Statuses.CANCELLED: [],
    }

    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(
        Journey,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
        null=True,
        blank=True
    )
    status = models.CharField(
        choices=Statuses.choices,
        default=Statuses.PENDING,
    )
    booked_at = models.DateTimeField(null=True, blank=True)
    bought_at = models.DateTimeField(null=True, blank=True)
    payment_confirmation = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["journey", "cargo", "seat"],
                name="unique_seat_per_journey",
            )
        ]
    def set_status(self, status, save=True):
        if status not in self.STATUS_TRANSITIONS[self.status]:
            raise ValueError(f"Invalid status transition from {self.status} to {status}")
        self.status = status
        if save:
            self.save(update_fields=["status"])

    def __str__(self):
        return (f"Journey {self.journey.route.source}-{self.journey.route.destination}"
                f" | Cargo {self.cargo} | Seat {self.seat}")
