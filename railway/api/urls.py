from django.urls import path, include
from rest_framework import routers

from railway.api.viewsets.journey import JourneyViewSet
from railway.api.viewsets.news import NewsViewSet
from railway.api.viewsets.ticket import TicketViewSet
from railway.api.viewsets.train import TrainViewSet

app_name = "railway"

router = routers.DefaultRouter()

router.register(r"journeys", JourneyViewSet, basename="journeys")
router.register(r"tickets", TicketViewSet, basename="tickets")
router.register(r"trains", TrainViewSet, basename="trains")
router.register(r"news", NewsViewSet, basename="news")

# router.register()
urlpatterns = [
    path('', include(router.urls)),
]