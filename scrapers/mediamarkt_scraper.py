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


if __name__ == "__main__":
    asyncio.run(main())
