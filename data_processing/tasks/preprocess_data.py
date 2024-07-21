import json

import pandas as pd
from backend_api.models import DatasetUpload
from celery import shared_task
from data_processing.models.dataset_preprocessed import DatasetPreprocessed
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

"""
{
  "columns": {
    "age": {
      "data_type": "numeric",
      "operations": {
        "missing_value_imputation": {"strategy": "mean"},
        "standardization": {}
      }
    },
    "income": {
      "data_type": "numeric",
      "operations": {
        "missing_value_imputation": {"strategy": "median"},
        "normalization": {}
      }
    },
    "gender": {
      "data_type": "categorical",
      "operations": {
        "missing_value_imputation": {"strategy": "mode"},
        "encoding": {}
      }
    }
  }
}

"""


@shared_task
def preprocess_data(dataset_upload_id, config):
    dataset_upload = DatasetUpload.objects.get(id=dataset_upload_id)
    original_file_path = dataset_upload.dataset_file.path
    # The outcome of this step is to create a dataset preprocessed

    # 1. Read the file
    dataframe = pd.read_csv(original_file_path)

    # 2. Clean up the data

    for column, specs in config["columns"].items():
        operations = specs["operations"]

        # Handle missing value imputation first
        if "missing_value_imputation" in operations:
            strategy = operations["missing_value_imputation"].get("strategy", "mean")
            if strategy == "mean":
                dataframe[column].fillna(dataframe[column].mean(), inplace=True)
            elif strategy == "median":
                dataframe[column].fillna(dataframe[column].median(), inplace=True)
            elif strategy == "mode":
                dataframe[column].fillna(dataframe[column].mode()[0], inplace=True)
            else:
                dataframe[column].fillna(strategy, inplace=True)  # Direct value replacement

        # Apply other preprocessing operations
        for operation, params in operations.items():
            if operation != "missing_value_imputation":
                if operation == "standardization":
                    dataframe[column] = StandardScaler().fit_transform(dataframe[[column]])

                elif operation == "normalization":
                    dataframe[column] = MinMaxScaler().fit_transform(dataframe[[column]])

                elif operation == "encoding":
                    dataframe[column] = LabelEncoder().fit_transform(dataframe[column])

                elif operation == "one_hot_encoding":
                    one_hot = OneHotEncoder()
                    transformed_data = one_hot.fit_transform(dataframe[[column]]).toarray()
                    one_hot_columns = [f"{column}_{category}" for category in one_hot.categories_[0]]
                    dataframe = dataframe.drop(column, axis=1)
                    dataframe = pd.concat(
                        [
                            dataframe,
                            pd.DataFrame(transformed_data, columns=one_hot_columns),
                        ],
                        axis=1,
                    )

    # 3. Save the file
    processed_file_path = f"{original_file_path}.processed"
    dataframe.to_csv(processed_file_path, index=False)
    dataset_preprocessed = DatasetPreprocessed(
        client_id=dataset_upload.client.id, dataset_file=processed_file_path, dataset_upload=dataset_upload
    )
    # 4. Create a dataset preprocessed
    dataset_preprocessed.save()
    return dataset_preprocessed.id
