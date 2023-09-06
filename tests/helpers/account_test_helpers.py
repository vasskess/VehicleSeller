from django.contrib.auth import get_user_model
from django.urls import reverse

test_user = get_user_model()
CREATE_USER_URL = reverse("account:create")
GENERATE_TOKEN_URL = reverse("account:token")
USER_DETAILS_URL = reverse("account:user-details")
PROFILE_DETAILS_URL = reverse("account:profile-details")


def create_user(**params):
    return test_user.objects.create_user(**params)
