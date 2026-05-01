from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models


class News(models.Model):
    class Type(models.TextChoices):
        DELAY = "delay", "Delay"
        CANCELLATION = "cancellation", "Cancellation"
        PLATFORM_CHANGE = "platform_change", "Platform change"
        GENERAL = "general", "General"

    title = models.CharField(
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(120)
        ]
    )
    short_description = models.CharField(
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(200)
        ]
    )
    full_description = models.TextField(
        validators=[
            MinLengthValidator(50),
            MaxLengthValidator(1000)
        ]
    )
    created_at = models.DateTimeField(null=True, blank=True)

    type = models.CharField(
        max_length=15,
        choices=Type.choices,
        default=Type.GENERAL,
    )

    journey = models.ForeignKey(
        "railway.Journey",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news"
    )

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user} | {self.news}"
