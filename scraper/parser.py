import re
import json
from typing import List, Dict, Optional

def extract_products_from_html_moyo(html_list: list) -> Optional[List[Dict]]:
    pattern = r"window\.dataLayer\.push\((\{.*?\})\);"
    products = []
    for html_page in html_list:
        match = re.search(pattern, html_page, re.DOTALL)
        if not match:
            print("[ERROR] dataLayer block not found")
            continue

        try:
            data = json.loads(match.group(1))
            for pid, price, name in zip(data["productId"], data["productPrice"], data["productName"]):
                products.append({
                    "id": pid,
                    "price": price,
                    "name": name
                })
        except Exception as e:
            print(f"[ERROR] JSON parsing failed: {e}")
            continue

    return products

