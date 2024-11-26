from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

import factory


from core.tests import UserFactory
from parking.models import Parking, Slot, ParkingSession, Payment
from parking.choices import ParkingType, PaymentMethod, PaymentStatus, SlotAvailability

User = get_user_model()


# Factory for Parking Model
class ParkingFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company")
    city = factory.Faker("city")
    state = factory.Faker("state")
    address = factory.Faker("address")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    location = factory.LazyAttribute(
        lambda o: {"latitude": o.latitude, "longitude": o.longitude}
    )
    rate = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    capacity = factory.Faker("random_int", min=10, max=100)
    parking_type = factory.Iterator(
        [
            ParkingType.COVERED,
            ParkingType.OPEN,
            ParkingType.UNDERGROUND,
            ParkingType.OTHER,
        ]
    )

    class Meta:
        model = Parking


# Factory for Slot Model
class SlotFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    parking = factory.SubFactory(ParkingFactory)
    availability = factory.Iterator(
        [SlotAvailability.AVAILABLE, SlotAvailability.OCCUPIED]
    )
    rate = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    availability_start = factory.LazyFunction(timezone.now)
    availability_end = factory.LazyFunction(lambda: timezone.now() + timedelta(hours=3))
    duration_limit = factory.Faker(
        "time_delta", end_datetime=timezone.now() + timedelta(days=1)
    )
    size = factory.Faker("word")

    class Meta:
        model = Slot


# Factory for ParkingSession Model
class ParkingSessionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    # Generate a vehicle number: a letter, a hyphen, and digits
    vehicle_number = factory.LazyAttribute(
        lambda o: f"{factory.Faker.random_letter().upper()}-{factory.faker.random_number(digits=5)}"
    )
    slot = factory.SubFactory(SlotFactory)
    entry_time = factory.LazyFunction(timezone.now)
    exit_time = factory.LazyFunction(lambda: timezone.now() + timedelta(hours=2))
    total_amount = factory.LazyAttribute(lambda o: o.calculate_cost())
    payment_status = factory.Iterator([PaymentStatus.PENDING, PaymentStatus.PAID])

    class Meta:
        model = ParkingSession


# Factory for Payment Model
class PaymentFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(
        "core.factories.UserFactory"
    )  # Assuming you have a UserFactory
    session = factory.SubFactory(ParkingSessionFactory)
    payment_method = factory.Iterator([PaymentMethod.CARD, PaymentMethod.CASH])
    payment_status = factory.Iterator([PaymentStatus.PENDING, PaymentStatus.PAID])
    transaction_id = factory.Faker("uuid4")

    class Meta:
        model = Payment
