from django.contrib import admin

from railway.models import Train, TrainType
from railway.models.journey import Journey
from railway.models.order import Order
from railway.models.route import Route
from railway.models.station import Station
from railway.models.ticket import Ticket

# -----------------------
# Station
# -----------------------

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "locality", "latitude", "longitude")
    search_fields = ("name", "locality")
    list_filter = ("locality",)


# -----------------------
# Route
# -----------------------

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance", "time")
    search_fields = ("source__name", "destination__name")
    list_filter = ("source", "destination")


# -----------------------
# Train Type
# -----------------------

@admin.register(TrainType)
class TrainTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# -----------------------
# Train
# -----------------------

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ("name", "train_type", "cargo_num", "places_in_cargo")
    list_filter = ("train_type",)
    search_fields = ("name",)


# -----------------------
# Journey
# -----------------------

@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("route", "train", "departure_time", "arrival_time")
    list_filter = ("route", "departure_time", "train")
    filter_horizontal = ("staff",)


# -----------------------
# Order
# -----------------------

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "user__username")


# -----------------------
# Ticket
# -----------------------

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("cargo", "seat", "journey", "order")
    list_filter = ("journey",)
    search_fields = ("cargo", "seat")
