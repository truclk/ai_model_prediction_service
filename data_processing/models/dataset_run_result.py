from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class DatasetRunResult(TimeStampedModel):
    client = models.ForeignKey("backend_api.Client", on_delete=models.CASCADE)
    dataset_run = models.ForeignKey("data_processing.DatasetRun", on_delete=models.CASCADE)
    predict_column = models.CharField(max_length=255, default="")
    number_of_features = models.IntegerField()
    method = models.CharField(max_length=255, default="", null=True)
    features = models.JSONField()
    results = models.JSONField(null=True)
    parameters = models.JSONField(null=True)
    model = models.CharField(
        max_length=255,
        choices=[
            ("naive_bayes", "Naive Bayes"),
            ("knn", "K-Nearest Neighbors"),
            ("lgbm", "LightGBM"),
            ("logistic_regression", "Logistic Regression"),
            ("naive_bayes_multiclass", "Naive Bayes Multiclass"),
            # ("decision_tree", "Decision Tree"),
            # ("random_forest", "Random Forest"),
            # ("svm", "Support Vector Machine"),
        ],
        default="naive_bayes",
    )  # The model name for training
    errors = models.JSONField(null=True)  # The errors that occurred during training
    status = models.CharField(
        max_length=255,
        choices=[
            ("PENDING", "PENDING"),
            ("STARTED", "STARTED"),
            ("RUNNING", "RUNNING"),
            ("SUCCESS", "SUCCESS"),
            ("FAILED", "FAILED"),
        ],
        default="PENDING",
    )
