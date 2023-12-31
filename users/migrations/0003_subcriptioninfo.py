# Generated by Django 4.2.5 on 2023-12-24 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0002_userprofile_phone_no_userprofile_standard"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubcriptionInfo",
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
                ("activation_date", models.DateTimeField(blank=True, null=True)),
                ("expiry_date", models.DateTimeField(blank=True, null=True)),
                ("amount", models.IntegerField()),
                ("order_id", models.CharField(max_length=200)),
                ("payment_id", models.CharField(max_length=200)),
                ("paid", models.BooleanField(default=False)),
                (
                    "subscription_type",
                    models.CharField(
                        blank=True,
                        choices=[("monthly", "Monthly"), ("yearly", "Yearly")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
