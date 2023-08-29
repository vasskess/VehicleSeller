from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core import exceptions
from rest_framework import serializers

my_user = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_user
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.get("password")

        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return my_user.objects.create_user(
            **validated_data
        )
