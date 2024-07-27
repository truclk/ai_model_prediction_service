from celery import shared_task
from data_processing.models import DatasetRun
from data_processing.models import DatasetRunResult
from jupiter_service.nbrunner import main

NOTEBOOKS = [
    "naive_bayes.ipynb",
    "logistic_regression.ipynb",
    "knn.ipynb",
    "lgbm.ipynb",
]
MODEL_NOTEBOOKS = {
    "naive_bayes": "naive_bayes.ipynb",
    "logistic_regression": "logistic_regression.ipynb",
    "knn": "knn.ipynb",
    "lgbm": "lgbm.ipynb",
}


@shared_task
def train_dataset_run(dataset_run_id):
    dataset_run = DatasetRun.objects.get(id=dataset_run_id)
    dataset_run.status = "RUNNING"
    dataset_run.save()
    path = dataset_run.dataset_preprocessed.dataset_file.path
    predict_column = dataset_run.dataset_preprocessed.predict_column
    for model in dataset_run.models:
        if model not in MODEL_NOTEBOOKS:
            continue
        notebook_name = MODEL_NOTEBOOKS[model]
        notebook_path = f"/model_templates/{notebook_name}"
        dataset_run_result = DatasetRunResult.objects.create(
            model=model,
            client=dataset_run.client,
            dataset_run=dataset_run,
            predict_column=predict_column,
            number_of_features=dataset_run.n_features_to_select,
            method=dataset_run.feature_selection_method,
            features=dataset_run.features,
        )
        dataset_run_result.status = "RUNNING"
        results, errors = main(notebook_path, training_file_path=path, predict_column=predict_column)
        dataset_run_result.results = results
        dataset_run_result.errors = errors
        dataset_run_result.status = "SUCCESS" if not errors else "FAILED"
        dataset_run_result.save()
    dataset_run.status = "SUCCESS"
    dataset_run.save()
