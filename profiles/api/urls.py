from django.urls import path, include
from rest_framework import routers

from profiles.api.viewsets.profiles import ProfilesViewSet

app_name = "profiles"

router = routers.DefaultRouter()

router.register(r"profiles", ProfilesViewSet, basename="profiles")

# router.register()
urlpatterns = [
    path('', include(router.urls)),
]