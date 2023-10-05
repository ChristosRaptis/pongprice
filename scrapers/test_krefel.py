import json
from bs4 import BeautifulSoup as bs
import fake_useragent
import asyncio
import httpx
import time
from tqdm import tqdm
import pypeln as pl


with open(
    "/home/chris/Becode/Projects/pongprice/data/krefel_product_urls.json", "r"
) as infile:
    product_urls = json.load(infile)

partial_urls = product_urls[:10]
print(partial_urls)


def get_headers():
    user_agent = fake_useragent.UserAgent().random
    headers = {"User-Agent": user_agent}
    return headers


headers = get_headers()


async def get_product_data(product_url):
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(product_url, timeout=30)
        print(f"Scraping {product_url}")
        product_data = {}
        soup = bs(response.text, "html.parser")
        product_data["url"] = product_url
        script = soup.find("script", type="application/json")
        if script is not None:
            dict = json.loads(script.string)
            data = dict["props"]["pageProps"]["dehydratedState"]["queries"][0][
                "state"
            ]["data"]
            product_data["product_name"] = data["manufacturer"] + " " + data["name"]
            product_data["product_price"] = data["price"]["formattedValue"]
        else:
            print("No script found")
            product_data["product_name"] = "N/A"
            product_data["product_price"] = "N/A"
        return product_data

async def main():
    start_time = time.perf_counter()

    # Create a pipeline with a generator that yields the URLs
    pipeline = pl.task.each(get_product_data, partial_urls)

    # Run the pipeline with 3 workers and a buffer size of 4
    product_list = await pl.task.list(pipeline, workers=3, maxsize=4)
    print(product_list)
    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")

if __name__ == "__main__":
    asyncio.run(main())


    



