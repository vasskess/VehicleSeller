from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError("Phone number should contain only digits.")
    if not len(value) == 10:
        raise ValidationError("Phone number should have exactly 10 digits.")
    if not value[0:2] == "08":
        raise ValidationError("Please provide a valid phone number.")
