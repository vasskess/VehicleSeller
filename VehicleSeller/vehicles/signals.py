from django.db.models.signals import post_delete
from django.dispatch import receiver

from VehicleSeller.core.image_deletion import delete_image
from VehicleSeller.vehicles.models import VehicleImage


@receiver(post_delete, sender=VehicleImage)
def delete_vehicle_image(sender, instance, **kwargs):
    image_to_delete = instance.vehicle_image
    delete_image(image_to_delete)


# TODO Think of other signals like on_update, etc.
