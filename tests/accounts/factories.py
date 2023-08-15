import factory
from VehicleSeller.accounts.models import SellerUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SellerUser

    email = factory.Sequence(lambda num: f"test_{num + 1}_user@example.com")
