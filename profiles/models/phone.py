from django.db import models
from django.utils import timezone


class PhoneVerification(models.Model):
    profile = models.OneToOneField(
        "Profile",
        on_delete=models.CASCADE,
        related_name="phone_verification"
    )
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return self.expires_at < timezone.now()
