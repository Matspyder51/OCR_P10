# Generated by Django 3.2.6 on 2021-09-12 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0005_alter_project_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="type",
            field=models.CharField(
                choices=[
                    ("0", "Back-end"),
                    ("1", "Front-end"),
                    ("2", "iOS"),
                    ("3", "Android"),
                ],
                default=0,
                max_length=1,
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="IssueComment",
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
                ("description", models.CharField(max_length=8192)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "issue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="projects.issue"
                    ),
                ),
            ],
        ),
    ]
