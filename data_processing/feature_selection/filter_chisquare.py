import pandas as pd
from data_processing.models import DatasetPreprocessed
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler


def feature_selection_filter_chisquare(dataset_preprocessed: DatasetPreprocessed, n_features_to_select=5):
    predict_column = dataset_preprocessed.predict_column
    df = pd.read_csv(dataset_preprocessed.dataset_file.path)
    X = df.drop(predict_column, axis=1)
    y = df[predict_column]

    # Ensure all data in X is non-negative
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    best_features = SelectKBest(score_func=chi2, k=n_features_to_select)
    fit = best_features.fit(X_scaled, y)

    # Summarize scores
    scores = pd.DataFrame(fit.scores_)
    columns = pd.DataFrame(X.columns)
    feature_scores = pd.concat([columns, scores], axis=1)
    feature_scores.columns = ["Feature", "Score"]
    print(feature_scores.nlargest(n_features_to_select, "Score"))

    # Convert the result to the desired format with scores
    feature_scores_dict = {
        item["Feature"]: {"Score": item["Score"]}
        for item in feature_scores.nlargest(n_features_to_select, "Score").to_dict("records")
    }
    return feature_scores_dict
