from django.db.models.signals import post_delete
from django.dispatch import receiver

from VehicleSeller.core.vehicle_helpers.image_deletion import delete_image
from VehicleSeller.vehicles.models import VehicleImage


@receiver(post_delete, sender=VehicleImage)
def delete_image_on_delete(sender, instance, **kwargs):
    delete_image(instance)


# TODO Think of other signals like on_update, etc.
