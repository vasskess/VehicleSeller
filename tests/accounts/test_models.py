import pytest

pytestmark = pytest.mark.django_db


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
