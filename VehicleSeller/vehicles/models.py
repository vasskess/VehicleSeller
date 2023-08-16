from django.db import models
from django.core.validators import MinValueValidator
from VehicleSeller.accounts.models import SellerUser


class Vehicle(models.Model):  # TODO add more fields with choices !
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
    is_used = models.BooleanField(default=False)
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
    seller = models.ForeignKey(SellerUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.vehicle_model}"
