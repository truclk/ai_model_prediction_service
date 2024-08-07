# Generated by Django 4.2.13 on 2024-07-26 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_processing", "0008_datasetrunresult_results"),
    ]

    operations = [
        migrations.AddField(
            model_name="datasetrunresult",
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
    ]
