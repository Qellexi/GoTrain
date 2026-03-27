from django.conf import settings
from django.db import models


class CrewProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="crew_profile"
    )
    position = models.CharField(max_length=100, blank=True)
    hired_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Crew: {self.user.first_name} {self.user.last_name}"
