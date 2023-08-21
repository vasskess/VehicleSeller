# Generated by Django 4.2.3 on 2023-08-19 08:09

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0004_vehiclebrand_vehiclecolor_vehicleengine_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="VehicleImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "vehicle_image",
                    cloudinary.models.CloudinaryField(
                        max_length=255, verbose_name="Vehicle Image"
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="vehicles.vehicle",
                    ),
                ),
            ],
        ),
    ]