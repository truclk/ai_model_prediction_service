from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.


class ModelRun(models.Model):
    # This model contains each run of the job
    # Each run has a unique id
    # Each run has a unique name
    # Each run has a model template
    # Each run has parameters for the model template
    # Each run has a status
    # Each run has a start time
    # Each run has an end time
    # Each run has a result

    def submit_job_to_cluster(self):
        # This would send
        pass

    def get_job_status(self):
        pass

    def get_results(self):
        pass
