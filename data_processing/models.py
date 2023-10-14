from django.db import models
from model_utils.models import TimeStampedModel


class DatasetFeature(TimeStampedModel):
    dataset_upload = models.ForeignKey(
        "DatasetUpload", on_delete=models.CASCADE, related_name="dataset_features"
    )
    name = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    number_of_feature = models.IntegerField(default=3)
    list_of_feature = models.JSONField()

    def __str__(self):
        return f"{self.dataset_upload.name} - {self.name}"
