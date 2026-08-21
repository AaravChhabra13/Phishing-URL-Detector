import re
from Levenshtein import distance

KNOWN_BRANDS = [
    "google", "paypal", "amazon", "apple", "microsoft", "netflix",
    "facebook", "instagram", "chase", "bankofamerica", "wellsfargo",
    "ebay", "linkedin", "twitter", "dropbox", "adobe", "coinbase",
    "instagram", "citibank", "americanexpress", "yahoo", "outlook",
    "spotify", "walmart", "irs", "meta", "tiktok", "reddit", "pinterest", "tumblr", "quora"
]

def has_https(url):
    return int(url.startswith("https"))

def url_length(url):
    return len(url)

def num_dots(url):
    return url.count('.')

def num_hyphens(url):
    return url.count('-')

def has_ip(url):
    part = url.split('//')[-1].split('/')[0]
    if part == "":
        return 0
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    return int(bool(re.match(pattern, part)))

def count_digits(url):
    count = 0
    for char in url:
        if char.isdigit():
            count += 1
    return count

def has_extension(url):
    return int(url.endswith((".exe", ".sh", ".bat", ".msi")))

def brand_edit_distance(url):
    part = url.split('//')[-1].split('/')[0].lower()
    domain_parts = part.split('.')
    core = domain_parts[-2] if len(domain_parts) >= 2 else domain_parts[0]
    min_distance = min(distance(core, brand) for brand in KNOWN_BRANDS)
    return min_distance

# print(brand_edit_distance("http://go1gle.com/login"))
# print(brand_edit_distance("https://www.google.com/search"))
# print(brand_edit_distance("http://totallyrandomsite.net"))
