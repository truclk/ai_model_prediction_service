from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class Dataset(TimeStampedModel):
    # Each dataset has a name and a schema.
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    description = models.TextField()

    raw_data_schema = models.JSONField()
    raw_path = models.CharField(max_length=1024)

    processed_data_schema = models.JSONField()
    processed_path = models.CharField(max_length=1024)
