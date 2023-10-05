import httpx
from bs4 import BeautifulSoup as bs
import fake_useragent
import asyncio
import json
import time

user_agent = fake_useragent.UserAgent().random
headers = {"User-Agent": user_agent}

product_sitemaps = [
    f"https://media.krefel.be/sys-master/sitemap/product-fr-{n}.xml"
    for n in range(0, 20)
]


async def get_product_urls(sitemap_url):
    response = httpx.get(sitemap_url, headers=headers)
    soup = bs(response.text, "xml")
    urls = [url.text for url in soup.find_all("loc")]
    return urls

async def main():
    start_time = time.perf_counter()
    url_tasks = [get_product_urls(sitemap) for sitemap in product_sitemaps]
    product_urls = await asyncio.gather(*url_tasks)
    product_urls = [
        url for sublist in product_urls for url in sublist
    ]  # flatten the list of lists
    print(f"Found {len(product_urls)} product urls")
    with open("data/krefel_product_urls.json", "w") as outfile:
        json.dump(product_urls, outfile)
    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")

if __name__ == "__main__":
    asyncio.run(main())    