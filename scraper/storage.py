import cloudscraper
import time
from comparer import save_to_csv

from schemas import Product

CATEGORY_ID = 80109  

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)
scraper.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7"
})

class RozetkaParser:
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


kaka = RozetkaParser()
data = kaka.get_ids()
print(len(data))
baka = kaka.get_items(data)
save_to_csv(baka)