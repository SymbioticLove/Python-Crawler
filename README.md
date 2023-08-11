# Web Crawler for Product Keywords

This script is designed to crawl a website and extract product/service keywords, brand names, and determine non-product/service pages. It utilizes the Beautiful Soup and NLTK libraries to parse and analyze the content.

## Functions

### `extract_brand_name(url, soup)`
- **Purpose:** Extracts the brand name from the given URL and the content of the page.
- **Parameters:** 
  - `url`: The URL of the page.
  - `soup`: BeautifulSoup object containing the HTML content.
- **Returns:** List of brand names.

### `extract_keywords(soup, brand_names)`
- **Purpose:** Extracts the product/service keywords from the given HTML content, excluding non-relevant words and brand names.
- **Parameters:**
  - `soup`: BeautifulSoup object containing the HTML content.
  - `brand_names`: List of brand names to exclude.
- **Returns:** Dictionary of product keywords with their frequency.

### `is_non_product_page(url)`
- **Purpose:** Determines if the given URL is a non-product/service page (e.g., account, cart, privacy).
- **Parameters:** 
  - `url`: The URL of the page.
- **Returns:** Boolean value indicating if the URL is a non-product page.

### `crawl_website(url, depth_limit, max_pages)`
- **Purpose:** Crawls the given website to a specified depth and extracts product/service keywords.
- **Parameters:**
  - `url`: The starting URL of the website.
  - `depth_limit`: Maximum depth to crawl.
  - `max_pages`: Maximum number of pages to visit.
- **Returns:** List of sorted product keywords based on relevance.

## Usage

Replace the `website_url`, `max_depth`, and `max_pages_to_crawl` variables in the main section to set the website and crawling parameters. Run the script to print the top product/service keywords.

```python
website_url = "https://aloyoga.com/"
max_depth = 3
max_pages_to_crawl = 50
product_keywords = crawl_website(website_url, max_depth, max_pages_to_crawl)
