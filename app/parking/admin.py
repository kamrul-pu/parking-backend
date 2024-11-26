"""Include models in the Default Admin Panel."""

from django.contrib import admin

from parking.models import Parking, Slot, ParkingSession, Payment


class ParkingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "name",
        "address",
        "capacity",
        "status",
    )


admin.site.register(Parking, ParkingAdmin)


class SlotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "name",
        "availability",
        "rate",
    )


admin.site.register(Slot, SlotAdmin)


class ParkingSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "entry_time",
        "exit_time",
        "total_amount",
        "payment_status",
    )


admin.site.register(ParkingSession, ParkingSessionAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "payment_status",
        "payment_method",
    )


admin.site.register(Payment, PaymentAdmin)
