from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.helpers.account_test_helpers import (
    create_user,
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
