# Generated by Django 4.2.5 on 2023-10-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExamQuestionOptions",
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
                ("content", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="ExamQuestion",
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
                ("body", models.TextField()),
                (
                    "correct_options",
                    models.ManyToManyField(
                        related_name="correct_options", to="main.examquestionoptions"
                    ),
                ),
                (
                    "options",
                    models.ManyToManyField(
                        related_name="options", to="main.examquestionoptions"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Exam",
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
                ("name", models.CharField(max_length=25)),
                ("year", models.IntegerField()),
                (
                    "questions",
                    models.ManyToManyField(
                        related_name="Exams", to="main.examquestion"
                    ),
                ),
            ],
        ),
    ]
