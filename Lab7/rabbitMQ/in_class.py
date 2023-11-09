import requests
from bs4 import BeautifulSoup
import json


def crawl_product_urls(max_pages, initial_page_url):
    base_url = "https://999.md"
    page_urls = [initial_page_url]
    product_urls = set()
    visited_page_urls = set()
    pages_without_new_products = 0

    while page_urls and (len(visited_page_urls) < max_pages or '»' in page_urls[-1]) and pages_without_new_products < 3:
        current_page_url = page_urls.pop(0)

        if current_page_url in visited_page_urls:
            continue

        visited_page_urls.add(current_page_url)

        response = requests.get(current_page_url)
        soup = BeautifulSoup(response.content, "html.parser")

        new_product_found = False

        for anchor in soup.find_all('a', href=lambda href: href and not href.startswith('/b'), class_='js-item-ad'):
            link_href = anchor.get('href')
            complete_url = base_url + link_href
            if complete_url not in product_urls:
                product_urls.add(complete_url)
                new_product_found = True

        pagination_links = set(base_url + page_link['href'] for page_link in soup.select('nav.paginator > ul > li > a'))
        page_urls.extend(link for link in pagination_links if link not in visited_page_urls)

        if not new_product_found:
            pages_without_new_products += 1
        else:
            pages_without_new_products = 0

    actual_pages_scraped = len(visited_page_urls)
    max_pages = min(max_pages, actual_pages_scraped)  # adjust max_pages if it exceeds the number of available pages

    return product_urls, actual_pages_scraped

def save_to_json(parsed_product_urls, filename):
    with open(filename, 'w') as json_file:
        json.dump(list(parsed_product_urls), json_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    start_url = "https://999.md/ro/list/computers-and-office-equipment/laptops"
    max_pages = 2 # adjust the maximum number of pages

    parsed_product_urls, scraped_pages = crawl_product_urls(max_pages, start_url)

    output_file = "parsed_product_urls.json"
    save_to_json(parsed_product_urls, output_file)

    print(f"Scraping a maximum of {max_pages} pages with products from {start_url}")
    print(f"Saved {len(parsed_product_urls)} unique product URLs from {scraped_pages} pages to {output_file}")

    # print("Collected URLs:")
    # for i, url in enumerate(parsed_product_urls, start=1):
    #     print(f"{i}. {url}")