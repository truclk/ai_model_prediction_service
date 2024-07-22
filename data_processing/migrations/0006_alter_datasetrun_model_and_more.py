# Generated by Django 4.2.13 on 2024-07-21 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_processing", "0005_datasetrun_datasetrunresult"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datasetrun",
            name="model",
            field=models.CharField(
                choices=[
                    ("naive_bayes", "Naive Bayes"),
                    ("knn", "K-Nearest Neighbors"),
                    ("lgbm", "LightGBM"),
                    ("logistic_regression", "Logistic Regression"),
                ],
                default="naive_bayes",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="datasetrun",
            name="predict_column",
            field=models.CharField(default="", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="datasetrun",
            name="target",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
