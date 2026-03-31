from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet

from railway.api.serializers.news import NewsReadSerializer, NewsDetailSerializer, NewsWriteSerializer
from railway.models import News
from railway.permissions import IsManager


class NewsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = News.objects.all()

    def get_permissions(self):
        if self.action in ("create", "update"):
            return [IsAuthenticated(), IsAdminUser(), IsManager()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsReadSerializer
        elif self.action == "retrieve":
            return NewsDetailSerializer
        return NewsWriteSerializer
