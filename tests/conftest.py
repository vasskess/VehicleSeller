from pytest_factoryboy import register
from tests.accounts.factories import UserFactory
from tests.vehicles.factories import (
    VehicleTransmissionFactory,
    VehicleEnginesFactory,
    VehicleEuroStandardFactory,
    VehicleManufacturingYearFactory,
    VehicleBrandFactory,
    VehicleModelFactory,
    VehicleColorFactory,
    VehicleFactory,
)

register(UserFactory)
register(VehicleTransmissionFactory)
register(VehicleEnginesFactory)
register(VehicleEuroStandardFactory)
register(VehicleManufacturingYearFactory)
register(VehicleBrandFactory)
register(VehicleModelFactory)
register(VehicleColorFactory)
register(VehicleFactory)
