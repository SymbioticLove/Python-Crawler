import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from urllib.parse import urljoin
import random
import time
import re
from urllib.parse import urlparse

# Function to extract brand name from the url
def extract_brand_name(url, soup):
    url_brand_name = urlparse(url).netloc.split('.')[0]

    # Extract brand name from title tag, split by '-' or '|'
    title = soup.title.string
    brand_name_from_title = re.split(' - |- | \| |\|', title)[0].lower().split()

    # Find common words in URL and title
    common_brand_names = set(url_brand_name.split('-')).intersection(set(brand_name_from_title))

    brand_names = list(common_brand_names)

    return brand_names

# Function to extract product/service keywords
def extract_keywords(soup, brand_names):
    stop_words = set(stopwords.words("english"))
    non_relevant_words = {
        'shop', 'store', 'buy', 'product', 'products', 'item', 'items', 'new', 'card', 
        'equipment', 'best', 'site', 'content', 'term', 'terms', 'back', 'backward', 'forwards', 'forward'
    }  # Add more words as needed
    non_relevant_words.update(brand_names)

    product_keywords_freq = {}

    text = soup.get_text()
    sentences = sent_tokenize(text)
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = nltk.pos_tag(words)

        for word, tag in tagged_words:
            # Only include alphanumeric words that are nouns and not in stop words or non-relevant words
            if tag.startswith('NN') and word.isalnum() and word.lower() not in stop_words and word.lower() not in non_relevant_words:
                product_keywords_freq[word.lower()] = product_keywords_freq.get(word.lower(), 0) + 1

    return product_keywords_freq

# Function to determine if the URL is an account, cart, information, privacy, or other non-product/service page
def is_non_product_page(url):
    non_product_keywords = {'account', 'cart', 'information', 'privacy', 'assets', 'twitter', 'facebook', 'instagram'}
    for keyword in non_product_keywords:
        if keyword in url.lower():
            return True
    return False

# Function to crawl the website
def crawl_website(url, depth_limit, max_pages):
    visited_urls = set()
    product_keywords_freq = {}

    def visit_page(url, depth):
        if depth > depth_limit or len(visited_urls) >= max_pages:
            return
        # Simulate a browser response
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        try:
            # Check if the link is valid and not 'javascript:void(0)'
            if not url.startswith(('http://', 'https://')):
                return

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Check if the page is a non-product/service page
                if is_non_product_page(url):
                    return

                brand_names = extract_brand_name(url, soup)
                keywords = extract_keywords(soup, brand_names)

                for keyword in keywords:
                    product_keywords_freq[keyword] = product_keywords_freq.get(keyword, 0) + keywords[keyword]

                visited_urls.add(url)
                time.sleep(random.uniform(1, 2))  # Add random delay between crawls

                for link in soup.find_all("a", href=True):
                    new_url = link["href"]
                    if new_url.startswith("#"):  # Skip anchor links
                        continue
                    new_url = urljoin(url, new_url)  # Handle relative URLs
                    if new_url not in visited_urls:
                        visit_page(new_url, depth + 1)

        except Exception as e:
            print(f"Error while visiting {url}: {e}")

    visit_page(url, 1)

    # Sort product keywords based on relevance score
    sorted_product_keywords = sorted(product_keywords_freq.items(), key=lambda x: x[1], reverse=True)

    return sorted_product_keywords

if __name__ == "__main__":
    website_url = "https://aloyoga.com/"  # Replace this with the URL you want to crawl
    max_depth = 3
    max_pages_to_crawl = 50

    product_keywords = crawl_website(website_url, max_depth, max_pages_to_crawl)

    print(f"Top product/service keywords for {website_url}:")
    for keyword, frequency in product_keywords[:10]:  # Display the top 10 product/service keywords
        print(f"{keyword}: Frequency - {frequency}")
