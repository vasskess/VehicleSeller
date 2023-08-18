from django.contrib import admin

from VehicleSeller.core.vehicle_helpers.mixins.admin_form_mixin import FormHelperMixin
from VehicleSeller.vehicles.models import (
    Vehicle,
    VehicleManufacturingYear,
    VehicleTransmission,
    VehicleBrand,
    VehicleModel,
    VehicleEngine,
    VehicleEuroStandard,
    VehicleColor,
)

excluded_fields = (
    "manufacturing_year",
    "id",
)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Attributes:
        list_display (list): A list of fields to be displayed in the admin list view.
            The list is dynamically generated to include all fields from the Vehicle model, excluding any fields
            specified in the 'excluded_fields' list. Additionally, the 'manufactured' field is inserted at index 6.
    """

    list_display = [
        field.name
        for field in Vehicle._meta.fields
        if field.name not in excluded_fields
    ]
    list_display.insert(6, "manufactured")


@admin.register(VehicleManufacturingYear)
class VehicleManufacturingYearAdmin(admin.ModelAdmin, FormHelperMixin):
    pass


@admin.register(VehicleTransmission)
class VehicleManufacturingYearAdmin(admin.ModelAdmin, FormHelperMixin):
    pass


admin.site.register(VehicleBrand)
admin.site.register(VehicleModel)
admin.site.register(VehicleEngine)
admin.site.register(VehicleEuroStandard)
admin.site.register(VehicleColor)
