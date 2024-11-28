from django.urls import path, include

urlpatterns = [
    path("", include("parking.urls.parkings"), name="parkings"),
    path("/slots", include("parking.urls.slots"), name="slots"),
    path(
        "/sessions", include("parking.urls.parking_sessions"), name="parking-sessions"
    ),
]
