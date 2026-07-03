import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

df2 = pd.read_csv("data/phishing_2.csv")
# print(df2.head())
# print(df2['target'].value_counts())

feature_cols2 = df2.columns.drop("target")
# print(feature_cols2)

X2 = df2[feature_cols2]
y2 = df2["target"]

X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y2, test_size=0.2, random_state=42)
model2 = RandomForestClassifier(random_state=42)
model2.fit(X_train2, y_train2)

print("training done")

predictions = model2.predict(X_test2)
print(classification_report(y_test2, predictions))

joblib.dump(model2, "pretrained_features_model.joblib")
print("model saved")
