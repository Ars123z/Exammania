# Generated by Django 4.2.5 on 2023-09-30 09:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="phone_no",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="standard",
            field=models.CharField(
                blank=True,
                choices=[
                    ("9th", "9th Grade"),
                    ("10th", "10th Grade"),
                    ("11th", "11th Grade"),
                    ("12th", "12th Grade"),
                    ("12th+", "12th Grade and Above"),
                ],
                max_length=10,
                null=True,
            ),
        ),
    ]