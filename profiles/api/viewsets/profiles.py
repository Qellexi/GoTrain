from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from profiles.api.serializers.profiles import ProfileListSerializer, ProfileRetrieveSerializer, ProfileUpdateSerializer
from profiles.models import Profile


class ProfilesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    qs = Profile.objects.all()

    def get_queryset(self):
        if action == "retrieve":
            return self.qs.filter(user=self.request.user)
        return self.qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if action == "list":
            return ProfileListSerializer
        if action == "retrieve":
            return ProfileRetrieveSerializer
        return ProfileUpdateSerializer
