# Phishing URL Detector

A machine learning tool that analyzes a URL and predicts whether it is a phishing link or legitimate.

## Why this matters

Phishing is one of the most common ways people get scammed online. Attackers send links that look real to trick people into giving up passwords or downloading harmful files. If you can flag a bad link before someone clicks it, you stop the attack early. This tool does that by looking at the URL itself and predicting whether it is phishing.

## How it works

The tool takes a raw URL and turns it into a set of numbers called features. Each feature measures one thing about the URL, for example whether it uses https, whether it ends in a suspicious file extension like .exe, or whether it uses a raw IP address instead of a domain name. There are eight of these features in total, including a brand similarity feature that measures how close a URL's domain is to a list of 24 well known brands using edit distance, to help catch lookalike domains like go1gle.com.

Those eight numbers are then passed to a trained random forest model, which looks at the pattern across all of them and predicts whether the URL is phishing or legitimate.

## Dataset

This project is trained on a public dataset of about 160,000 phishing and legitimate URLs from Kaggle. The dataset is not included in this repository because of its size, so you need to download it yourself.

Download it from https://www.kaggle.com/datasets/victusadi/phishing-urls-dataset-with-extracted-features and place the CSV in a folder called data inside the project, so the path is data/phishing.csv.

This dataset includes both the raw URL and a set of pre-extracted features. This project uses only the raw url column and the label, and builds its own seven features from scratch, so the pre-extracted columns are not used.

In addition to the main dataset, this project includes 1,000 synthetic lookalike domain URLs, generated to train the brand similarity feature. These were built using common typosquatting techniques such as character substitution, letter doubling, letter dropping, and adjacent letter swaps across the 24 brands checked by this project, and verified so each one is genuinely a close match to a real brand name before being included.

The trained model files are also not included. They are created when you run the training script, so the run steps below will generate them for you.

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

Looking at feature importance after training, url_length and num_dots account for roughly three quarters of the model's decisions, which makes sense given how many phishing URLs in this dataset are long, multi-part paths off raw IPs. The brand similarity feature contributes real but smaller weight, since it is solving a different, rarer pattern in this particular dataset.

## Limitations

This model only looks at the surface features of a URL, so it can miss attacks that those features do not capture well. The clearest example is lookalike domains. I added a feature that measures edit distance between a URL's domain and a list of known brands, along with 1,000 synthetic training examples built specifically to teach this pattern. Testing showed this genuinely worked, in the sense that the model's confidence noticeably shifts for lookalike domains, a URL like go2gle.com scores around 40 percent phishing probability rather than being ignored entirely. But it is not yet enough to flip the final prediction past the 50 percent decision threshold.

Looking at feature importance explains why. url_length and num_dots dominate the model's decisions, because most phishing URLs in this dataset are long, multi-part paths from raw IP addresses, and the model learned that pattern very strongly since it explains the large majority of the dataset. Lookalike domains are short and clean on every feature except brand similarity, so they have to fight against two much more heavily weighted features that are usually right. The brand similarity feature is doing real work, it is just currently outweighed.

A second limitation came from a separate model I trained on a pre-featurized dataset. That dataset came with features already extracted but without the original URLs. Because I could not see the raw URLs and could not know exactly how each feature was defined, I could not build a checker that turns a new URL into those same features. This taught me that owning your own feature extraction matters, because it is what lets a model actually be used on new data.

## Future work

The most direct next step is to use the model's probability output rather than its hard prediction for lookalike domains. Instead of a plain phishing or legitimate answer, a rule like flagging anything above 30 percent phishing probability for manual review would already catch cases like go2gle.com, which the current 50 percent threshold misses. This is a real design tradeoff between sensitivity and false alarms that security tools make regularly.

A second option is training a separate, smaller model focused specifically on lookalike detection, so brand similarity is not competing against features tuned for a very different, more common attack pattern in the same forest. A third option is adding meaningfully more synthetic lookalike examples, though testing this session showed that simply adding more rows is not enough on its own unless they are verified to actually carry the intended signal, since a first attempt at generating more data failed to do this and needed to be corrected.