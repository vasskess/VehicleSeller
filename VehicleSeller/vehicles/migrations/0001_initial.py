# Generated by Django 4.2.3 on 2023-08-16 13:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Vehicle",
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
                ("brand", models.CharField(max_length=100, verbose_name="Brand")),
                (
                    "vehicle_model",
                    models.CharField(max_length=100, verbose_name="Model"),
                ),
                (
                    "transmission",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Transmission",
                    ),
                ),
                ("is_used", models.BooleanField(default=False)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=9,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Price",
                    ),
                ),
                ("mileage", models.PositiveIntegerField(verbose_name="Mileage")),
                ("color", models.CharField(max_length=50, verbose_name="Color")),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]