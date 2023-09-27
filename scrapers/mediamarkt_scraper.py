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
    max_pages = 1000
    with tqdm() as pbar:
        while page_count <= max_pages:
            print(f"Scraping page {page_count + 1}: {current_url}")
            response = httpx.get(current_url, timeout=60.0)
            soup = bs(response.content, "html.parser")
            divs = soup.find_all(
                "div", attrs={"class": "sc-3bd4ad78-0 bGOTBX sc-5bb8ec6d-1 kHWTsV"}
            )
            for div in divs:
                product = {}
                a_tag = div.find("a")
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
                soup.find("button", attrs={"data-test": "mms-search-srp-loadmore"})
                == None
            ):
                break
            page_count += 1
            current_url = url + f"?page={page_count + 1}"
            pbar.update(1)
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
        await consent_button.click()
        # print("Consent button clicked")
        await categories_button.click()
        # print("categories button clicked")
        html = await page.content()
        soup = bs(html, "html.parser")
        aside_tag = soup.find("aside", attrs={"class": "sc-2d009fd-0 dBWZMt"})
        ul_tag = aside_tag.find_next("ul")
        a_tags = ul_tag.find_all("a")
        links = [a["href"] for a in a_tags]
        await browser.close()
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


if __name__ == "__main__":
    asyncio.run(main())
