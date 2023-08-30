from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from django.core import exceptions
from rest_framework import serializers
from django.utils.translation import gettext as _

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

        return my_user.objects.create_user(**validated_data)


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
