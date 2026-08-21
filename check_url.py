import joblib
import pandas as pd
from features import has_extension, has_https, url_length, num_dots, num_hyphens, has_ip, count_digits, brand_edit_distance

model = joblib.load("url_features_model.joblib")

url = input("Enter a URL to check: ")

features = pd.DataFrame([{
    "has_https": has_https(url),
    "url_length": url_length(url),
    "num_dots": num_dots(url),
    "num_hyphens": num_hyphens(url),
    "has_ip": has_ip(url),
    "count_digits": count_digits(url),
    "has_extension": has_extension(url),
    "brand_edit_distance": brand_edit_distance(url)
}])

# print(list(features.columns))

prediction = model.predict(features)
print(prediction)

proba = model.predict_proba(features)
print("probability [legit, phishing]:", proba)