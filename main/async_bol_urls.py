import asyncio
import aiohttp
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
from fake_useragent import UserAgent
import random

random.seed(10)


ua = UserAgent()
headers = {"User-Agent": ua.random}

beggining = time.perf_counter()


async def fetch_max_pages(session, url):
    async with session.get(url, headers=headers) as response:
        page_source = await response.text()
    soup = BeautifulSoup(page_source, "html.parser")
    page_number_elements = soup.find_all("a", class_="js_pagination_item")[-1]
    max_page_number = None

    for page_element in page_number_elements:
        page_text = page_element.get_text(strip=True)
        if page_text.isdigit():
            max_page_number = int(page_text)
            break  # Break out of the loop once you find the max page number

    return url, max_page_number


async def scrape_bol(session, url, driver):
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            print(f"Request failed with status code: {response.status}")
        page_source = await response.text()

    await asyncio.sleep(5)

    try:
        button_cookies = driver.find_element(
            By.XPATH, '//*[@id="js-reject-all-button"]'
        )
        if button_cookies.is_displayed():
            button_cookies.click()
            await asyncio.sleep(5)

        button_cookies_2 = driver.find_element(
            By.XPATH,
            '//*[@id="modalWindow"]/div[2]/div[2]/wsp-country-language-modal/button',
        )

        if button_cookies_2.is_displayed():
            button_cookies_2.click()
            await asyncio.sleep(5)

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

        print(product_info)
        product_info_list.append(product_info)

    return product_info_list


async def main():
    ua = UserAgent()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-agent={ua.random}")

    with open("list_urls_bol.json", "r") as file:
        list_urls_bol = json.load(file)

    list_urls_bol_reworked = []
    options = Options()
    options.headless = True  # Run Chrome in headless mode
    web_driver = webdriver.Chrome(options=chrome_options)

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

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_max_pages(session, url) for url in list_urls_bol_reworked]
        url_and_max_page = await asyncio.gather(*tasks)

    product_list_bol = []

    for url, max_pages in url_and_max_page:
        async with aiohttp.ClientSession() as session:  # Create a new session for each URL
            scraped_url = await scrape_bol(session, url, web_driver)
            print(scraped_url)
        product_list_bol.extend(scraped_url)  # Use append to add each product list

        if max_pages is None:
            print(url)
        else:
            for page_number in range(2, max_pages + 1):
                new_url = f"{url}/?page={page_number}"
                print(new_url)
                async with aiohttp.ClientSession() as session:  # Create a new session for each URL
                    scraped_url = await scrape_bol(session, new_url, web_driver)
                    print(scraped_url)
                product_list_bol.extend(scraped_url)  # Use append here as well

    # Flatten the nested list
    flat_product_list = [item for sublist in product_list_bol for item in sublist]

    with open("bol_products_2.json", "w") as outfile:
        json.dump(flat_product_list, outfile)  # Dump the flat list to JSON


if __name__ == "__main__":
    asyncio.run(main())
