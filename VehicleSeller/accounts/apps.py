from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "VehicleSeller.accounts"

    def ready(self):
        import VehicleSeller.accounts.signals
