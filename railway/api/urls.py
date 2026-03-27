from django.urls import path, include
from rest_framework import routers

from railway.api.viewsets.journey import JourneyViewSet
from railway.api.viewsets.ticket import TicketViewSet

app_name = "railway"

router = routers.DefaultRouter()

router.register(r"journeys", JourneyViewSet, basename="journeys")
router.register(r"tickets", TicketViewSet, basename="trains")
# router.register()
urlpatterns = [
    path('', include(router.urls)),
]