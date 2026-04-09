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

    def __str__(self):
        return self.title

class Notification(models.Model):
    title = models.CharField(
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(50)
        ]
    )
    short_description = models.CharField(
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(100)
        ]
    )
    full_description = models.TextField(
        validators=[
            MinLengthValidator(50),
            MaxLengthValidator(200)
        ]
    )
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title