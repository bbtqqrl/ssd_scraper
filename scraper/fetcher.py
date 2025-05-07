import requests
import cloudscraper
from bs4 import BeautifulSoup
from typing import Optional
from parser import extract_products_from_html_moyo
from comparer import save_to_csv, save_to_csv_moyo
from dotenv import load_dotenv
from schemas import Product
from datetime import datetime
import os
import random


load_dotenv()
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/136.0.0.0 Safari/537.36",
}


class RozetkaScraper:
    def __init__(self, category_id=80109):
        self.category_id = category_id
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )
        self.scraper.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7"
        })

        url = f"https://xl-catalog-api.rozetka.com.ua/v4/goods/get?category_id={self.category_id}"
        resp = self.scraper.get(url)
        if resp.status_code != 200:
            print(resp.status_code)
            raise Exception(f"Bad status code {resp.status_code}: {resp.text[:100]}")
        data = resp.json()["data"]

        self.total_pages = data["total_pages"]
        self.page_limit = data["goods_limit"]
        print(f"[INIT] total_pages={self.total_pages}, page_limit={self.page_limit}")

    def get_ids(self):
        all_ids = []
        for page in range(1, self.total_pages + 1):
            url = f"https://xl-catalog-api.rozetka.com.ua/v4/goods/get?category_id={self.category_id}&page={page}"
            resp = self.scraper.get(url)
            ids = resp.json()["data"]["ids"]
            all_ids.extend(ids)
        return all_ids
    
    def get_items(self, item_list):
        product_list = []
        while item_list:
            batch = item_list[:self.page_limit]
            product_ids = ','.join(map(str, batch))
            item_list = item_list[self.page_limit:] 
            url = f"https://xl-catalog-api.rozetka.com.ua/v4/goods/getDetails?product_ids={product_ids}"
            print(url)
            
            resp = self.scraper.get(url)
            ids = resp.json()
            product_list.extend(
                Product(id=int(item["id"]), brand=item["brand"], title=item["title"], price=float(item["price"]), href=item["href"])
                for item in ids["data"]
            )
            print(len(product_list))
        return product_list


class MoyoScraper:
    def __init__(self, url: str = "https://www.moyo.ua/ua/comp-and-periphery/inform_carrier/ssd/?page="):
        self.url = url
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            page_elements = soup.select("ul.pagination li[data-page]")
            page_numbers = [int(li['data-page']) for li in page_elements if li.has_attr("data-page")]

            if page_numbers:
                self.count_pages = max(page_numbers)
            else:
                print("[WARN] No page numbers found")
                self.count_pages = 1
        except Exception as e: 
            print(f"[ERROR] Failed to get total pages: {e}")
            self.count_pages = 1


    def fetch_html_moyo(self, timeout: int = 10) -> Optional[str]:
        html_list = []
        for page_num in range(self.count_pages):
            try:
                response = requests.get(f"{self.url}{page_num}", headers=HEADERS, timeout=timeout)
                response.raise_for_status()
                html_list.append(response.text)
            except requests.RequestException as e:
                print(f"[ERROR] Failed to fetch {self.url}: {e}")
                return None
        return html_list
    

Moyo = MoyoScraper()
html = Moyo.fetch_html_moyo()
parse_html = extract_products_from_html_moyo(html_list=html)
save_to_csv_moyo(parse_html, f"products_moyo_{datetime.now().date()}.csv")



kaka = RozetkaScraper()
data = kaka.get_ids()
baka = kaka.get_items(data)
save_to_csv(baka, f"products_rozetka_{datetime.now().date()}.csv")

