import asyncio
import json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup as bs
from tqdm import tqdm


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

async def main():
    multimedia_links = await get_main_links(multimedia_url)
    phone_links = await get_main_links(phone_url)
    all_categories_links = multimedia_links + phone_links
    print(len(all_categories_links))
    with open("categories_links.json", "w") as f:
        json.dump(all_categories_links, f)
    


if __name__ == "__main__":
    asyncio.run(main())
