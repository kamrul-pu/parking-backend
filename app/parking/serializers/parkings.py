from rest_framework import serializers


from parking.models import Parking

from parking.choices import ParkingType


class ParkingListSerializer(serializers.ModelSerializer):
    remaining = serializers.IntegerField(read_only=True)

    class Meta:
        model = Parking
        fields = (
            "id",
            "uid",
            "name",
            "slug",
            "description",
            "city",
            "state",
            "address",
            "latitude",
            "longitude",
            "rate",
            "capacity",
            "occupied",
            "remaining",
        )
        read_only_fields = (
            "id",
            "uid",
        )


class ParkingDetailSerializer(ParkingListSerializer):
    class Meta(ParkingListSerializer.Meta):
        fields = ParkingListSerializer.Meta.fields + (
            "parking_type",
            "created_at",
        )
