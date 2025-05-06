import csv
from typing import List, Dict
from dataclasses import asdict
from schemas import Product

def save_to_csv_moyo(products: List[Dict], filename: str = "products_moyo.csv"):
    if not products:
        print("[WARNING] No products to save.")
        return

    keys = products[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)

    print(f"[INFO] Saved {len(products)} products to {filename}")

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
