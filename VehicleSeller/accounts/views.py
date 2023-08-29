from rest_framework import generics

from VehicleSeller.accounts.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
