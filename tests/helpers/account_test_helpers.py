from django.contrib.auth import get_user_model
from django.urls import reverse

test_user = get_user_model()
CREATE_USER_URL = reverse("account:create")
GENERATE_TOKEN_URL = reverse("account:token")


def create_user(**params):
    return test_user.objects.create_user(**params)
