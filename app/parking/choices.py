from django.db.models import TextChoices


class ParkingType(TextChoices):
    OPEN = "OPEN", "Open"
    COVERED = "COVERED", "Covered"
    UNDERGROUND = "UNDERGROUND", "Underground"
    OTHER = "OTHER", "Other"


class SlotAvailability(TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    BOOKED = "BOOKED", "Booked"
    OCCUPIED = "OCCUPIED", "Occupied"


class PaymentStatus(TextChoices):
    PAID = "PAID", "Paid"
    PENDING = "PENDING", "Pending"


class PaymentMethod(TextChoices):
    BANK = "BANK", "Bank"
    CARD = "CARD", "Card"
    CASH = "CASH", "Cash"
    PASS = "PASS", "Pass"
