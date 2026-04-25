from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from profiles.api.serializers.profiles import ProfileListSerializer, ProfileRetrieveSerializer, ProfileUpdateSerializer
from profiles.models import Profile


class ProfilesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    qs = Profile.objects.all()

    def get_queryset(self):
        if self.action == "retrieve":
            return self.qs.filter(user=self.request.user)
        return self.qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileRetrieveSerializer
        return ProfileUpdateSerializer

    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request):
        profile = Profile.objects.get(user=request.user)
        if request.method == "PATCH":
            serializer = ProfileUpdateSerializer(
                profile,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = ProfileRetrieveSerializer(profile)
        return Response(serializer.data)