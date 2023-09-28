<<<<<<< HEAD
import json
from bs4 import BeautifulSoup as bs
import httpx
from tqdm import tqdm
import time

base_url = "https://www.mediamarkt.be"


import asyncio

async def get_data(url: str) -> list:
    product_list = []
    current_url = url
    page_count = 0
    max_pages = 100
    async with httpx.AsyncClient() as client:
        with tqdm() as pbar:
            while page_count <= max_pages:
                print("-" * 100)
                print(f"Scraping page {page_count + 1}: {current_url}")
                response = await client.get(current_url, timeout=90.0)
                soup = bs(response.content, "html.parser")
                divs = soup.find_all(
                    "div",
                    attrs={
                        "class": "sc-57bbc469-0 hhSaVb sc-5bb8ec6d-3 YFARY sc-b0d9c874-1 bRUDYz"
                    },
                )
                for div in divs:
                    product = {}
                    a_tag = div.find(
                        "a", attrs={"class": "sc-db43135e-1 gpEOUZ sc-b0d9c874-0 gJSJVL"}
                    )
                    try:
                        product["product_url"] = base_url + a_tag["href"]
                    except:
                        product["product_url"] = current_url
                    print(product["product_url"])
                    try:
                        product["product_name"] = a_tag.text
                    except AttributeError:
                        try:
                            product["product_name"] = a_tag.find("p").text
                        except AttributeError:
                            product["product_name"] = "name not available"
                    price_div = div.find("div", attrs={"class": "sc-3bd4ad78-0 kQSbne"})
                    try:
                        product["product_price"] = price_div.find("span").text.strip()
                    except AttributeError:
                        product["product_price"] = "price not available"
                    product_list.append(product)
                if not soup.find(
                    "button", class_="sc-21f2092b-1 eTQftF sc-2469269c-1 eeiKDF"
                ):
                    break
                page_count += 1
                current_url = url + f"?page={page_count + 1}"
                pbar.update(1)
    return product_list


async def main():
    start_time = time.perf_counter()
    final_list = []
    with open("data/categories_links.json", "r") as f:
        categories_links = json.load(f)
    tasks = []
    for category_link in categories_links:
        print(f"Scraping {category_link}")
        task = asyncio.create_task(get_data(category_link))
        tasks.append(task)
    products_list = await asyncio.gather(*tasks)
    for products in products_list:
        final_list += products
        print(f"{len(final_list)} products scraped.")
        print("-" * 100)
    with open("data/products.json", "w") as f:
        json.dump(final_list, f, indent=4)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Scraping completed in {elapsed_time/60:.2f} minutes.")

=======
import asyncio
from urllib import response
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as bs
import httpx
from tqdm import tqdm
import time

base_url = "https://www.mediamarkt.be"

multimedia_url = (
    "https://www.mediamarkt.be/fr/category/_ordinateur-multim%C3%A9dia-452669.html"
)

phone_url = (
    "https://www.mediamarkt.be/fr/category/_t%C3%A9l%C3%A9phone-navigation-509451.html"
)

category_url = "https://www.mediamarkt.be/fr/category/_gsm-smartphone-509452.html"


async def get_data(url: str) -> list:
    product_list = []
    current_url = url
    page_count = 0
    max_pages = 2
    async with httpx.AsyncClient() as client:
        with tqdm() as pbar:
            while page_count <= max_pages:
                print(f"Scraping page {page_count + 1}: {current_url}")
                response = await client.get(current_url, timeout=60.0)
                soup = bs(response.content, "html.parser")
                divs = soup.find_all(
                    "div", attrs={"class": "sc-57bbc469-0 hhSaVb sc-5bb8ec6d-3 YFARY sc-b0d9c874-1 bRUDYz"}
                )
                for div in divs:
                    product = {}
                    a_tag = div.find("a", attrs={"class": "sc-db43135e-1 gpEOUZ sc-b0d9c874-0 gJSJVL"})
                    try:
                        product["product_url"] = base_url + a_tag["href"]
                    except:
                        product["product_url"] = "url not available"
                    product["product_name"] = a_tag.text
                    price_div = div.find("div", attrs={"class": "sc-3bd4ad78-0 kQSbne"})
                    product["product_price"] = price_div.find("span").text
                    product_list.append(product)
                print(len(product_list))
                if (
                    soup.find(
                        "button",
                        attrs={"class": "sc-21f2092b-1 eTQftF sc-2469269c-1 eeiKDF"},
                    )
                    == None
                ):
                    break
                page_count += 1
                current_url = url + f"?page={page_count + 1}"
                pbar.update(1)
                await asyncio.sleep(1)  # Wait for 1 second between page requests
    return product_list


async def get_main_links(url: str) -> list:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        consent_button = page.locator("#pwa-consent-layer-accept-all-button")
        categories_button = page.locator(
            "#main-content > div.sc-dbb4f5b6-0.dMPtoe >\
                                        div.sc-490debc5-0.jhMMyN > div.sc-835d3f28-0.kTdeVZ > aside > div:nth-child(1) > aside > div > button"
        )
        await page.goto(url)
        try:
            await consent_button.click(timeout=5000)
        except:
            pass
        # print("Consent button clicked")
        try:
            await categories_button.click(timeout=5000)
        except:
            pass
        # print("categories button clicked")
        html = await page.content()
        soup = bs(html, "html.parser")
        li_tags = soup.find_all("li", attrs={"class": "sc-f741f313-2 kTVmzt"})
        a_tags = [li.find("a") for li in li_tags]
        links = [base_url + a["href"] for a in a_tags]
        await browser.close()
<<<<<<< HEAD
>>>>>>> 437a1b2 (progress)
=======
        return links


async def main():
    start_time = time.perf_counter()
    final_list = []
    multimedia_links = await get_main_links(multimedia_url)
    phone_links = await get_main_links(phone_url)
    all_categories_links = multimedia_links + phone_links
    for category_link in all_categories_links:
        products = await get_data(category_link)
        final_list += products
        print(f"{len(final_list)} products scraped.")
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Scraping completed in {elapsed_time:.2f} seconds.")
>>>>>>> 9fc7d17 (up and running, probably)


if __name__ == "__main__":
    asyncio.run(main())
