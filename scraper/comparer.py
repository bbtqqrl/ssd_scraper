import csv
from dataclasses import asdict
from typing import List, Dict
from schemas import Product

def save_to_csv(products: List[Product], filename: str = "products.csv"):
    if not products:
        print("[WARNING] No products to save.")
        return
    dict_products = [asdict(p) for p in products]
    keys = dict_products[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(dict_products)

    print(f"[INFO] Saved {len(products)} products to {filename}")
