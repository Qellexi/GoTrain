from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import CrewProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff", "is_crew")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_crew", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_crew", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_crew"),
        }),
    )


@admin.register(CrewProfile)
class CrewProfileAdmin(admin.ModelAdmin):
    list_display = ("__str__", "position", "hired_at")
    search_fields = ("user__email", "user__first_name", "user__last_name", "position")
    list_filter = ("position", "hired_at")
    autocomplete_fields = ("user",)  # замість dropdown для великої кількості юзерів