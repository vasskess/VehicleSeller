from django.contrib.admin.options import BaseModelAdmin


class FormHelperMixin(BaseModelAdmin):
    """
    Methods:
        formfield_for_choice_field(self, db_field, request, **kwargs): Overrides the formfield_for_choice_field
            method of the admin.ModelAdmin class. This method modifies the choices displayed for the
            "year_of_manufacturing" field to remove the "YEAR_" prefix and
            "vehicle_transmission" field to lower and capitalize first letter.
    """

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "vehicle_manufacturing_year":
            kwargs["choices"] = [
                (choice[0], choice[1].replace("YEAR_", ""))
                for choice in db_field.choices
            ]
        if db_field.name == "vehicle_transmission":
            kwargs["choices"] = [
                (choice[0], choice[1].lower().capitalize())
                for choice in db_field.choices
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)
