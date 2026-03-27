from django.urls import path, include
from rest_framework import routers

from users.api.viewsets.crew_profile import CrewProfileViewSet
from users.api.viewsets.user import UserViewSet

app_name = "users"

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"crew", CrewProfileViewSet, basename="crew")

urlpatterns = [
    path('', include(router.urls)),
]