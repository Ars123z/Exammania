# Generated by Django 4.2.5 on 2023-11-20 08:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0013_alter_exam_questions"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exam",
            options={"ordering": ["name", "year"]},
        ),
    ]
