"""Models for Parking app."""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from common.models import BaseModelWithUID, NameSlugDescriptionBaseModel

from parking.choices import SlotAvailability, PaymentStatus, PaymentMethod, ParkingType

User = get_user_model()


class Parking(NameSlugDescriptionBaseModel):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.JSONField(default=dict)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    capacity = models.IntegerField(default=0)
    parking_type = models.CharField(
        max_length=20, choices=ParkingType.choices, default=ParkingType.OTHER
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.slug}"

    class Meta:
        verbose_name = "Parking"
        verbose_name_plural = "Parkings"


class Slot(BaseModelWithUID):
    name = models.CharField(max_length=50, blank=True)
    parking = models.ForeignKey(
        Parking, related_name="slots", on_delete=models.DO_NOTHING, blank=True
    )
    availability = models.CharField(
        max_length=15,
        choices=SlotAvailability.choices,
        default=SlotAvailability.AVAILABLE,
    )
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    availability_start = models.DateTimeField()  # When the slot becomes available
    availability_end = models.DateTimeField()  # When the slot is no longer available
    duration_limit = models.DurationField(
        default=24
    )  # Maximum duration a user can park
    size = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.availability}"

    def is_available(self):
        return self.status == "available" and timezone.now() < self.availability_end


class ParkingSession(BaseModelWithUID):
    user = models.ForeignKey(
        User, related_name="sessions", on_delete=models.DO_NOTHING, blank=True
    )
    vehicle_number = models.CharField(max_length=20)
    slot = models.ForeignKey(
        Slot, related_name="sessions", on_delete=models.DO_NOTHING, blank=True
    )
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )

    def calculate_cost(self):
        # Calculate the cost of booking based on the duration of the parking slot
        duration = self.exit_time - self.entry_time
        return self.slot.rate * (duration.total_seconds() / 3600)

    def __str__(self) -> str:
        return f"Booking for {self.user.first_name} at {self.slot.name}"


# Payment (Transaction information for the booking)
class Payment(BaseModelWithUID):
    user = models.ForeignKey(
        User, related_name="payments", on_delete=models.DO_NOTHING, blank=True
    )
    session = models.OneToOneField(
        ParkingSession, related_name="payments", on_delete=models.DO_NOTHING, blank=True
    )
    payment_method = models.CharField(
        max_length=50, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )  # Payment method used
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    transaction_id = models.CharField(
        max_length=255, unique=True
    )  # Unique transaction ID

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.payment_status}"
