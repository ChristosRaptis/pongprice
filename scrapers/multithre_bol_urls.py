import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
)
import time
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

beggining = time.perf_counter()
session = requests.Session()


def scrape_bol(url):
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        page_source = driver.get(url)
        page_source

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

    finally:
        driver.quit()


def main():
    session = requests.Session()
    driver = webdriver.Chrome()
    with open("bol/bol_urls.json", "r") as file:
        bol_urls = json.load(file)

    list_products = []

    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(
            tqdm(
                pool.map(scrape_bol, bol_urls), desc="Scraping Bol", total=len(bol_urls)
            )
        )
        list_products.extend(results)
        print(list_products)

    with open("bol_products_6.json", "w") as outfile:
        json.dump(list_products, outfile)


if __name__ == "__main__":
    main()


end = time.perf_counter()

print(f"Time it takes : {end-beggining}")
