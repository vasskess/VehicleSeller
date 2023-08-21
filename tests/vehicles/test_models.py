import pytest

pytestmark = pytest.mark.django_db


class TestVehicleBrandModel:
    def test_vehicle_brand_dunder_str_returns_proper_output(
        self, vehicle_brand_factory
    ):
        brand = vehicle_brand_factory()
        assert brand.__str__() == "Honda"


class TestVehicleModelModel:
    def test_vehicle_model_dunder_str_returns_proper_output(
        self, vehicle_model_factory
    ):
        brand = vehicle_model_factory()
        assert brand.__str__() == "Civic"


class TestVehicleTransmissionModel:
    def test_vehicle_transmission_dunder_str_returns_proper_output(
        self, vehicle_transmission_factory
    ):
        transmission = vehicle_transmission_factory()
        assert transmission.__str__() == "Manual"


class TestVehicleEngineModel:
    def test_vehicle_engine_dunder_str_returns_proper_output(
        self, vehicle_engines_factory
    ):
        engine = vehicle_engines_factory()
        assert engine.__str__() == "Petrol"


class TestVehicleEuroStandardModel:
    def test_vehicle_euro_standard_dunder_str_returns_proper_output(
        self, vehicle_euro_standard_factory
    ):
        standard = vehicle_euro_standard_factory()
        assert standard.__str__() == "EURO-3"


class TestVehicleManufacturingYearModel:
    def test_vehicle_manufacturing_year_dunder_str_returns_proper_output(
        self, vehicle_manufacturing_year_factory
    ):
        manufactured = vehicle_manufacturing_year_factory()
        assert manufactured.__str__() == "2008"


class TestVehicleColorModel:
    def test_vehicle_color_dunder_str_returns_proper_output(
        self, vehicle_color_factory
    ):
        brand = vehicle_color_factory()
        assert brand.__str__() == "Red"


class TestVehicleModel:
    def test_vehicle_price_returns_proper_value(self, vehicle_factory):
        vehicle = vehicle_factory()
        assert vehicle.price == "8500"

    def test_vehicle_mileage_returns_proper_value(self, vehicle_factory):
        vehicle = vehicle_factory()
        assert vehicle.mileage == "175600"

    def test_vehicle_is_used_returns_proper_boolean(self, vehicle_factory):
        vehicle = vehicle_factory()
        assert vehicle.is_used

    def test_vehicle_seller_returns_proper_value(self, user_factory, vehicle_factory):
        user = user_factory(email="secret_email@mhmmm")
        vehicle = vehicle_factory(seller=user)

        assert vehicle.seller.email == "secret_email@mhmmm"

    def test_vehicle_str_returns_proper_output(self, vehicle_factory):
        brand = vehicle_factory()
        assert brand.__str__() == f'{"Honda"} - {"Civic"}'


class TestBaseAttributesModel:
    def test_name_property_returns_proper_class_name_as_name_value(
        self, vehicle_transmission_factory
    ):
        transmission = vehicle_transmission_factory()

        assert transmission.name == "VehicleTransmission"
