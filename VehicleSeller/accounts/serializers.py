from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from django.core import exceptions
from rest_framework import serializers
from django.utils.translation import gettext as _

from VehicleSeller.core.account_helpers.profile_model_helper import get_profile_model

my_user = get_user_model()
my_profile = get_profile_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_user
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    # TODO move this staticmethod as function if i`ll use it anywhere else, but most likely not !
    @staticmethod
    def _validate_password(password):
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

    def create(self, validated_data):
        password = validated_data.get("password")
        self._validate_password(password)

        return my_user.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            self._validate_password(password)
            user.set_password(password)
            user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_profile
        fields = ["first_name", "last_name", "location", "phone_number"]


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            message = _("Please, provide valid credentials.")
            raise serializers.ValidationError(message, code="authorization")

        attrs["user"] = user
        return attrs
