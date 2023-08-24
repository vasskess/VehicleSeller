from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from VehicleSeller.accounts.models import ProfileImage
from VehicleSeller.core.account_helpers.profile_model_helper import get_profile_model
from VehicleSeller.core.image_deletion import delete_image

User = get_user_model()
profile_model = get_profile_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile_model.objects.create(user=instance)


@receiver(post_delete, sender=ProfileImage)
def delete_profile_image(sender, instance, **kwargs):
    image_to_delete = instance.profile_image
    delete_image(image_to_delete)


# TODO ^^^ drf_spectacular views to see it in action, plus look for better solution if it has one !
# TODO maybe also add error handling(try/except) just in case !
