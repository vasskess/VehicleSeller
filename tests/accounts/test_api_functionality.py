from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from tests.helpers.account_test_helpers import test_user, create_user, CREATE_USER_URL


class PublicAccountApiTests(TestCase):
    def setUP(self):
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
        expected_error_message = "Enter a valid email address."

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.data["email"][0], expected_error_message)
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
