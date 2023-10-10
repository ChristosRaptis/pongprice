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

session = requests.Session()
url_and_max_page = []

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


for url in list_urls_bol_reworked:
    page_source = session.get(url).text
    soup = BeautifulSoup(page_source, "html.parser")
    page_number_elements = soup.find_all("a", class_="js_pagination_item")[-1]
    max_page_number = None

    for page_element in page_number_elements:
        page_text = page_element.get_text(strip=True)
        if page_text.isdigit():
            max_page_number = int(page_text)
            break  # Break out of the loop once you find the max page number

    url_and_max_page.append((url, max_page_number))

list_urls_bol = []

for url, max_pages in url_and_max_page:
    list_urls_bol.append(url)
    if max_pages is None:
        print(url)
    else:
        for _ in range(2, max_pages + 1):
            new_url = f"{url}/?page={_}"
            list_urls_bol.append(new_url)

with open("bol_urls.json", "w") as outfile:
    json.dump(list_urls_bol, outfile)
