# Generated by Django 4.2.5 on 2023-10-09 04:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_examquestion_difficulty_level_examquestion_subject_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="examquestion",
            name="difficulty_level",
            field=models.CharField(
                choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
                max_length=10,
            ),
        ),
    ]
