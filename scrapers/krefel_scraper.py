import re
from urllib import response
from bs4 import BeautifulSoup as bs
import httpx
import asyncio
from tqdm import tqdm
import time

base_url = "https://www.krefel.be"

phones = "https://www.krefel.be/fr/c/A10-B10010-C937/telephonie-et-navigation/smartphones/smartphones"


async def get_data(url: str) -> list:
    product_list = []
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=90.0)
        soup = bs(response.content, "html.parser")
        divs = soup.find_all(
            "div",
            attrs={
                "class": "ProductTileView-styled__StyledProductTileView-sc-2c0dbbbb-0 bAQTWh"
            },
        )
        for div in tqdm(divs, desc="Scraping products"):
            product = {}
            a_tag = div.find(
                "a",
                attrs={
                    "class": "Link-styled__StyledLink-sc-8621feb-0 jQxtVT product-link \
                        ProductTileView-styled__StyledProductTitle-sc-2c0dbbbb-2 gZbckY"
                },
            )
            product["url"] = base_url + a_tag["href"]
            product["product_name"] = a_tag.find("h3").text
            product["product_price"] = div.find(
                "span",
                attrs={
                    "class": "Typography-styled__StyledTypography-sc-890188a7-0 \
                        fBzHDo current-price typography"
                },
            ).text
            product_list.append(product)
            print(f"Added product: {product}")
    print(f"Finished scraping {url}")
    return product_list

async def main():
    product_list = await get_data(phones)
    print(len(product_list))
    print(product_list)        

if __name__ == "__main__":
    asyncio.run(main())