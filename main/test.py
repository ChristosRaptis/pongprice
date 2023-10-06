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


with open("list_urls_bol.json", "r") as file:
    list_urls_bol = json.load(file)

driver = webdriver.Chrome()
product_info_list = []

url = "https://www.bol.com/be/fr/l/laptops/4770/?promo=software_360__A_34232-34233-Laptops-0_0_"
page_source = driver.get(url)
page_source

try:
    button_cookies = driver.find_element(By.XPATH, '//*[@id="js-reject-all-button"]')
    if button_cookies.is_displayed():
        button_cookies.click()
        time.sleep(5)

    button_cookies = driver.find_element(
        By.XPATH,
        '//*[@id="modalWindow"]/div[2]/div[2]/wsp-country-language-modal/button',
    )
    if button_cookies.is_displayed():
        button_cookies.click()
        time.sleep(5)

except NoSuchElementException:
    pass

time.sleep(5)

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
paragraphs = soup.find_all("div", class_="product-item__content")

for paragraph in paragraphs:
    product_info = {}
    product = paragraph.find("div", class_="product-title--inline")
    if product:
        product_info[
            "url"
        ] = f"https://www.bol.com{paragraph.find('a', class_='product-title px_list_page_product_click list_page_product_tracking_target')['href']}"
        product_info["product_name"] = product.text.strip()

    product_price = paragraph.find(
        "span", class_="promo-price"
    )  # Use paragraph instead of soup

    if product_price:
        product_info["product_price"] = product_price.text.strip()
    time.sleep(3)
    product_info_list.append(product_info)
    time.sleep(3)

print(product_info_list)
