from django.contrib.auth import get_user_model

User = get_user_model()


def get_profile_model():
    return User.profile.related.related_model
