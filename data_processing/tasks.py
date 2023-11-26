from data_processing.feature_selection.wrapper_rfe import feature_selection_wrapper_rfe
from data_processing.feature_selection.filter_chisquare import feature_selection_filter_chisquare


@shared_task
def dataset_upload_feature_select(dataset_upload_id):
    dataset_upload = DatasetUpload.objects.get(id=dataset_upload_id)
    methods = {
        "rfe": wrapper_rfe,
        "chi2": filter_chisquare
    }

@shared_task
def run_feature_selection(dataset_upload_id, method):
    dataset_upload = DatasetUpload.objects.get(id=dataset_upload_id)
    n_features_to_select = 5
    results = {}
    if method == "rfe":
        features = feature_selection_wrapper_rfe(dataset_upload, n_features_to_select=n_features_to_select)
    elif method == "chi2":
        features = feature_selection_filter_chisquare(dataset_upload, n_features_to_select=n_features_to_select)
    else:
        raise ValueError(f"Invalid method: {method}")
    FeatureSelectionResult.objects.create(
        dataset_upload=dataset_upload,
        method=method,
        features=features,
    )
