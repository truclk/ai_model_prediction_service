import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from scipy import stats
from backend_api.models import DatasetUpload, DatasetMetadata


def analyze_metadata(dataset_upload: DatasetUpload):

    df = pd.read_csv(dataset_upload.dataset_file.path)
    metadata = {
        "columns": list(df.columns),
        "data_types": df.dtypes.apply(lambda x: str(x)).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "unique_values": df.nunique().to_dict(),
    }

    # Basic statistics for numeric columns
    metadata["statistics"] = df.describe().fillna("N/A").to_dict()

    dataset_metadata, _ = DatasetMetadata.objects.get_or_create(
        dataset_upload=dataset_upload
    )
    dataset_metadata.metadata = metadata
    dataset_metadata.row_count = df.shape[0]
    dataset_metadata.column_count = df.shape[1]
    dataset_metadata.save()
