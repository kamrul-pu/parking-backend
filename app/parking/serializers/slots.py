from rest_framework import serializers


from parking.models import Slot


class SlotListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = (
            "id",
            "uid",
            "availability",
            "rate",
            "duration_limit",
            "size",
        )
        read_only_fields = (
            "id",
            "uid",
        )


class SlotDetailSerializer(SlotListSerializer):
    class Meta(SlotListSerializer.Meta):
        fileds = SlotListSerializer.Meta.fields + (
            "created_at",
            "updated_at",
            "status",
        )
