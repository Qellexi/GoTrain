from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from users.api.serializers.user import UserRetrieveSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("retrieve", "list", "me"):
            return UserRetrieveSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return (AllowAny(),)
        if self.action in ("list", "destroy"):
            return (IsAdminUser(),)
        return (IsAuthenticated(),)

    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request):
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)