from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_crew", False)
        extra_fields.setdefault("is_manager", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

class ManagerUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_manager=True)

class CrewUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_crew=True)

class RegularUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_crew=False,
            is_manager=False,
            is_staff=False,
            is_superuser=False,
        )

class User(AbstractUser):
    """User model"""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_crew = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    managers = ManagerUserManager()
    crew = CrewUserManager()
    regular = RegularUserManager()

    def __str__(self):
        return self.email
