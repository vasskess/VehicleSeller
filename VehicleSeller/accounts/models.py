from cloudinary.models import CloudinaryField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

from VehicleSeller.accounts.managers import SellerUserManager
from VehicleSeller.core.account_helpers.phone_number_validator import (
    validate_phone_number,
)


class SellerUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_ERROR = "User with that email already exist !"

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        verbose_name="Email",
        error_messages={"unique": USERNAME_ERROR},
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False, null=False, blank=False, verbose_name="Staff status"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = "email"
    objects = SellerUserManager()

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return self.email


class SellerProfile(models.Model):
    FIRST_NAME_MIN_LEN = 3
    FIRST_NAME_MAX_LEN = 100
    FIRST_NAME_MIN_LEN_MESSAGE = (
        f"First name must be at least {FIRST_NAME_MIN_LEN} characters long"
    )

    LAST_NAME_MIN_LEN = 3
    LAST_NAME_MAX_LEN = 100
    LAST_NAME_MIN_LEN_MESSAGE = (
        f"Last name must be at least {LAST_NAME_MIN_LEN} characters long"
    )

    LOCATION_MIN_LEN = 3
    LOCATION_MAX_LEN = 75
    LOCATION_MIN_LEN_MESSAGE = (
        f"Location must be at least {LOCATION_MIN_LEN} characters long"
    )

    PHONE_NUMBER_MAX_LEN = 10

    user = models.OneToOneField(
        SellerUser,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="User email",
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LEN, FIRST_NAME_MIN_LEN_MESSAGE),
        ),
        null=False,
        blank=False,
        verbose_name="First Name",
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(MinLengthValidator(LAST_NAME_MIN_LEN, LAST_NAME_MIN_LEN_MESSAGE),),
        null=False,
        blank=False,
        verbose_name="Last Name",
    )
    location = models.CharField(
        max_length=LOCATION_MAX_LEN,
        validators=(MinLengthValidator(LOCATION_MIN_LEN, LOCATION_MIN_LEN_MESSAGE),),
        null=False,
        blank=False,
        verbose_name="Location",
    )

    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LEN,
        validators=[validate_phone_number],
        null=False,
        blank=False,
        verbose_name="Phone Number",
    )
    slug = models.SlugField(
        unique=True,
        editable=False,
        verbose_name="slug",
    )

    class Meta:
        ordering = ["-user"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.email.split("@")[0] + "-" + str(self.user.id))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class ProfileImage(models.Model):
    profile_img = models.ForeignKey(
        SellerUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="profile_image",
    )
    profile_image = CloudinaryField(verbose_name="Profile Image", folder="Testing")
