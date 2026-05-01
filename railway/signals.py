from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from railway.models import Ticket, Journey, News, Statuses, Notification
from railway.tasks import delete_unpaid_ticket
from users.models import User


@receiver(post_save, sender=Ticket)
def schedule_ticket_cancellation(sender, instance, created, **kwargs):
    if created:
        delete_unpaid_ticket.apply_async(args=(instance.id,), countdown=60*15)


@receiver(post_save, sender=Ticket)
def update_profile_points(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Ticket.objects.get(pk=instance.pk)
    except Ticket.DoesNotExist:
        return

    if old.status == Statuses.BOOKED and instance.status == Statuses.BOUGHT:
        profile = instance.order.user.profile
        profile.points += 50
        profile.save(update_fields=['points'])

@receiver(post_save, sender=Journey)
def journey_changed(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Journey.objects.get(pk=instance.pk)
    except Journey.DoesNotExist:
        return

    if old.departure_time != instance.departure_time:
        News.objects.create(
            title=f"Journey {instance.id} departure time changed",
            full_description=f"Journey {instance.id} departure time changed from "
                             f"{old.departure_time} to {instance.departure_time}",
            type=News.Type.DELAY,
            journey=instance,
        )

    if old.arrival_time != instance.arrival_time:
        News.objects.create(
            title=f"Journey {instance.id} arrival time changed",
            full_description=f"Journey {instance.id} arrival time changed from "
                             f"{old.arrival_time} to {instance.arrival_time}",
            type=News.Type.DELAY,
            journey=instance,
        )

    if old.platform != instance.platform:
        News.objects.create(
            title=f"Platform change: {instance.route}",
            full_description=f"Platform changed from {old.platform} to {instance.platform}",
            type=News.Type.PLATFORM_CHANGE,
            journey=instance,
        )

@receiver(post_delete, sender=Journey)
def journey_deleted(sender, instance, **kwargs):
    News.objects.create(
        title=f"Journey {instance.id} deleted",
        full_description=f"Journey {instance.route} | {instance.departure_time} has been cancelled.",
        type=News.Type.CANCELLATION,
        journey=None, #journey is deleted
    )

@receiver(post_save, sender=News)
def create_notifications(sender, instance, created, **kwargs):
    if created and instance.journey:
        users = User.objects.filter(
            tickets__journey=instance.journey,
            tickets__status__in=[Statuses.BOOKED, Statuses.BOUGHT]
        ).distinct()

        notifications = [
            Notification(user=user, news=instance)
            for user in users
        ]
        Notification.objects.bulk_create(notifications)
