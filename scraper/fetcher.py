import requests
from bs4 import BeautifulSoup
from typing import Optional
from parser import extract_products_from_html
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_html(url: str, count_pages: int,  timeout: int = 10) -> Optional[str]:
    html_list = []
    for page_num in range(count_pages):
        try:
            response = requests.get(f"{url}{page_num}", headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            html_list.append(response.text)
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            return None
    return html_list


def get_total_pages(url: str) -> int:
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        page_elements = soup.select("ul.pagination li[data-page]")
        page_numbers = [int(li['data-page']) for li in page_elements if li.has_attr("data-page")]

        if page_numbers:
            return max(page_numbers)
        else:
            print("[WARN] No page numbers found")
            return 1

    except Exception as e:
        print(f"[ERROR] Failed to get total pages: {e}")
        return 1
    
url = "https://www.moyo.ua/ua/comp-and-periphery/inform_carrier/ssd/?page="
count_pages = get_total_pages(url)
html = fetch_html(url, count_pages)
products = extract_products_from_html(html_list=html)
print(products)

    
