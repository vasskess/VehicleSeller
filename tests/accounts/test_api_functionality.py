from django.core.validators import EmailValidator
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status, serializers

from VehicleSeller.accounts.serializers import AuthTokenSerializer
from tests.helpers.account_test_helpers import (
    test_user,
    create_user,
    CREATE_USER_URL,
    GENERATE_TOKEN_URL,
    USER_DETAILS_URL,
)


# TODO might need to separate Public and Private classes since tests will be a lot ?!
class PublicAccountApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_account_with_valid_credentials_creates_account_and_store_password_properly_in_db(
        self,
    ):
        seller_user = {
            "email": "secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        result = self.client.post(CREATE_USER_URL, seller_user)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        password_to_check = test_user.objects.get(email=seller_user["email"])

        self.assertTrue(password_to_check.check_password(seller_user["password"]))
        self.assertNotIn("password", result.data)
        """ Check that password is not presented in response ! """

    def test_create_account_with_existing_email_returning_proper_error_message_and_status_code(
        self,
    ):
        seller_user = {
            "email": "secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        create_user(**seller_user)

        result = self.client.post(CREATE_USER_URL, seller_user)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.data["email"][0], test_user.USERNAME_ERROR)

    def test_create_account_with_invalid_email_returning_proper_error_message_status_code_and_user_is_not_created(
        self,
    ):
        seller_user = {
            "email": "secret_email@",
            "password": "11secretPassword22",
        }

        result = self.client.post(CREATE_USER_URL, seller_user)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.data["email"][0], EmailValidator.message)

        user_exists = test_user.objects.filter(email=seller_user["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_account_with_short_password_returning_proper_error_message_status_code_and_user_is_not_created(
        self,
    ):
        seller_user = {
            "email": "secret_email@mhmm.com",
            "password": "1234567",
        }

        result = self.client.post(CREATE_USER_URL, seller_user)

        expected_error_message = (
            "This password is too short. It must contain at least 8 characters."
        )

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.data["password"][0], expected_error_message)

        user_exists = test_user.objects.filter(email=seller_user["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_account_with_common_password_returning_proper_error_message_status_code_and_user_is_not_created(
        self,
    ):
        seller_user = {
            "email": "secret_email@mhmm.com",
            "password": "qwerty123",
        }

        result = self.client.post(CREATE_USER_URL, seller_user)
        expected_error_message = "This password is too common."

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.data["password"][0], expected_error_message)

        user_exists = test_user.objects.filter(email=seller_user["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_account_with_numeric_password_returning_proper_error_message_status_code_and_user_is_not_created(
        self,
    ):
        seller_user = {
            "email": "secret_email@mhmm.com",
            "password": "6589012345",
        }

        result = self.client.post(CREATE_USER_URL, seller_user)

        expected_error_message = "This password is entirely numeric."

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.data["password"][0], expected_error_message)

        user_exists = test_user.objects.filter(email=seller_user["email"]).exists()
        self.assertFalse(user_exists)

    def test_generate_token_for_user_with_valid_credentials_returns_token_and_proper_status_code(
        self,
    ):
        user_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        create_user(**user_credentials)
        seller_user = {
            "email": user_credentials["email"],
            "password": user_credentials["password"],
        }

        result = self.client.post(GENERATE_TOKEN_URL, seller_user)

        self.assertIn("token", result.data)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

    def test_generate_token_for_user_with_invalid_email_doesnt_returns_token__returns_proper_status_code(
        self,
    ):
        user_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        create_user(**user_credentials)
        seller_user = {
            "email": "not_secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        result = self.client.post(GENERATE_TOKEN_URL, seller_user)

        self.assertNotIn("token", result.data)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_token_for_user_with_invalid_email_raises_proper_error_and_returns_proper_message(
        self,
    ):
        user_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        create_user(**user_credentials)
        seller_user = {
            "email": "not_secret_email@mhmm.com",
            "password": "11secretPassword22",
        }
        expected_error = "Please, provide valid credentials."

        with self.assertRaises(serializers.ValidationError) as error:
            AuthTokenSerializer().validate(seller_user)

        exception = error.exception
        self.assertEqual(str(exception.detail[0]), expected_error)

    def test_generate_token_for_user_with_invalid_password_doesnt_returns_token_and_returns_proper_status_code(
        self,
    ):
        user_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        create_user(**user_credentials)
        seller_user = {
            "email": "secret_email@mhmm.com",
            "password": "not_secretPassword123",
        }

        result = self.client.post(GENERATE_TOKEN_URL, seller_user)

        self.assertNotIn("token", result.data)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_token_for_user_with_invalid_password_raises_proper_error_and_returns_proper_message(
        self,
    ):
        user_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        create_user(**user_credentials)
        seller_user = {
            "email": "secret_email@mhmm.com",
            "password": "not_secretPassword123",
        }

        expected_error = "Please, provide valid credentials."

        with self.assertRaises(serializers.ValidationError) as error:
            AuthTokenSerializer().validate(seller_user)

        exception = error.exception
        self.assertEqual(str(exception.detail[0]), expected_error)

    def test_generate_token_for_user_with_blank_password_doesnt_returns_token_and_returns_proper_status_code(
        self,
    ):
        user_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        create_user(**user_credentials)
        seller_user = {
            "email": "secret_email@mhmm.com",
            "password": "",
        }

        result = self.client.post(GENERATE_TOKEN_URL, seller_user)

        self.assertNotIn("token", result.data)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_token_for_user_with_blank_password_raises_proper_error_and_returns_proper_message(
        self,
    ):
        user_credentials = {
            "email": "secret_email@mhmm.com",
            "password": "11secretPassword22",
        }

        create_user(**user_credentials)
        seller_user = {
            "email": "secret_email@mhmm.com",
            "password": "",
        }

        expected_error = "Please, provide valid credentials."

        with self.assertRaises(serializers.ValidationError) as error:
            AuthTokenSerializer().validate(seller_user)

        exception = error.exception
        self.assertEqual(str(exception.detail[0]), expected_error)


class PrivateAccountApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="secret_email@mhmm.com",
            password="passwordmhmm",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_method_for_user_details_endpoint_returns_proper_user_and_proper_status_code(
        self,
    ):
        result = self.client.get(USER_DETAILS_URL)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(
            result.data,
            {
                "email": self.user.email,
            },
        )

    def test_put_method_with_valid_email_and_password_update_user_email_and_password_and_returns_proper_status_code(
        self,
    ):
        updated_credentials = {
            "email": "new_secret_email@mhmm.com",
            "password": "newpasswordmhmm",
        }

        result = self.client.patch(USER_DETAILS_URL, updated_credentials)

        self.user.refresh_from_db()

        self.assertEqual(self.user.email, updated_credentials["email"])
        self.assertTrue(self.user.check_password(updated_credentials["password"]))
        self.assertEqual(result.status_code, status.HTTP_200_OK)
