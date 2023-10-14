from django.contrib.auth import User
from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.


class Client(TimeStampedModel):
    # Multi tenant in the future
    name = models.CharField(max_length=255)


# class TrainningRun(TimeStampedModel):
#     # This set would contains the training of client
#     # Each set has a unique id
#     # Each set has a unique name
#     # Includes the dataset data schema and version
#     # Includes the model template of this run
#     # Includes the parameters for the model template
#     # Includes the status of this run
#     # Includes the start time of this run
#     # Includes the end time of this run
#     # Includes the result of this run
#     name = models.CharField(max_length=255)
#     version = models.CharField(max_length=255)
#     description = models.TextField()
#     dataset = models.ForeignKey("datasets.Dataset", on_delete=models.CASCADE)
#     category = models.CharField(max_length=255)
#     client = models.ForeignKey("Client", on_delete=models.CASCADE)

#     model_template = models.ForeignKey(
#         "model_templates.ModelTemplate", on_delete=models.CASCADE
#     )
#     parameters = models.JSONField()
#     status = models.CharField(max_length=255)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     result = models.JSONField()


class DatasetUpload(TimeStampedModel):
    # This set would contains the training of client
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dataset_file = models.FileField(upload_to="../dataset_file")
    name = models.CharField(max_length=255, default="")
    features = models.JSONField(null=True)
    predict_column = models.CharField(max_length=255, default="")
    status = models.CharField(
        max_length=255,
        choices=[
            ("PENDING", "PENDING"),
            ("RUNNING", "RUNNING"),
            ("SUCCESS", "SUCCESS"),
            ("FAILED", "FAILED"),
        ],
        default="PENDING",
    )


class DatasetRun(TimeStampedModel):
    dataset_upload = models.ForeignKey("DatasetUpload", on_delete=models.CASCADE)
    features = models.JSONField()
    target = models.JSONField()
    status = models.CharField(
        max_length=255,
        choices=[
            ("PENDING", "PENDING"),
            ("RUNNING", "RUNNING"),
            ("SUCCESS", "SUCCESS"),
            ("FAILED", "FAILED"),
        ],
        default="PENDING",
    )


class DatasetResult(TimeStampedModel):
    dataset_upload = models.ForeignKey("DatasetUpload", on_delete=models.CASCADE)
    notebook_name = models.CharField(max_length=255, default="")
    results = models.JSONField()
