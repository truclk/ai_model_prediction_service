import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from backend_api.models import DatasetUpload

# Load data


def feature_selection_filter_chisquare(dataset_upload: DatasetUpload, n_features_to_select=5, predict_column=None):
    predict_column = predict_column or dataset_upload.predict_column
    df = pd.read_csv(dataset_upload.dataset_file.path)
    X = df.drop(predict_column, axis=1)
    y = df[predict_column or dataset_upload.predict_column]
    best_features = SelectKBest(score_func=chi2, k=n_features_to_select)
    fit = best_features.fit(X, y)

    # Summarize scores
    scores = pd.DataFrame(fit.scores_)
    columns = pd.DataFrame(X.columns)
    feature_scores = pd.concat([columns, scores], axis=1)
    feature_scores.columns = ['Feature', 'Score']
    print(feature_scores.nlargest(n_features_to_select, 'Score'))
    # Get the list of features
    # Get the json in format feature as key and nested dict of score and rank
    feature_scores_dict = feature_scores.nlargest(n_features_to_select, 'Score').to_dict('records')
    return feature_scores_dict
    
