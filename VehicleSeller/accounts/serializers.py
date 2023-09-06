from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from django.core import exceptions
from rest_framework import serializers
from django.utils.translation import gettext as _

from VehicleSeller.core.account_helpers.profile_model_helper import get_profile_model

my_user = get_user_model()
my_profile = get_profile_model()


class UserSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField(source="profile.slug")

    class Meta:
        model = my_user
        fields = ["email", "password", "slug"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    @staticmethod
    def _validate_password(password):
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

    @staticmethod
    def _validate_email(email):
        queryset = my_user.objects.all().filter(email=email.lower())
        if queryset.exists():
            raise serializers.ValidationError("User with that email already exist !")
        return email

    def create(self, validated_data):
        password = validated_data.get("password")
        email = validated_data.get("email")
        self._validate_password(password)
        self._validate_email(email)

        return my_user.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        email = validated_data.pop("email", None)
        user = super().update(instance, validated_data)

        if password:
            self._validate_password(password)
            user.set_password(password)
            user.save()

        if email:
            self._validate_email(email)
            user.email = email
            user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_profile
        fields = ["first_name", "last_name", "location", "phone_number"]

    def update(self, instance, validated_data):
        for field_name, value in validated_data.items():
            setattr(instance, field_name, value)
        instance.save()

        return instance
        # =========================================================
        # first_name = validated_data.pop("first_name", None)
        # last_name = validated_data.pop("last_name", None)
        # location = validated_data.pop("location", None)
        # phone_number = validated_data.pop("phone_number", None)
        # profile = super().update(instance, validated_data)
        #
        # if first_name:
        #     profile.first_name = first_name
        # if last_name:
        #     profile.last_name = last_name
        # if location:
        #     profile.location = location
        # if phone_number:
        #     profile.phone_number = phone_number
        # profile.save()
        #
        # return profile
        # =========================================================
        # This ^^^ approach is more explicit and provides a clear and separate check for each field before updating it,
        # but i`ts ugly !


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
