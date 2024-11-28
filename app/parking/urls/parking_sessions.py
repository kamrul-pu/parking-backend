from django.urls import path

from parking.views.parking_sessions import ParkingSessionList, ParkingSessionDetail


urlpatterns = [
    path("", ParkingSessionList.as_view(), name="parking-session-list"),
    path("/<uuid:uid>", ParkingSessionDetail.as_view(), name="parking-session-detail"),
]
