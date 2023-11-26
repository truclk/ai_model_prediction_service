from celery import shared_task
from jupiter_service.nbrunner import main

from backend_api.models import DatasetUpload

NOTEBOOKS = [
    "naive_bayes.ipynb",
    "logistic_regression.ipynb",
    "knn.ipynb",
    "lgbm.ipynb",
]


@shared_task
def process_dataset_upload(dataset_upload_id):
    dataset_upload = DatasetUpload.objects.get(id=dataset_upload_id)
    dataset_upload.status = "RUNNING"
    dataset_upload.save()
    path = dataset_upload.dataset_file.path
    predict_column = dataset_upload.predict_column
    for notebook_name in NOTEBOOKS:
        notebook_path = f"/model_templates/{notebook_name}"
        results = main(
            notebook_path, training_file_path=path, predict_column=predict_column
        )
        dataset_upload.datasetresult_set.create(
            results=results, notebook_name=notebook_name
        )

    dataset_upload.status = "SUCCESS"
    dataset_upload.save()


@shared_task
def process_dataset_upload(dataset_upload_id):
    dataset_upload = DatasetUpload.objects.get(id=dataset_upload_id)
    
