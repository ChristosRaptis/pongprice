import requests
from bs4 import BeautifulSoup
import json
from vandenborre_urls_scraper import getting_urls
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
import pandas as pd
import time

beggining = time.perf_counter()

with open("list_urls_multim_teleph.json", "r") as file:
    list_urls_multim_teleph = json.load(file)

driver = webdriver.Chrome()
product_info_list = []

for url in list_urls_multim_teleph:
    page_source = driver.get(url)
    page_source
    time.sleep(5)

    try:
        button_cookies = driver.find_element(
            By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'
        )
        if button_cookies.is_displayed():
            button_cookies.click()
            time.sleep(5)

    except NoSuchElementException:
        pass

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    try:
        button_existence = soup.find("li", class_="custom-select-option")
        if button_existence:
            button_more_products = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "body > div.container.bg-white.product-list-page > div.js-prodlist-full-template > div.row.js-prodlist-pagination > div > div.col-md-3.hidden-xs.hidden-sm > div > div > div > div > div",
                    )
                )
            )
            button_more_products.click()

            time.sleep(5)

            button_all_products = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "body > div.container.bg-white.product-list-page > div.js-prodlist-full-template > div.row.js-prodlist-pagination > div > div.col-md-3.hidden-xs.hidden-sm > div > div > div > div > ul > li:nth-child(4)",
                    )
                )
            )
            button_all_products.click()

            time.sleep(10)

    except ElementNotInteractableException:
        # Handle the case where the button is not interactable or doesn't exist
        print(f"Button not found or not interactable on URL: {url}")

    # Scrape product information directly using Selenium

    paragraphs = soup.find_all(
        "div",
        class_="col-md-4 col-sm-4 col-xs-12 js-product-container product-container js-gtm-product-container margin-top-10-md margin-btm-10-md",
    )

    for paragraph in paragraphs:
        product_info = {}

        product_name = paragraph.find(
            "h2", class_="productname uppercase js-ellipsis js-ellipsis-productlist"
        )
        if product_name:
            product_info[
                "url"
            ] = f"https:{paragraph.find('a', class_='js-product-click')['href']}"
            product_info["product_name"] = product_name.text.strip()

        product_price = paragraph.find("div", class_="price js-gtm-price")

        if product_price:
            product_info["product_price"] = product_price.find(
                "span", class_="current"
            ).text.strip()

        product_info_list.append(product_info)

df_products_vandeborre = pd.DataFrame(product_info_list)
df_products_vandeborre.to_csv("df_products_vandeborre_V5.csv")

driver.quit()

end = time.perf_counter()

print(f"Got the products in {end - beggining:0.4f} seconds")
