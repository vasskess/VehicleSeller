from django.db import models
from django.core.validators import MinValueValidator
from VehicleSeller.accounts.models import SellerUser
from VehicleSeller.core.vehicle_helpers.enum_helpers.engine_type import EngineTypes
from VehicleSeller.core.vehicle_helpers.enum_helpers.euro_category import EuroCategory
from VehicleSeller.core.vehicle_helpers.enum_helpers.year_of_manufactoring import Year


class Vehicle(models.Model):  # TODO think about custom validators if needed at some point !
    BRAND_MAX_LEN = 100

    VEHICLE_MODEL_MAX_LEN = 100

    TRANSMISSION_MAX_LEN = 50

    PRICE_MAX_DIGITS = 9
    PRICE_DECIMAL_PLACES = 2
    PRICE_MIN_VALUE = 0

    COLOR_MAX_LEN = 50

    brand = models.CharField(
        max_length=BRAND_MAX_LEN, null=False, blank=False, verbose_name="Brand"
    )
    vehicle_model = models.CharField(
        max_length=VEHICLE_MODEL_MAX_LEN, null=False, blank=False, verbose_name="Model"
    )
    transmission = models.CharField(
        max_length=TRANSMISSION_MAX_LEN,
        null=False,
        blank=False,
        verbose_name="Transmission",
    )
    engine_type = models.CharField(
        choices=EngineTypes.choices(),
        max_length=EngineTypes.max_length(),
        null=False,
        blank=False,
        verbose_name="Engine Type",
    )
    euro_standard = models.CharField(
        choices=EuroCategory.choices(),
        max_length=EuroCategory.max_length(),
        null=False,
        blank=False,
        verbose_name="Euro Standard",
    )
    manufacturing_year = models.CharField(
        choices=Year.choices(),
        max_length=Year.max_length(),
        null=False,
        blank=False,
        verbose_name="Manufacturing Year",
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
    color = models.CharField(
        max_length=COLOR_MAX_LEN, null=False, blank=False, verbose_name="Color"
    )
    is_used = models.BooleanField(default=False)
    seller = models.ForeignKey(SellerUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.vehicle_model}"
