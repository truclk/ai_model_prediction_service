import pandas as pd
from backend_api.models import DatasetMetadata
from backend_api.models import DatasetUpload
from celery import shared_task


@shared_task
def analyze_metadata(dataset_upload_id):
    dataset_upload = DatasetUpload.objects.get(id=dataset_upload_id)

    df = pd.read_csv(dataset_upload.dataset_file.path)
    metadata = {
        "columns": list(df.columns),
        "data_types": df.dtypes.apply(lambda x: str(x)).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "unique_values": df.nunique().to_dict(),
    }

    # Basic statistics for numeric columns
    metadata["statistics"] = df.describe().fillna("N/A").to_dict()

    dataset_metadata, _ = DatasetMetadata.objects.get_or_create(dataset_upload=dataset_upload)
    dataset_metadata.metadata = metadata
    dataset_metadata.row_count = df.shape[0]
    dataset_metadata.column_count = df.shape[1]
    dataset_metadata.save()
    dataset_upload.status = "DETECTED_METADATA"
    dataset_upload.save()
