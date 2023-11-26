from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class FeatureSelectionResult(TimeStampedModel):
    dataset_upload = models.ForeignKey("backend_api.DatasetUpload", on_delete=models.CASCADE)
    number_of_features = models.IntegerField()
    method = models.CharField(max_length=255)
    features = models.JSONField()
