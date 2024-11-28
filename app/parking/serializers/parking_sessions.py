from rest_framework import serializers


from parking.models import ParkingSession


class SessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSession
        fields = (
            "user",
            "vehicle_number",
            "slot",
            "entry_time",
            "exit_time",
            "total_amount",
            "payment_status",
        )


class SessionDetailSerializer(SessionListSerializer):
    class Meta(SessionListSerializer.Meta):
        fields = SessionListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
        )
