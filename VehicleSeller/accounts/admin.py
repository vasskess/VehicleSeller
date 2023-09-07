from django.contrib.auth import admin as auth_admin
from django.contrib import admin
from django.contrib.auth import get_user_model

from VehicleSeller.accounts.models import ProfileImage
from VehicleSeller.core.account_helpers.profile_model_helper import get_profile_model

User = get_user_model()
profile_model = get_profile_model()


class ProfileImageInline(admin.TabularInline):
    model = ProfileImage
    extra = 1


@admin.register(User)
class SellerUserAdmin(auth_admin.UserAdmin):
    list_display = ("email", "is_staff", "is_superuser")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
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
    inlines = [ProfileImageInline]
    ordering = ("email",)


admin.site.register(profile_model)
