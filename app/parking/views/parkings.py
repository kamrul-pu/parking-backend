from math import cos, radians

from django.db.models import F

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny

from parking.models import Parking


from parking.serializers.parkings import ParkingListSerializer, ParkingDetailSerializer

from math import radians, cos


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
            queryset = queryset.filter(state__iexact=state)
        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)

            # Set max_distance to 1000 meters (1km)
            max_distance = 1000

            # Calculate the range in degrees
            lat_distance = max_distance / 111000
            lon_distance = max_distance / (111000 * cos(radians(latitude)))

            # Calculate min and max for latitude and longitude
            min_latitude = latitude - lat_distance
            max_latitude = latitude + lat_distance
            min_longitude = longitude - lon_distance
            max_longitude = longitude + lon_distance

            # Apply the filtering for latitude and longitude range
            queryset = queryset.filter(
                latitude__range=[min_latitude, max_latitude],
                longitude__range=[min_longitude, max_longitude],
            )
        return queryset


class ParkingDetail(RetrieveUpdateAPIView):
    serializer_class = ParkingDetailSerializer
    queryset = Parking().get_all_non_inactives()
    permission_classes = (IsAdminUser,)
    lookup_field = "uid"
