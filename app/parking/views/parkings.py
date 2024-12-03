import os

from math import cos, radians

from django.db.models import F

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny

from parking.models import Parking


from parking.serializers.parkings import ParkingListSerializer, ParkingDetailSerializer
from parking.utils import calculate_distance

MAX_DISTANCE: int = int(os.environ.get("MAX_DISTANCE", 10000))


class ParkingList(ListCreateAPIView):
    serializer_class = ParkingListSerializer
    queryset = (
        Parking().get_all_actives().annotate(remaining=F("capacity") - F("occupied"))
    )
    permission_classes = ()

    def get_permissions(self):
        request = self.request
        if request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = self.queryset
        city: str = self.request.query_params.get("city", None)
        state: str = self.request.query_params.get("state", None)
        latitude: str = self.request.query_params.get("latitude", None)
        longitude: str = self.request.query_params.get("longitude", None)

        if city:
            queryset = queryset.filter(city__icontains=city)
        if state:
            queryset = queryset.filter(state__icontains=state)

        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)

            # Calculate the range in degrees (for the bounding box filter)
            lat_distance = MAX_DISTANCE / 111000  # degrees latitude
            lon_distance = MAX_DISTANCE / (
                111000 * cos(radians(latitude))
            )  # degrees longitude

            # Calculate min and max for latitude and longitude
            min_latitude = latitude - lat_distance
            max_latitude = latitude + lat_distance
            min_longitude = longitude - lon_distance
            max_longitude = longitude + lon_distance

            # Apply the bounding box filter
            queryset = queryset.filter(
                latitude__range=[min_latitude, max_latitude],
                longitude__range=[min_longitude, max_longitude],
            )

            # Calculate the distance for each parking location
            # Annotate queryset with the calculated distance for each parking
            for parking in queryset:
                parking.distance = calculate_distance(
                    latitude, longitude, parking.latitude, parking.longitude
                )

        return queryset


class ParkingDetail(RetrieveUpdateAPIView):
    serializer_class = ParkingDetailSerializer
    queryset = Parking().get_all_non_inactives()
    permission_classes = (IsAdminUser,)
    lookup_field = "uid"
