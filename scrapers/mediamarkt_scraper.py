<<<<<<< HEAD
import json
from bs4 import BeautifulSoup as bs
from playwright.async_api import async_playwright
import httpx
from tqdm import tqdm
import time
import asyncio
from dotenv import load_dotenv

base_url = "https://www.mediamarkt.be"

multimedia_url = (
    "https://www.mediamarkt.be/fr/category/_ordinateur-multim%C3%A9dia-452669.html"
)

phone_url = (
    "https://www.mediamarkt.be/fr/category/_t%C3%A9l%C3%A9phone-navigation-509451.html"
)

async def get_main_links(url: str) -> list:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        consent_button = page.locator("#pwa-consent-layer-accept-all-button")
        categories_button = page.locator(
            "#acc-content-id-facet-Catégorie > ul > div > button"
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
        categories = [li.find("a") for li in li_tags]
        category_links = []
        for category in tqdm(categories):
            first_url = base_url + category["href"]
            print(first_url)
            response = await page.goto(first_url)
            final_url = response.url
            print(final_url)    
            category_links.append(final_url)
        await browser.close()
    return category_links

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
    multimedia_links = await get_main_links(multimedia_url)
    phone_links = await get_main_links(phone_url)
    categories_links = multimedia_links + phone_links
    print(len(categories_links))
    # final_list = []
    # with open("data/categories_links.json", "r") as f:
    #     categories_links = json.load(f)
    # tasks = []
    # for category_link in categories_links[0]:
    #     print(f"Scraping {category_link}")
    #     task = asyncio.create_task(get_data(category_link))
    #     tasks.append(task)
    # products_list = await asyncio.gather(*tasks)
    # for products in products_list:
    #     final_list += products
    #     print(f"{len(final_list)} products scraped.")
    #     print("-" * 100)
    # with open("data/mediamarkt_products.json", "w") as f:
    #     json.dump(final_list, f, indent=4)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Scraping completed in {elapsed_time/60:.2f} minutes.")

=======
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as bs

multimedia_url = (
    "https://www.mediamarkt.be/fr/category/_ordinateur-multim%C3%A9dia-452669.html"
)

ul_selector = "#floating-ui-5 > ul"
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        consent_button = page.locator("#pwa-consent-layer-accept-all-button")
        categories_button = page.locator("#main-content > div.sc-dbb4f5b6-0.dMPtoe >\
                                        div.sc-490debc5-0.jhMMyN > div.sc-835d3f28-0.kTdeVZ > aside > div:nth-child(1) > aside > div > button") 
        await page.goto(multimedia_url) 
        await consent_button.click()
        print("Consent button clicked")
        await categories_button.click()
        print("categories button clicked")
        html = await page.content()
        soup = bs(html, "html.parser")
        categories
        categories = soup.find_all("a", attrs={"class": "sc-db43135e-0 bjnEhE"})
        print(type(categories))
        links = [a["href"] for a in categories]
        print(links)
        print(len(links))
        await browser.close()
>>>>>>> 437a1b2 (progress)


if __name__ == "__main__":
    asyncio.run(main())
