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
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

beggining = time.perf_counter()

with open("urls&maxpage.json", "r") as file:
    urls_maxpage = json.load(file)

driver = webdriver.Chrome()


def scrape_bol(url):
    try:
        time.sleep(5)

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
            # print(paragraph)
            product_info = {}
            product = paragraph.find("div", class_="product-title--inline")

            if product:
                product_info["product_name"] = product.text.strip()
                product_info[
                    "url"
                ] = f'https://www.bol.com{paragraph.find("a", class_="product-title px_list_page_product_click list_page_product_tracking_target")["href"]}'

            product_price = paragraph.find("span", class_="promo-price")

            if product_price:
                product_info["product_price"] = product_price.text.strip()
            time.sleep(3)

            product_info_list.append(product_info)

        return product_info_list

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")


product_info_list = []


def get_products(urls_maxpage):
    for list_json in urls_maxpage:
        for i in range(1, list_json[1] - 1):
            url = list_json[0]
            page_source = driver.get(url)
            page_source
            time.sleep(5)
            try:
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
                    # print(paragraph)
                    product_info = {}
                    product = paragraph.find("div", class_="product-title--inline")

                    if product:
                        product_info["product_name"] = product.text.strip()
                        product_info[
                            "url"
                        ] = f'https://www.bol.com{paragraph.find("a", class_="product-title px_list_page_product_click list_page_product_tracking_target")["href"]}'

                    product_price = paragraph.find("span", class_="promo-price")

                    if product_price:
                        product_info["product_price"] = product_price.text.strip()
                    time.sleep(3)

                    product_info_list.append(product_info)

            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")

            button_next = driver.find_element(
                By.XPATH,
                '//*[@id="js_pagination_control"]/ul/li[8]/a',
            )
            if button_next.is_displayed():
                button_next.click()
            time.sleep(2)
    driver.quit()
    return product_info_list


results = get_products(urls_maxpage[4:6])
# with ThreadPoolExecutor(max_workers=2) as pool:
#     results = list(
#         tqdm(
#             pool.map(get_products, urls_maxpage[4:6]),
#             desc="Scraping Bol",
#             total=(len(urls_maxpage)),
#         )
#     )

with open("bol_products.json", "w") as outfile:
    json.dump(results, outfile)

end = time.perf_counter()

print(f"Got the products in {end - beggining:0.4f} seconds")
