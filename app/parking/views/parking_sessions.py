from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from parking.models import ParkingSession

from parking.serializers.parking_sessions import (
    SessionListSerializer,
    SessionDetailSerializer,
)


class ParkingSessionList(ListCreateAPIView):
    permission_classes = ()
    serializer_class = SessionListSerializer
    queryset = ParkingSession().get_all_actives()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminUser()]


class ParkingSessionDetail(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SessionDetailSerializer
    queryset = ParkingSession().get_all_non_inactives()
    lookup_field = "uid"
