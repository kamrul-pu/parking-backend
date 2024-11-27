import factory
from django.contrib.auth import get_user_model
from faker import Faker

from core.choices import UserKind

# Get the user model dynamically (this helps if you change your model in the future)
User = get_user_model()

fake = Faker()


# Create a factory for User
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Assigning default data to each field
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    gender = factory.Iterator(
        ["MALE", "FEMALE"]
    )  # You can adjust this to your gender choices
    image = None  # Leave image as None if you don't want to upload images for testing
    is_active = True
    is_staff = False
    kind = UserKind.CUSTOMER  # Default user kind

    # You can also handle custom fields if necessary
    @factory.lazy_attribute
    def slug(self):
        return f"{self.first_name}-{self.last_name}".lower()

    # # You can create a method to set custom attributes like `kind` if required
    # @factory.post_generation
    # def set_kind(self, create, extracted, **kwargs):
    #     if extracted:
    #         self.kind = extracted
    #     else:
    #         self.kind = "UNDEFINED"

    # Example of how you can override the `create_user` functionality:
    @factory.lazy_attribute
    def password(self):
        return fake.password()

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        if extracted:
            self.set_password(extracted)  # Use a custom password if needed
        else:
            self.set_password(self.password)
