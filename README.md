# Phishing URL Detector

A machine learning tool that analyzes a URL and predicts whether it is a phishing link or legitimate.

## Why this matters

Phishing is one of the most common ways people get scammed online. Attackers send links that look real to trick people into giving up passwords or downloading harmful files. If you can flag a bad link before someone clicks it, you stop the attack early. This tool does that by looking at the URL itself and predicting whether it is phishing.

## How it works

The tool takes a raw URL and turns it into a set of numbers called features. Each feature measures one thing about the URL, for example whether it uses https, whether it ends in a suspicious file extension like .exe, or whether it uses a raw IP address instead of a domain name. There are seven of these features in total.

Those seven numbers are then passed to a trained random forest model, which looks at the pattern across all of them and predicts whether the URL is phishing or legitimate.

## How to run it

1. Install the dependencies:

pip install -r requirements.txt

2. Put your dataset in the data folder, then build the features:

python build_features.py

3. Train the model:

python url_features_model_train.py

4. Check a single URL:

python check_url.py

You will be prompted to enter a URL, and the tool will predict whether it is phishing or legitimate.

## Results

The dataset was heavily imbalanced, with about 159,000 phishing URLs and only around 820 legitimate ones, so roughly 99.5 percent phishing. Because of this, I used balanced class weights during training so the model would not simply learn to label everything as phishing.

For a phishing detector, the most important metric is recall on the phishing class, because a missed phishing link is far more dangerous than a false alarm. On the held-out test set, the model reached close to 1.00 recall on phishing, meaning it caught nearly every phishing URL it was tested on.

These numbers are strong, but they should be read with some caution. The dataset contained many obvious phishing URLs, such as raw IP addresses serving executable files, which are easy to catch. On messier real-world traffic with more varied legitimate URLs, performance would likely be lower.

## Limitations

This model only looks at the surface features of a URL, so it misses attacks that those features cannot capture. The clearest example is lookalike domains. When I tested go1gle.com, a fake version of google.com with a 1 in place of an o, the model labeled it legitimate. The reason is that on every feature the model uses, go1gle.com looks completely normal. It is short, uses one dot, has no hyphens, is not an IP address, has no suspicious extension, and contains almost no digits. None of the seven features can detect that the word itself is a misspelling of a real brand, so the model has no way to catch it.

A second limitation came from a separate model I trained on a pre-featurized dataset. That dataset came with features already extracted but without the original URLs. Because I could not see the raw URLs and could not know exactly how each feature was defined, I could not build a checker that turns a new URL into those same features. If I guessed even one feature definition wrong, the model's predictions would be off. This taught me that owning your own feature extraction matters, because it is what lets a model actually be used on new data.

## Future work

The most important next step is a version 2 that can catch lookalike domains, which is the model's biggest weakness right now. The idea is to take a single URL and compare its domain against a list of well-known brands, then measure how many character changes separate them. A domain like go1gle.com is only one change away from google.com, so it would get flagged as suspicious even though none of the current seven features catch it. This would add a whole new type of detection that works on the actual text of the domain, rather than just its surface features.