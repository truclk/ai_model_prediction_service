from celery import shared_task
from data_processing.feature_selection.filter_chisquare import \
    feature_selection_filter_chisquare
from data_processing.feature_selection.wrapper_rfe import \
    feature_selection_wrapper_rfe
from data_processing.models.dataset_preprocessed import DatasetPreprocessed


@shared_task
def run_feature_selection(dataset_preprocessed_id, method, n_features_to_select):
    dataset_upload = DatasetPreprocessed.objects.get(id=dataset_preprocessed_id)
    if method == "rfe":
        features = feature_selection_wrapper_rfe(dataset_upload, n_features_to_select=n_features_to_select)
    elif method == "chi2":
        features = feature_selection_filter_chisquare(dataset_upload, n_features_to_select=n_features_to_select)
    else:
        raise ValueError(f"Invalid method: {method}")
    return features
