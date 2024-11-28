from django.urls import path

from parking.views.slots import SlotList, SlotDetail

urlpatterns = [
    path("", SlotList.as_view(), name="slot-list"),
    path("/<uuid:uid>", SlotDetail.as_view(), name="slot-details"),
]
