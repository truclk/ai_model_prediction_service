from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.


class Client(TimeStampedModel):
    # Multi tenant in the future
    name = models.CharField(max_length=255)


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
    dataset = models.ForeignKey("datasets.Dataset", on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    client = models.ForeignKey("Client", on_delete=models.CASCADE)

    model_template = models.ForeignKey(
        "model_templates.ModelTemplate", on_delete=models.CASCADE
    )
    parameters = models.JSONField()
    status = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    result = models.JSONField()
