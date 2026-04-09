from django.db import models

from railway.models.journey import Journey
from railway.models.order import Order


class Statuses(models.TextChoices):
    PENDING = "pending", "Pending"
    BOOKED = "booked", "Booked"
    BOUGHT = "bought", "Bought"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class SeatClass(models.TextChoices):
    FIRST_CLASS = "first_class", "First Class"
    SECOND_CLASS = "second_class", "Second Class"
    ECONOMY = "economy", "Economy"


class Ticket(models.Model):
    STATUS_TRANSITIONS = {
        Statuses.PENDING: [Statuses.BOOKED, Statuses.CANCELLED],
        Statuses.BOOKED: [Statuses.BOUGHT, Statuses.CANCELLED],
        Statuses.BOUGHT: [Statuses.COMPLETED, Statuses.CANCELLED],
        Statuses.COMPLETED: [],
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

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    seat_class = models.CharField(
        choices=SeatClass.choices,
        default=SeatClass.SECOND_CLASS,
    )

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
