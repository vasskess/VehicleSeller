from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken

from VehicleSeller.accounts.serializers import UserSerializer, AuthTokenSerializer

my_user = get_user_model()


# TODO maybe use ViewSets here instead ?
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class GenerateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
