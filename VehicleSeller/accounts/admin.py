from django.contrib.auth import admin as auth_admin
from django.contrib import admin
from django.contrib.auth import get_user_model

from VehicleSeller.core.account_helpers.profile_model_helper import get_profile_model

User = get_user_model()
profile_model = get_profile_model()


@admin.register(User)
class SellerUserAdmin(auth_admin.UserAdmin):

    model = User
    list_display = ("email", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email",)}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "groups", "is_superuser")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    ordering = ("email",)


admin.site.register(profile_model)
