from django.urls import path

from parking.views.parkings import ParkingList, ParkingDetail


urlpatterns = [
    path("", ParkingList.as_view(), name="parking-list"),
    path("/<uuid:uid>", ParkingDetail.as_view(), name="parking-detail"),
]
