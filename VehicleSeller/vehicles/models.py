from django.db import models
from django.core.validators import MinValueValidator
from VehicleSeller.accounts.models import SellerUser
from VehicleSeller.core.vehicle_helpers.enum_helpers.transmissions import Transmission
from VehicleSeller.core.vehicle_helpers.enum_helpers.engine_type import EngineTypes
from VehicleSeller.core.vehicle_helpers.enum_helpers.euro_category import EuroCategory
from VehicleSeller.core.vehicle_helpers.enum_helpers.year_of_manufactoring import Year


#  TODO think about custom validators if needed at some point !
class BaseNameModel(models.Model):
    NAME_MAX_LEN = 100

    name = models.CharField(
        max_length=NAME_MAX_LEN, null=False, blank=False, verbose_name="Name"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class BaseAttributesModel(models.Model):
    class Meta:
        abstract = True

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return str(self.name)


class VehicleBrand(BaseNameModel):
    class Meta:
        verbose_name = "Vehicle Brand"


class VehicleModel(BaseNameModel):
    class Meta:
        verbose_name = "Vehicle Model"


class VehicleTransmission(BaseAttributesModel):
    vehicle_transmission = models.CharField(
        choices=Transmission.choices(),
        max_length=Transmission.max_length(),
        null=False,
        blank=False,
        verbose_name="Transmission",
    )

    def __str__(self):
        return self.vehicle_transmission


class VehicleEngine(BaseAttributesModel):
    vehicle_engine = models.CharField(
        choices=EngineTypes.choices(),
        max_length=EngineTypes.max_length(),
        null=False,
        blank=False,
        verbose_name="Engine Type",
    )

    def __str__(self):
        return self.vehicle_engine


class VehicleEuroStandard(BaseAttributesModel):
    vehicle_standard = models.CharField(
        choices=EuroCategory.choices(),
        max_length=EuroCategory.max_length(),
        null=False,
        blank=False,
        verbose_name="Euro Standard",
    )

    def __str__(self):
        return self.vehicle_standard


class VehicleManufacturingYear(BaseAttributesModel):
    vehicle_manufacturing_year = models.CharField(
        choices=Year.choices(),
        max_length=Year.max_length(),
        null=False,
        blank=False,
        verbose_name="Manufacturing Year",
    )

    def __str__(self):
        return self.vehicle_manufacturing_year


class VehicleColor(BaseAttributesModel):
    NAME_MAX_LEN = 50

    name = models.CharField(max_length=NAME_MAX_LEN)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    PRICE_MAX_DIGITS = 9
    PRICE_DECIMAL_PLACES = 2
    PRICE_MIN_VALUE = 0

    brand = models.ForeignKey(VehicleBrand, on_delete=models.PROTECT)
    model = models.ForeignKey(VehicleModel, on_delete=models.PROTECT)
    transmission = models.ForeignKey(VehicleTransmission, on_delete=models.PROTECT)
    engine_type = models.ForeignKey(VehicleEngine, on_delete=models.PROTECT)
    euro_standard = models.ForeignKey(VehicleEuroStandard, on_delete=models.PROTECT)
    manufacturing_year = models.ForeignKey(
        VehicleManufacturingYear, on_delete=models.PROTECT
    )
    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        validators=[MinValueValidator(PRICE_MIN_VALUE)],
        verbose_name="Price",
    )
    mileage = models.PositiveIntegerField(
        null=False, blank=False, verbose_name="Mileage"
    )
    color = models.ForeignKey(
        VehicleColor, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_used = models.BooleanField(default=False)

    seller = models.ForeignKey(SellerUser, on_delete=models.CASCADE)

    @property
    def manufactured(self):
        return self.manufacturing_year.vehicle_manufacturing_year.replace("YEAR_", "")

    def __str__(self):
        return f"{self.brand} - {self.model}"
