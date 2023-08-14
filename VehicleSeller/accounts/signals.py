from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from VehicleSeller.core.account_helpers.profile_model_helper import get_profile_model

User = get_user_model()
profile_model = get_profile_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile_model.objects.create(user=instance)
