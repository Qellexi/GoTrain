from celery import shared_task

from railway.models import Ticket, Statuses, Order


@shared_task
def delete_unpaid_ticket(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return

    if ticket.status == Statuses.BOOKED:
        order = ticket.order
        ticket.delete()
        if order is not None and not order.tickets.exists(): # якщо більше немає квитків в цьому order
            order.delete()              # видаляємо і сам order
