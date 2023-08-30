from django.urls import path

from VehicleSeller.accounts import views

app_name = "account"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.GenerateTokenView.as_view(), name="token"),
]
