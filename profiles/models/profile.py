from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    avatar = models.ImageField(
        upload_to="profiles/avatars/",
        blank=True,
        null=True
    )
    phone_number = models.CharField(max_length=15, blank=True)
    alternative_email = models.EmailField(blank=True)
    date_of_birth = models.DateField()

    points = models.PositiveIntegerField(default=0)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    def __str__(self):
        return f"Profile for {self.user.username}"

    @property
    def total_journeys(self):
        return self.user.orders.filter(
            tickets__status="bought"
        ).count()
