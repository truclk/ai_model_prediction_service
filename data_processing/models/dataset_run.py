from django.db import models
from model_utils.models import TimeStampedModel


class DatasetRun(TimeStampedModel):
    # This is a run configuration
    # Including the Model using to train and all hyperparameters
    client = models.ForeignKey("backend_api.Client", on_delete=models.CASCADE)
    description = models.TextField()
    version = models.CharField(max_length=255)
    n_features_to_select = models.IntegerField(default=5)
    feature_selection_method = models.CharField(
        max_length=255,
        choices=[
            ("rfe", "Recursive Feature Elimination"),
            ("chi2", "Chi-Square"),
            ("manual", "Manual"),
        ],
        default="rfe",
    )
    dataset_preprocessed = models.ForeignKey("data_processing.DatasetPreprocessed", on_delete=models.CASCADE)
    features = models.JSONField()  # List of features in json array
    parameters = models.JSONField()  # The parameters for the model
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
    errors = models.JSONField(null=True)  # The errors that occurred during training
    models = models.JSONField(null=True)  # The models that were trained
