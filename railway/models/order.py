from django.conf import settings
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ticket_ids = ", ".join(str(ticket.id) for ticket in self.tickets.all())
        return f"Order {self.id} | Tickets: [{ticket_ids}]"