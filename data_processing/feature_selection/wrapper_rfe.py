from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from backend_api.models import DatasetUpload


def feature_selection_wrapper_rfe(dataset_upload: DatasetUpload, n_features_to_select=5):
    df = pd.read_csv(dataset_upload.dataset_file.path)
    X = df.drop(predict_column, axis=1)
    y = df[predict_column]
    model = RandomForestClassifier()
    rfe = RFE(model, n_features_to_select=5)  # Adjust the number of features

    # Fit the model
    rfe = rfe.fit(X, y)

    # Print the chosen features
    print("Chosen Features: ")
    for i in range(X.shape[1]):
        if rfe.support_[i]:
            print(X.columns[i])
    # Get the json in format feature as key and nested dict of score and rank
    feature_scores_dict = {}
    for i in range(X.shape[1]):
        if rfe.support_[i]:
            feature_scores_dict[X.columns[i]] = {
            }

