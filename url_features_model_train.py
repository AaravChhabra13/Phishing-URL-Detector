import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("data/features.csv")

feature_cols = df.columns.drop("label")
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

# print(y_train.value_counts())
# print(y_test.value_counts())