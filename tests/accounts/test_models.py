import pytest
from django.core.exceptions import ValidationError

from VehicleSeller.core.account_helpers.phone_number_validator import (
    validate_phone_number,
)

pytestmark = pytest.mark.django_db


# TODO Might need refactoring plus some more test(this one for sure!)


class TestSellerUserModel:
    def test_seller_user_dunder_str_returns_proper_email_output(self, user_factory):
        user_1 = user_factory.create()
        user_2 = user_factory.create()

        assert user_1.__str__() == "test_1_user@example.com"
        assert user_2.__str__() == "test_2_user@example.com"

    def test_seller_profile_dunder_str_returns_proper_slug_output(self, user_factory):
        user = user_factory.create(email="secret_email@mhmmm")
        profile = user.profile

        assert profile.__str__() == "secret_email"

    @pytest.mark.parametrize(
        "invalid_phone_number, expected_error",
        [
            ("08mhmmm", "Phone number should contain only digits."),
            ("083456789", "Phone number should have exactly 10 digits."),
            ("1234567890", "Please provide a valid phone number."),
        ],
    )
    def test_seller_profile_phone_number_validator_returns_proper_error_messages(
        self, user_factory, invalid_phone_number, expected_error
    ):
        user = user_factory.create()
        profile = user.profile

        profile.phone_number = invalid_phone_number

        with pytest.raises(ValidationError) as error_msg:
            validate_phone_number(profile.phone_number)

        actual_error = str(*error_msg.value)
        assert actual_error == expected_error

    def test_seller_profile_phone_number_validator_returns_valid_number(
        self, user_factory
    ):
        user = user_factory.create()
        profile = user.profile

        profile.phone_number = "0834567890"
        profile.save()

        assert profile.phone_number == "0834567890"
