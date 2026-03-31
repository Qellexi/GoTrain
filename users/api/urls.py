from django.urls import path, include
from rest_framework import routers

from users.api.viewsets.crew_profile import CrewProfileViewSet
from users.api.viewsets.user import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = "users"

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"crew", CrewProfileViewSet, basename="crew")


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]