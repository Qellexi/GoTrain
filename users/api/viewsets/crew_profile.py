from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.api.serializers.crew_profile import CrewProfileRetrieveSerializer, CrewProfileSerializer
from users.models import CrewProfile


class CrewProfileViewSet(viewsets.ModelViewSet):
    queryset = CrewProfile.objects.select_related("user")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return CrewProfileRetrieveSerializer
        return CrewProfileSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return (IsAdminUser(),)
        return super().get_permissions()