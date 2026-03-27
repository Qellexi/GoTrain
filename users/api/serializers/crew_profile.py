from rest_framework import serializers
from users.models import CrewProfile

import logging
logger = logging.getLogger(__name__)

class CrewProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = CrewProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "position",
            "hired_at",
        )

    def get_fields(self):
        fields = super().get_fields()
        logger.debug(f"CrewProfileSerializer fields: {fields}")
        return fields


class CrewProfileRetrieveSerializer(CrewProfileSerializer):
    pass  # вже все є в базовому