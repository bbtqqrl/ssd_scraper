import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from typing import Optional
from parser import extract_products_from_html_moyo
from comparer import save_to_csv
from dotenv import load_dotenv
import os
import random


load_dotenv()
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/136.0.0.0 Safari/537.36",
    "Referer": "https://hard.rozetka.com.ua/ua/ssd/c80109/",
    "Origin":  "https://hard.rozetka.com.ua",
    "X-Requested-With": "XMLHttpRequest",
}


def fetch_html_moyo(url: str, count_pages: int,  timeout: int = 10) -> Optional[str]:
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


def get_total_pages_moyo(url: str) -> int:
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
    
# url = "https://www.moyo.ua/ua/comp-and-periphery/inform_carrier/ssd/?page="
# count_pages = get_total_pages_moyo(url)
# html = fetch_html_moyo(url, count_pages)
# products = extract_products_from_html_moyo(html_list=html)
# save_to_csv(products)

def fetch_html_rozetka(url: str, cookies: dict,  timeout: int = 10) -> Optional[str]:
    html_list = []
    # for page_num in range(count_pages):
    try:
        response = requests.get(url, headers=HEADERS, cookies=cookies, timeout=timeout, proxies={"http": None, "https": None})
        response.raise_for_status()
        html_list.append(response.text)
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None
    return html_list



def get_rozetka_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="c:/Users/maksp/OneDrive/Документи/chrome-win/chrome.exe", headless=False)  # headless=False = бачиш браузер
        page = browser.new_page()

        # відкриваємо головну сторінку Rozetka
        page.goto("https://rozetka.com.ua/")

        page.wait_for_timeout(5000)  # чекаємо 5 секунд — сайт виконає JS, отримає cookies

        cookies = page.context.cookies()
        browser.close()
    rozetka_cookies = [
        c for c in cookies if c["domain"].endswith("rozetka.com.ua")
    ]
    cookies_dict = { c["name"]: c["value"] for c in rozetka_cookies }
    return cookies_dict

cookies = get_rozetka_cookies()
print(cookies)
url = "https://xl-catalog-api.rozetka.com.ua/v4/goods/getDetails?country=UA&lang=ua&with_groups=1&with_docket=1&with_extra_info=1&goods_group_href=1&product_ids=354111201,477939314,358532337,234935635,12991699,413068041,387068100,505660054,83374176,429989186,135045840,234908281,277806733,316526614,358521642,93909002,323284093,323271967,53682576,393186270,425511654,131126259,399085038,506294609,506294189,506292129,364609773,234596293,180140570,358539690,417576903,506308029,275080888,383996817,266667191,442859777,395441364,453864368,441843560,506291429,396907284,503392249,316527697,131123333,436709108,504658874,364600170,503384109,484458999,504658919,450999611,437833892,408830295,422630754,381999168,422630745,484456084,9971798,390507354,41520760"
data = fetch_html_rozetka(url=url, cookies=cookies)
print(data)


# data = get_total_pages_rozetka(f"https://xl-catalog-api.rozetka.com.ua/v4/goods/getDetails?country=UA&lang=ua&with_groups=1&with_docket=1&with_extra_info=1&goods_group_href=1&product_ids=354111201,477939314,358532337,234935635,12991699,413068041,387068100,505660054,83374176,429989186,135045840,234908281,277806733,316526614,358521642,93909002,323284093,323271967,53682576,393186270,425511654,131126259,399085038,506294609,506294189,506292129,364609773,234596293,180140570,358539690,417576903,506308029,275080888,383996817,266667191,442859777,395441364,453864368,441843560,506291429,396907284,503392249,316527697,131123333,436709108,504658874,364600170,503384109,484458999,504658919,450999611,437833892,408830295,422630754,381999168,422630745,484456084,9971798,390507354,41520760")
# print(data)