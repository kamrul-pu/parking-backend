from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from parking.models import Slot

from parking.serializers.slots import SlotListSerializer, SlotDetailSerializer


class SlotList(ListCreateAPIView):
    permission_classes = ()
    serializer_class = SlotListSerializer
    queryset = Slot().get_all_actives()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminUser()]


class SlotDetail(RetrieveUpdateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SlotDetailSerializer
    queryset = Slot().get_all_non_inactives()
    lookup_field = "uid"
