from rest_framework import serializers

from profiles.models import Profile


class ProfileListSerializer(serializers.ModelSerializer):
    """
    List serializer for Profile model.
    """
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "phone_number",
        )

class ProfileRetrieveSerializer(serializers.ModelSerializer):
    """
    Detail serializer for Profile model.
    """
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "avatar",
            "phone_number",
            "alternative_email",
            "date_of_birth",
            "points",
            "balance",
            "total_journeys"
        )

class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Update serializer for Profile model.
    """
    class Meta:
        model = Profile
        fields = (
            "avatar",
            "phone_number",
            "alternative_email",
            "date_of_birth",
        )
