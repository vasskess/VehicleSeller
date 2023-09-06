from django.core.validators import EmailValidator
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.helpers.account_test_helpers import (
    create_user,
    test_user,
    USER_DETAILS_URL,
)


class PrivateAccountApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="secret_email@mhmm.com",
            password="passwordmhmm",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_creating_user_also_creates_profile_with_empty_profile_fields_and_proper_slug(
        self,
    ):
        profile = self.user.profile

        self.assertEqual(self.user.pk, self.user.profile.pk)
        self.assertEqual(profile.first_name, "")
        self.assertEqual(profile.last_name, "")
        self.assertEqual(profile.location, "")
        self.assertEqual(profile.phone_number, "")
        self.assertEqual(
            f"{self.user.email.split('@')[0]}-{self.user.pk}", profile.slug
        )

    def test_get_method_for_user_details_endpoint_returns_proper_user_proper_slug_and_proper_status_code(
        self,
    ):
        result = self.client.get(USER_DETAILS_URL)

        self.assertEqual(
            result.data,
            {
                "email": self.user.email,
                "slug": self.user.profile.slug,
            },
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_put_method_with_valid_user_credentials_update_user_credentials_and_returns_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "new_secret_email@mhmm.com",
            "password": "newpasswordmhmm",
        }

        result = self.client.put(USER_DETAILS_URL, updated_credentials)

        self.assertEqual(self.user.email, updated_credentials["email"])
        self.assertTrue(self.user.check_password(updated_credentials["password"]))
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_put_method_with_existing_email_returns_proper_error_message_and_proper_status_code(
        self,
    ):
        update_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "passwordmhmm",
        }

        result = self.client.put(USER_DETAILS_URL, update_credentials)

        self.assertEqual(result.data[0], test_user.USERNAME_ERROR)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_method_without_email_field_returns_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "password": "newpasswordmhmm",
        }

        result = self.client.put(USER_DETAILS_URL, updated_credentials)

        expected_error = "This field is required."

        self.assertEqual(result.data["email"][0], expected_error)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_method_without_password_field_returns_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "new_secret_email@mhmm.com",
        }

        result = self.client.put(USER_DETAILS_URL, updated_credentials)

        expected_error = "This field is required."

        self.assertEqual(result.data["password"][0], expected_error)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_method_with_empty_credential_fields_returns_proper_error_messages_and_proper_status_code(
        self,
    ):
        updated_credentials = {}

        result = self.client.put(USER_DETAILS_URL, updated_credentials)

        expected_error = "This field is required."

        self.assertEqual(result.data["email"][0], expected_error)
        self.assertEqual(result.data["password"][0], expected_error)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_method_with_invalid_email_returns_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "new_secret_email@",
            "password": "newpasswordmhmm",
        }

        result = self.client.put(USER_DETAILS_URL, updated_credentials)

        self.assertEqual(result.data["email"][0], EmailValidator.message)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_method_with_short_password_returning_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "1234567",
        }

        result = self.client.put(USER_DETAILS_URL, updated_credentials)

        expected_error_message = (
            "This password is too short. It must contain at least 8 characters."
        )

        self.assertEqual(result.data["password"][0], expected_error_message)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_method_with_common_password_returning_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "qwerty123",
        }

        result = self.client.put(USER_DETAILS_URL, updated_credentials)
        expected_error_message = "This password is too common."

        self.assertEqual(result.data["password"][0], expected_error_message)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_method_with_entirely_numeric_password_returning_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "6589012345",
        }

        result = self.client.put(USER_DETAILS_URL, updated_credentials)

        expected_error_message = "This password is entirely numeric."

        self.assertEqual(result.data["password"][0], expected_error_message)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_method_with_valid_user_credentials_update_user_credentials_and_returns_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "new_secret_email@mhmm.com",
            "password": "newpasswordmhmm",
        }

        result = self.client.patch(USER_DETAILS_URL, updated_credentials)

        self.assertEqual(self.user.email, updated_credentials["email"])
        self.assertTrue(self.user.check_password(updated_credentials["password"]))
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_email_change_email_successfully_and_returns_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "new_secret_email@mhmm.com",
        }

        result = self.client.patch(USER_DETAILS_URL, updated_credentials)

        self.assertEqual(self.user.email, updated_credentials["email"])
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_valid_password_change_password_successfully_and_returns_proper_status_code(
        self,
    ):
        updated_credentials = {
            "password": "newpasswordmhmm",
        }

        result = self.client.patch(USER_DETAILS_URL, updated_credentials)

        self.assertTrue(self.user.check_password(updated_credentials["password"]))
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_patch_method_with_invalid_email_returns_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "new_secret_email@",
        }

        result = self.client.patch(USER_DETAILS_URL, updated_credentials)

        self.assertEqual(result.data["email"][0], EmailValidator.message)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_method_with_existing_email_returns_proper_error_message_and_proper_status_code(
        self,
    ):
        update_credentials = {"email": "secret_email@mhmm.com"}

        result = self.client.patch(USER_DETAILS_URL, update_credentials)

        self.assertEqual(result.data[0], test_user.USERNAME_ERROR)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_method_with_short_password_returning_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "password": "1234567",
        }

        result = self.client.patch(USER_DETAILS_URL, updated_credentials)

        expected_error_message = (
            "This password is too short. It must contain at least 8 characters."
        )

        self.assertEqual(result.data["password"][0], expected_error_message)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_method_with_common_password_returning_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "password": "qwerty123",
        }

        result = self.client.patch(USER_DETAILS_URL, updated_credentials)
        expected_error_message = "This password is too common."

        self.assertEqual(result.data["password"][0], expected_error_message)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_method_with_entirely_numeric_password_returning_proper_error_message_and_proper_status_code(
        self,
    ):
        updated_credentials = {
            "password": "6589012345",
        }

        result = self.client.patch(USER_DETAILS_URL, updated_credentials)

        expected_error_message = "This password is entirely numeric."

        self.assertEqual(result.data["password"][0], expected_error_message)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_method_with_empty_credential_fields_doesnt_change_credentials_and_returns_proper_status_code(
        self,
    ):
        initial_password = self.user.password

        updated_credentials = {}

        result = self.client.patch(USER_DETAILS_URL, updated_credentials)

        updated_user = test_user.objects.get(id=self.user.id)

        self.assertEqual(result.data["email"], self.user.email)
        self.assertEqual(updated_user.password, initial_password)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_post_method_on_user_details_endpoint_is_not_allowed(self):
        result = self.client.post(USER_DETAILS_URL, {})

        self.assertEqual(result.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
