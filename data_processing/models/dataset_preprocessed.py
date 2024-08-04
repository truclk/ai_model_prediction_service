from django.db import models
from model_utils.models import TimeStampedModel


def preprocessed_tenant_directory_path(instance, filename):
    # Assuming instance has a tenant attribute
    tenant_id = instance.client_id
    dataset_upload_id = instance.dataset_upload.id
    return f"./dataset_file/client_{tenant_id}/dataset_upload_{dataset_upload_id}/{filename}"


# Create your models here.
class DatasetPreprocessed(TimeStampedModel):
    # This is a preprocessed dataset with data clean up before that and ready for a training
    dataset_upload = models.ForeignKey("backend_api.DatasetUpload", on_delete=models.CASCADE)
    dataset_file = models.FileField(upload_to=preprocessed_tenant_directory_path)
    client = models.ForeignKey("backend_api.Client", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    description = models.TextField()
    config = models.JSONField(null=True, blank=True, default=dict)
    predict_column = models.CharField(max_length=255, default="")
