import factory

from VehicleSeller.vehicles.models import (
    VehicleTransmission,
    VehicleEngine,
    VehicleEuroStandard,
    VehicleManufacturingYear,
    VehicleBrand,
    VehicleModel,
    VehicleColor,
    Vehicle,
)
from VehicleSeller.core.vehicle_helpers.enum_helpers.transmissions import Transmission
from VehicleSeller.core.vehicle_helpers.enum_helpers.engine_type import EngineTypes
from VehicleSeller.core.vehicle_helpers.enum_helpers.euro_category import EuroCategory
from VehicleSeller.core.vehicle_helpers.enum_helpers.year_of_manufactoring import Year
from tests.accounts.factories import UserFactory


class VehicleTransmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VehicleTransmission

    vehicle_transmission = factory.Iterator([choice.value for choice in Transmission])


class VehicleEnginesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VehicleEngine

    vehicle_engine = factory.Iterator([choice.value for choice in EngineTypes][1:])


class VehicleEuroStandardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VehicleEuroStandard

    vehicle_standard = factory.Iterator([choice.value for choice in EuroCategory][2:])


class VehicleManufacturingYearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VehicleManufacturingYear

    vehicle_manufacturing_year = factory.Iterator(
        [choice.value for choice in Year][78:]
    )


class VehicleBrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VehicleBrand

    name = "Honda"


class VehicleModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VehicleModel

    name = "Civic"


class VehicleColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VehicleColor

    name = "Red"


class VehicleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vehicle

    brand = factory.SubFactory(VehicleBrandFactory)
    model = factory.SubFactory(VehicleModelFactory)
    transmission = factory.SubFactory(VehicleTransmissionFactory)
    engine_type = factory.SubFactory(VehicleEnginesFactory)
    euro_standard = factory.SubFactory(VehicleEuroStandardFactory)
    manufacturing_year = factory.SubFactory(VehicleManufacturingYearFactory)
    price = "8500"
    mileage = "175600"
    color = factory.SubFactory(VehicleColorFactory)
    is_used = True
    seller = factory.SubFactory(UserFactory)
