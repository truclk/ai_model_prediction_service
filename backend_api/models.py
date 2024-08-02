from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.


class Client(TimeStampedModel):
    # Multi tenant in the future
    name = models.CharField(max_length=255)


class ClientUser(TimeStampedModel):
    # This model is the relationship between user and client
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    role = models.CharField(
        max_length=255,
        choices=[
            ("ADMIN", "ADMIN"),
            ("USER", "USER"),
        ],
    )


class TrainningRun(TimeStampedModel):
    # This set would contains the training of client
    # Each set has a unique id
    # Each set has a unique name
    # Includes the dataset data schema and version
    # Includes the model template of this run
    # Includes the parameters for the model template
    # Includes the status of this run
    # Includes the start time of this run
    # Includes the end time of this run
    # Includes the result of this run
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    description = models.TextField()
    # dataset = models.ForeignKey("datasets.Dataset", on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    client = models.ForeignKey("Client", on_delete=models.CASCADE)

    # model_template = models.ForeignKey(
    #     "model_templates.ModelTemplate", on_delete=models.CASCADE
    # )
    parameters = models.JSONField()
    status = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    result = models.JSONField()


def upload_tenant_directory_path(instance, filename):
    # Assuming instance has a tenant attribute
    tenant_id = instance.client_id
    timestamp = instance.created.strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{filename}"
    return f"./dataset_file/client_{tenant_id}/upload/{filename}"


class DatasetUpload(TimeStampedModel):
    # This set would contains the training of client
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=True)
    dataset_file = models.FileField(upload_to=upload_tenant_directory_path)
    name = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    status = models.CharField(
        max_length=255,
        choices=[
            ("PENDING", "PENDING"),
            ("DETECTED_METADATA", "DETECTED_METADATA"),
            ("PREPROCESSED", "PREPROCESSED"),
            ("RUNNING", "RUNNING"),
            ("SUCCESS", "SUCCESS"),
            ("FAILED", "FAILED"),
        ],
        default="PENDING",
    )


class DatasetMetadata(TimeStampedModel):
    # This model would describe the dataset metadata including list of features, type of features
    # Number of rows, number of columns, etc.
    dataset_upload = models.OneToOneField("DatasetUpload", on_delete=models.CASCADE, related_name="metadata")
    metadata = models.JSONField(null=True)
    row_count = models.IntegerField(null=True)
    column_count = models.IntegerField(null=True)
