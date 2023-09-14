from rest_framework import generics, authentication, permissions

from VehicleSeller.vehicles.serializers import VehicleSerializer


class CreateVehicleView(generics.CreateAPIView):
    serializer_class = VehicleSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
