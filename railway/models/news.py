from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models


class News(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title