from rest_framework import serializers
from VehicleSeller.vehicles.models import (
    Vehicle,
    VehicleBrand,
    VehicleColor,
    VehicleEngine,
    VehicleEuroStandard,
    VehicleManufacturingYear,
    VehicleModel,
    VehicleTransmission,
    VehicleImage,
)


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = "__all__"


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = "__all__"


class VehicleTransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleTransmission
        fields = "__all__"


class VehicleEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleEngine
        fields = "__all__"


class VehicleEuroStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleEuroStandard
        fields = "__all__"


class VehicleManufacturingYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleManufacturingYear
        fields = "__all__"


class VehicleColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleColor
        fields = "__all__"


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    brand = VehicleBrandSerializer()
    model = VehicleModelSerializer()
    transmission = VehicleTransmissionSerializer()
    engine_type = VehicleEngineSerializer()
    euro_standard = VehicleEuroStandardSerializer()
    manufacturing_year = VehicleManufacturingYearSerializer()
    color = VehicleColorSerializer()
    images = VehicleImageSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        exclude = ["seller"]

    def create(self, validated_data):
        brand_data = validated_data.pop("brand")
        model_data = validated_data.pop("model")
        transmission_data = validated_data.pop("transmission")
        engine_type_data = validated_data.pop("engine_type")
        euro_standard_data = validated_data.pop("euro_standard")
        manufacturing_year_data = validated_data.pop("manufacturing_year")
        color_data = validated_data.pop("color")
        seller = self.context["request"].user
        # TODO Might need to figure out a better way to serialize fields for models with choices
        brand = VehicleBrand.objects.create(**brand_data)
        model = VehicleModel.objects.create(**model_data)
        transmission = VehicleTransmission.objects.create(**transmission_data)
        engine_type = VehicleEngine.objects.create(**engine_type_data)
        euro_standard = VehicleEuroStandard.objects.create(**euro_standard_data)
        manufacturing_year = VehicleManufacturingYear.objects.create(**manufacturing_year_data)
        color = VehicleColor.objects.create(**color_data)

        vehicle = Vehicle.objects.create(
            brand=brand,
            model=model,
            transmission=transmission,
            engine_type=engine_type,
            euro_standard=euro_standard,
            manufacturing_year=manufacturing_year,
            color=color,
            seller=seller,
            **validated_data
        )

        return vehicle


