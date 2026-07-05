import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("data/features.csv")

feature_cols = ["has_https", "url_length", "num_dots", "num_hyphens",
                "has_ip", "count_digits", "has_extension"]
X = df[feature_cols]
y = df["label"]

print(X.shape)
print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify = y)

print(X_train.shape)
print(X_test.shape)

model = RandomForestClassifier(class_weight="balanced", random_state=42)
model.fit(X_train, y_train)

print("training done")

predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

joblib.dump(model, "url_features_model.joblib")
print("model saved")

# y_proba = model.predict_proba(X_test)[:, 1]
# from sklearn.metrics import roc_auc_score
# print(classification_report(y_test, predictions))
# print("ROC-AUC:", roc_auc_score(y_test, y_proba))  # y_proba = model.predict_proba(X_test)[:,1]

# print(y_train.value_counts())
# print(y_test.value_counts())