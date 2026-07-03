import pandas as pd
df = pd.read_csv("data/phishing.csv")
from features import has_extension, has_https, url_length, num_dots, num_hyphens, has_ip, count_digits

df['url_length'] = df['url'].apply(url_length)
df['num_dots'] = df['url'].apply(num_dots)
df['num_hyphens'] = df['url'].apply(num_hyphens)
df['has_https'] = df['url'].apply(has_https)
df['has_ip'] = df['url'].apply(has_ip)
df['count_digits'] = df['url'].apply(count_digits)
df['has_extension'] = df['url'].apply(has_extension)

print(df[['url', 'url_length', 'num_dots', 'num_hyphens', 'has_https', 'has_ip', 'count_digits', 'has_extension']].head())

df.to_csv("data/features.csv", index=False)
