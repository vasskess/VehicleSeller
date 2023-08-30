from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken

from VehicleSeller.accounts.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
