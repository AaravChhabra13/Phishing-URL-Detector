import re

def has_https(url):
    return int(url.startswith("https"))

# print(has_https("https://www.google.com"))   # should print 1
# print(has_https("http://phishing-site.com"))  # should print 0

def url_length(url):
    return len(url)

# print(url_length("https://google.com/search"))

def num_dots(url):
    return url.count('.')

# print(num_dots("https://www.example.com/path/to/page.html"))  # should print 3

def num_hyphens(url):
    return url.count('-')

# print(num_hyphens("https://www-example.com/path/to/page.html"))  # should print 2

def has_ip(url):
    part = url.split('//')[-1].split('/')[0]
    if part == "":
        return 0
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    return int(bool(re.match(pattern, part)))

# print(has_ip("http://192.168.1.1/login"))     # should print 1
# print(has_ip("https://www.google.com/search")) # should print 0

def count_digits(url):
    count = 0
    for char in url:
        if char.isdigit():
            count += 1
    return count

# print(count_digits("http://192.168.1.1/login"))   # should print 8
# print(count_digits("https://google.com"))          # should print 0

def has_extension(url):
    return int(url.endswith((".exe", ".sh", ".bat", ".msi")))

