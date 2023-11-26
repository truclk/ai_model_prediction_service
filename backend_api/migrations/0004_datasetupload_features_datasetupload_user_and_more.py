# Generated by Django 4.2.4 on 2023-11-01 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("backend_api", "0003_datasetupload_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="datasetupload",
            name="features",
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name="datasetupload",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="datasetupload",
            name="dataset_file",
            field=models.FileField(upload_to="../dataset_file"),
        ),
        migrations.CreateModel(
            name="DatasetRun",
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
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("features", models.JSONField()),
                ("target", models.JSONField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "PENDING"),
                            ("RUNNING", "RUNNING"),
                            ("SUCCESS", "SUCCESS"),
                            ("FAILED", "FAILED"),
                        ],
                        default="PENDING",
                        max_length=255,
                    ),
                ),
                (
                    "dataset_upload",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend_api.datasetupload",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]