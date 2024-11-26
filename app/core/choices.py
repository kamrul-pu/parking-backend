from django.db.models import TextChoices


class UserKind(TextChoices):
    ADMIN = "ADMIN", "Admin"
    CUSTOMER = "CUSTOMER", "Customer"
    CUSTOMER_SERVICE = "CUSTOMER_SERVICE", "Customer_Service"
    MANAGER = "MANAGER", "Manager"
    LOCATION_MANAGER = "LOCATION_MANAGER", "Location_Manager"
    OTHER = "OTHER", "Other"
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    UNDEFINED = "UNDEFINED", "Undefined"


class UserGender(TextChoices):
    FEMALE = "FEMALE", "Female"
    MALE = "MALE", "Male"
    UNKNOWN = "UNKNOWN", "Unknown"
    OTHER = "OTHER", "Other"
