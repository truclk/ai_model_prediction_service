# Generated by Django 4.2.4 on 2023-09-04 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend_api", "0002_datasetresult_notebook_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="datasetupload",
            name="name",
            field=models.CharField(default="", max_length=255),
        ),
    ]