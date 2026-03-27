from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_crew",
        )
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
            "is_crew": {"read_only": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserRetrieveSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_crew",
            "is_staff",
        )
        extra_kwargs = {
            "is_crew": {"read_only": True},
            "is_staff": {"read_only": True},
        }