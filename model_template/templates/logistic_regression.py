import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# This one input
train = pd.read_csv("train.csv")
target = train["redemption_status"]
train = train.drop(["redemption_status"], axis=1)

x = pd.DataFrame(train)
y = target
col_names = [
    "cd_sum",
    "coupon_discount_x",
    "coupon_used_x",
    "item_counts",
    "no_of_customers",
    "od_sum",
    "other_discount_x",
    "price_sum",
    "qu_sum",
    "quantity_x",
    "selling_price_x",
    "t_counts",
    "total_discount_mean",
    "total_discount_sum",
    "campaign_type",
    "campaign_duration",
    "family_size",
    "no_of_children",
    "income_bracket",
    "coupon_discount_y",
    "coupon_used_y",
    "no_of_items",
    "other_discount_y",
    "quantity_y",
    "selling_price_y",
    "cdd_sum",
    "customer_id_count",
    "odd_sum",
    "qa_sum",
    "pprice_sum",
]
features = x[col_names]
scaler = StandardScaler().fit(features.values)
features = scaler.transform(features.values)
x[col_names] = features
x = np.array(x)


x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=2439
)
LR = LogisticRegression()
LR.fit(x_train, y_train)
y_pred_LR = LR.predict(x_test)

accuracy_score_result = accuracy_score(y_test, y_pred_LR)
roc_auc_score_result = roc_auc_score(y_test, y_pred_LR)
print("accuracy_score:", accuracy_score_result)
print("roc_auc_score:", roc_auc_score_result)
