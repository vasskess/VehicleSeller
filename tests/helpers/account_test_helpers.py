from django.contrib.auth import get_user_model
from django.urls import reverse

test_user = get_user_model()
CREATE_USER_URL = reverse("account:create")


def create_user(**params):
    return test_user.objects.create_user(**params)
