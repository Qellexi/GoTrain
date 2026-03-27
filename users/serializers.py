from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from users.models.crew_profile import CrewProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "is_crew",
            "password",
            "is_staff",
        )
        read_only_fields = ("id", "is_crew", "is_staff", "password")

        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
                "label": _("Password"),
            },
        }
    def create(self, validated_data):
        """create user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update user with encrypted password"""
        password = validated_data.pop("password", None)
        user = super().update(instance,validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user

class CrewProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CrewProfile
        fields = ("id", "user", "position", "hired_at")
