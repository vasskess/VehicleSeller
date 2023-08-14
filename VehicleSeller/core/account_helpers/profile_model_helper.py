from django.contrib.auth import get_user_model

User = get_user_model()


def get_profile_model():
    return User._meta.get_field("profile").remote_field.model
