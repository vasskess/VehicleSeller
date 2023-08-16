from django.contrib import admin

from VehicleSeller.vehicles.models import Vehicle


excluded_fields = (
    "manufacturing_year",
    "id",
)
# TODO This ^^^ might be moved if needs to, at some point !


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """
    Attributes:
        list_display (list): A list of fields to be displayed in the admin list view.
            The list is dynamically generated to include all fields from the Vehicle model, excluding any fields
            specified in the 'excluded_fields' list. Additionally, the 'manufactured' field is inserted at index 6.

    Methods:
        formfield_for_choice_field(self, db_field, request, **kwargs): Overrides the formfield_for_choice_field
            method of the admin.ModelAdmin class. This method modifies the choices displayed for the
            'year_of_manufacturing' field to remove the 'YEAR_' prefix.
    """

    list_display = [
        field.name
        for field in Vehicle._meta.fields
        if field.name not in excluded_fields
    ]
    list_display.insert(6, "manufactured")

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "manufacturing_year":
            kwargs["choices"] = [
                (choice[0], choice[1].replace("YEAR_", ""))
                for choice in db_field.choices
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)
