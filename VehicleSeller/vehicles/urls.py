from django.urls import path

from VehicleSeller.vehicles import views

app_name = "vehicles"

urlpatterns = [
    path("create/", views.CreateVehicleView.as_view(), name="create-vehicle"),
]
