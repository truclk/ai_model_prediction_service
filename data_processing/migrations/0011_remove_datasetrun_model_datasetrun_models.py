# Generated by Django 4.2.13 on 2024-07-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_processing", "0010_datasetrun_errors"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="datasetrun",
            name="model",
        ),
        migrations.AddField(
            model_name="datasetrun",
            name="models",
            field=models.JSONField(null=True),
        ),
    ]
