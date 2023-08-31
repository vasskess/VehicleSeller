from django.urls import path

from VehicleSeller.accounts import views

app_name = "account"
# TODO --> routers if ViewSets in views !
urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.GenerateTokenView.as_view(), name="token"),
    path("details/", views.ManageUserView.as_view(), name="details"),
]
