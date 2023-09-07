from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.helpers.account_test_helpers import (
    create_user,
    PROFILE_DETAILS_URL,
)


class PrivateProfileApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="secret_email@mhmm.com",
            password="passwordmhmm",
        )
        self.user.profile.first_name = "Vasil"
        self.user.profile.last_name = "Rangelov"
        self.user.profile.location = "Sofia"
        self.user.profile.phone_number = "0888445566"
        self.user.profile.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def _assert_profile_update_fails(self, status_code, field, expected_error_message):

        self.assertEqual(self.user.profile.first_name, "Vasil")
        self.assertEqual(self.user.profile.last_name, "Rangelov")
        self.assertEqual(self.user.profile.location, "Sofia")
        self.assertEqual(self.user.profile.phone_number, "0888445566")
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(field, expected_error_message)

    def test_get_method_for_profile_details_returns_proper_profile_proper_profile_details_and_proper_status_code(
        self,
    ):

        result = self.client.get(PROFILE_DETAILS_URL)

        self.assertEqual(self.user.pk, self.user.profile.pk)
        self.assertEqual(
            result.data,
            {
                "first_name": self.user.profile.first_name,
                "last_name": self.user.profile.last_name,
                "location": self.user.profile.location,
                "phone_number": self.user.profile.phone_number,
            },
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_put_method_with_valid_profile_field_values_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "Iliev",
            "location": "Ruse",
            "phone_number": "0888112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(
            self.user.profile.first_name, updated_profile_data["first_name"]
        )
        self.assertEqual(self.user.profile.last_name, updated_profile_data["last_name"])
        self.assertEqual(self.user.profile.location, updated_profile_data["location"])
        self.assertEqual(
            self.user.profile.phone_number, updated_profile_data["phone_number"]
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_put_method_with_invalid_profile_first_name_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Mi",
            "last_name": "Iliev",
            "location": "Ruse",
            "phone_number": "0888112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = f"Ensure this field has at least {self.user.profile.FIRST_NAME_MIN_LEN} characters."

        self._assert_profile_update_fails(
            result.status_code, result.data["first_name"][0], expected_error_message
        )

    def test_put_method_with_blank_profile_first_name_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "",
            "last_name": "Iliev",
            "location": "Ruse",
            "phone_number": "0888112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = f"This field may not be blank."

        self._assert_profile_update_fails(
            result.status_code, result.data["first_name"][0], expected_error_message
        )

    def test_put_method_with_invalid_profile_last_name_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "Il",
            "location": "Ruse",
            "phone_number": "0888112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = f"Ensure this field has at least {self.user.profile.LAST_NAME_MIN_LEN} characters."

        self._assert_profile_update_fails(
            result.status_code, result.data["last_name"][0], expected_error_message
        )

    def test_put_method_with_blank_last_name_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "",
            "location": "Ruse",
            "phone_number": "0888112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = f"This field may not be blank."

        self._assert_profile_update_fails(
            result.status_code, result.data["last_name"][0], expected_error_message
        )

    def test_put_method_with_invalid_profile_location_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "Iliev",
            "location": "Ru",
            "phone_number": "0888112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = f"Ensure this field has at least {self.user.profile.LOCATION_MIN_LEN} characters."

        self._assert_profile_update_fails(
            result.status_code, result.data["location"][0], expected_error_message
        )

    def test_put_method_with_blank_profile_location_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "Iliev",
            "location": "",
            "phone_number": "0888112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = "This field may not be blank."

        self._assert_profile_update_fails(
            result.status_code, result.data["location"][0], expected_error_message
        )

    def test_put_method_with_phone_number_contains_letter_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "Iliev",
            "location": "Ruse",
            "phone_number": "08a8112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = f"Phone number should contain only digits."

        self._assert_profile_update_fails(
            result.status_code, result.data["phone_number"][0], expected_error_message
        )

    def test_put_method_with_phone_number_with_less_digits_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "Iliev",
            "location": "Ruse",
            "phone_number": "088112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = f"Phone number should have exactly 10 digits."

        self._assert_profile_update_fails(
            result.status_code, result.data["phone_number"][0], expected_error_message
        )

    def test_put_method_with_phone_number_with_more_digits_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "Iliev",
            "location": "Ruse",
            "phone_number": "088811223344",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = f"Phone number should have exactly 10 digits."

        self._assert_profile_update_fails(
            result.status_code, result.data["phone_number"][0], expected_error_message
        )

    def test_put_method_with_phone_number_not_starts_with_08_doesnt_update_profile_fields_and_return_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "Iliev",
            "location": "Ruse",
            "phone_number": "0188112233",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = f"Please provide a valid phone number."

        self._assert_profile_update_fails(
            result.status_code, result.data["phone_number"][0], expected_error_message
        )

    def test_put_method_with_blank_phone_number_doesnt_update_profile_fields_and_returns_proper_status_code(
        self,
    ):
        updated_profile_data = {
            "first_name": "Milen",
            "last_name": "Iliev",
            "location": "Ruse",
            "phone_number": "",
        }

        result = self.client.put(PROFILE_DETAILS_URL, updated_profile_data)

        expected_error_message = "This field may not be blank."

        self._assert_profile_update_fails(
            result.status_code, result.data["phone_number"][0], expected_error_message
        )

    def test_patch_method_with_valid_first_name_returns_proper_first_name_and_proper_status_code(
        self,
    ):

        updated_profile_data = {"first_name": "Milen"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(
            self.user.profile.first_name, updated_profile_data["first_name"]
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_first_and_last_name_returns_proper_first_and_last_name_and_proper_status_code(
        self,
    ):
        updated_profile_data = {"first_name": "Milen", "last_name": "Iliev"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(
            self.user.profile.first_name, updated_profile_data["first_name"]
        )
        self.assertEqual(self.user.profile.last_name, updated_profile_data["last_name"])
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_mtd_with_valid_first_name_and_location_returns_proper_first_name_and_location_and_proper_status_code(
        self,
    ):
        updated_profile_data = {"first_name": "Milen", "location": "Ruse"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(
            self.user.profile.first_name, updated_profile_data["first_name"]
        )
        self.assertEqual(self.user.profile.location, updated_profile_data["location"])
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_first_name_and_number_returns_proper_first_name_and_number_and_proper_status_code(
        self,
    ):
        updated_profile_data = {"first_name": "Milen", "phone_number": "0888112233"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(
            self.user.profile.first_name, updated_profile_data["first_name"]
        )
        self.assertEqual(
            self.user.profile.phone_number, updated_profile_data["phone_number"]
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_last_name_returns_proper_last_name_and_proper_status_code(
        self,
    ):
        updated_profile_data = {"last_name": "Iliev"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(self.user.profile.last_name, updated_profile_data["last_name"])
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_last_name_and_location_return_proper_last_name_and_location_and_proper_status_code(
        self,
    ):
        updated_profile_data = {"last_name": "Iliev", "location": "Ruse"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(self.user.profile.last_name, updated_profile_data["last_name"])
        self.assertEqual(self.user.profile.location, updated_profile_data["location"])
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_last_name_and_number_returns_proper_last_name_and_number_and_proper_status_code(
        self,
    ):
        updated_profile_data = {"last_name": "Iliev", "phone_number": "0888112233"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(self.user.profile.last_name, updated_profile_data["last_name"])
        self.assertEqual(
            self.user.profile.phone_number, updated_profile_data["phone_number"]
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_location_returns_proper_location_and_proper_status_code(
        self,
    ):
        updated_profile_data = {"location": "Ruse"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(self.user.profile.location, updated_profile_data["location"])
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_location_and_number_returns_proper_location_and_number_and_proper_status_code(
        self,
    ):
        updated_profile_data = {"location": "Ruse", "phone_number": "0888112233"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(self.user.profile.location, updated_profile_data["location"])
        self.assertEqual(
            self.user.profile.phone_number, updated_profile_data["phone_number"]
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_phone_number_returns_proper_phone_number_and_proper_status_code(
        self,
    ):
        updated_profile_data = {"phone_number": "0888112233"}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(
            self.user.profile.phone_number, updated_profile_data["phone_number"]
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_empty_profile_fields_doesnt_change_profile_fields_and_returns_proper_status_code(
        self,
    ):

        updated_profile_data = {}

        result = self.client.patch(PROFILE_DETAILS_URL, updated_profile_data)

        self.assertEqual(result.data["first_name"], self.user.profile.first_name)
        self.assertEqual(result.data["last_name"], self.user.profile.last_name)
        self.assertEqual(result.data["location"], self.user.profile.location)
        self.assertEqual(result.data["phone_number"], self.user.profile.phone_number)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_post_method_on_profile_details_endpoint_is_not_allowed(self):
        result = self.client.post(PROFILE_DETAILS_URL, {})

        self.assertEqual(result.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
