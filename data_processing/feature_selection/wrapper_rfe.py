import pandas as pd
from data_processing.models import DatasetPreprocessed
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE


def feature_selection_wrapper_rfe(dataset_preprocessed: DatasetPreprocessed, n_features_to_select=5):
    df = pd.read_csv(dataset_preprocessed.dataset_file.path)
    predict_column = dataset_preprocessed.predict_column
    X = df.drop(predict_column, axis=1)
    y = df[predict_column]
    model = RandomForestClassifier()
    rfe = RFE(model, n_features_to_select=5)

    # Fit the model
    rfe = rfe.fit(X, y)

    # Print the chosen features
    print("Chosen Features: ")
    for i in range(X.shape[1]):
        if rfe.support_[i]:
            print(X.columns[i])
    feature_scores_dict = {}
    for i in range(X.shape[1]):
        if rfe.support_[i]:
            feature_scores_dict[X.columns[i]] = {}
    return feature_scores_dict
