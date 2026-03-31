from django.db.models.signals import post_save
from django.dispatch import receiver

from railway.models import Ticket
from tasks import delete_unpaid_ticket


@receiver(post_save, sender=Ticket)
def schedule_ticket_cancellation(sender, instance, created, **kwargs):
    if created:
        delete_unpaid_ticket.apply_async(args=(instance.id,), countdown=60*15)
