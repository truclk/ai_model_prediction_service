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
