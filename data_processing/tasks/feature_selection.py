from celery import shared_task
from data_processing.feature_selection.filter_chisquare import \
    feature_selection_filter_chisquare
from data_processing.feature_selection.wrapper_rfe import \
    feature_selection_wrapper_rfe
from data_processing.models.dataset_run import DatasetRun


@shared_task
def run_feature_selection(dataset_run_id):
    dataset_run = DatasetRun.objects.get(id=dataset_run_id)
    dataset_preprocessed = dataset_run.dataset_preprocessed
    method = dataset_run.feature_selection_method
    n_features_to_select = dataset_run.n_features_to_select
    if method == "rfe":
        features = feature_selection_wrapper_rfe(dataset_preprocessed, n_features_to_select=n_features_to_select)
    elif method == "chi2":
        features = feature_selection_filter_chisquare(dataset_preprocessed, n_features_to_select=n_features_to_select)
    else:
        raise ValueError(f"Invalid method: {method}")
    dataset_run.features = features
    dataset_run.save()
