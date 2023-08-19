from django.apps import AppConfig


class VehiclesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "VehicleSeller.vehicles"

    def ready(self):
        import VehicleSeller.vehicles.signals
