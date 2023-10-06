import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
import pandas as pd
import time

beggining = time.perf_counter()
session = requests.Session()

with open("list_urls_bol.json", "r") as file:
    list_urls_bol = json.load(file)


list_urls_bol_reworked = []

for url in list_urls_bol:
    url_split = url.split("/")[:-1]
    url_reworked = "/".join([str(url) for url in url_split])
    list_urls_bol_reworked.append(url_reworked)

list_urls_bol_reworked

drop_list = [
    "https://www.bol.com/be/fr/m/pc-accessoires",
    "https://www.bol.com/be/fr/m/netwerkinternet",
    "https://www.bol.com/be/fr/m/pc-accessoires-tassen-opbergsystemen",
    "https://www.bol.com/be/fr/m/alles-voor-de-pc-gamer",
    "https://www.bol.com/be/fr/m/pc-accessoires-dataopslag",
    "https://www.bol.com/be/fr/sf/storage",
    "https://www.bol.com/be/fr/sf/laptoptassen",
]

for url in drop_list:
    if url in list_urls_bol_reworked:
        list_urls_bol_reworked.remove(url)

list_urls_bol_reworked = list_urls_bol_reworked[4:5]

driver = webdriver.Chrome()


def scrape_bol(url):
    page_source = driver.get(url)
    page_source

    time.sleep(3)

    try:
        button_cookies = driver.find_element(
            By.XPATH, '//*[@id="js-reject-all-button"]'
        )
        if button_cookies.is_displayed():
            button_cookies.click()
            time.sleep(5)

        button_cookies_2 = driver.find_element(
            By.XPATH,
            '//*[@id="modalWindow"]/div[2]/div[2]/wsp-country-language-modal/button',
        )

        if button_cookies_2.is_displayed():
            button_cookies_2.click()
            time.sleep(5)

    except NoSuchElementException:
        pass

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    paragraphs = soup.find_all("div", class_="product-item__content")
    product_info_list = []

    for paragraph in paragraphs:
        product_info = {}
        product = paragraph.find("div", class_="product-title--inline")
        if product:
            product_info["product_name"] = product.text.strip()
            # if "href" in product.attrs:
            product_info[
                "url"
            ] = f'https://www.bol.com{paragraph.find("a",class_="product-title px_list_page_product_click list_page_product_tracking_target")["href"]}'
            # else:
            #     product_info["url"] = "NA"

        product_price = paragraph.find(
            "span", class_="promo-price"
        )  # Use paragraph instead of soup

        if product_price:
            product_info["product_price"] = product_price.text.strip()
        time.sleep(3)

        product_info_list.append(product_info)

    return product_info_list


# session = requests.Session()
# url_and_max_page = []

# for url in list_urls_bol_reworked:
#     page_source = session.get(url).text
#     soup = BeautifulSoup(page_source, "html.parser")
#     page_number_elements = soup.find_all("a", class_="js_pagination_item")[-1]
#     max_page_number = None

#     for page_element in page_number_elements:
#         page_text = page_element.get_text(strip=True)
#         if page_text.isdigit():
#             max_page_number = int(page_text)
#             break  # Break out of the loop once you find the max page number

#     url_and_max_page.append((url, max_page_number))

# product_list_bol = []

# for url, max_pages in url_and_max_page:
#     scraped_url = scrape_bol(url)
#     product_list_bol.append(scraped_url)

#     if max_pages is None:
#         print(url)

#     else:
#         for _ in range(2, max_pages + 1):
#             new_url = f"{url}/?page={_}"
            print(new_url)
            scraped_url = scrape_bol(url)
            product_list_bol.append(scraped_url)


with open("bol_products_4.json", "w") as outfile:
    json.dump(product_list_bol, outfile)


end = time.perf_counter()

print(f"Time it takes : {end-beggining}")
