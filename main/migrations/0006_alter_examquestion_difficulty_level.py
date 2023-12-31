# Generated by Django 4.2.5 on 2023-10-09 04:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0005_alter_examquestion_difficulty_level"),
    ]

    operations = [
        migrations.AlterField(
            model_name="examquestion",
            name="difficulty_level",
            field=models.CharField(
                choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
                default="medium",
                max_length=10,
            ),
        ),
    ]
