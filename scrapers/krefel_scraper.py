import httpx
from bs4 import BeautifulSoup as bs
import fake_useragent
import asyncio
import json
import time
from tqdm import tqdm
import gc
from fp.fp import FreeProxy

def get_headers():
    user_agent = fake_useragent.UserAgent().random
    headers = {"User-Agent": user_agent}
    return headers


async def get_product_data(product_url:str, client:httpx.AsyncClient, semaphore:asyncio.Semaphore):
    print(f"Scraping {product_url}")
    async with semaphore:
        response = await client.get(product_url, timeout=30)
        print(f"Scraping {product_url}")
        product_data = {}
        soup = bs(response.text, "html.parser")
        
        product_data["url"] = product_url
        script = soup.find('script', type='application/json')
        if script is not None:
            dict = json.loads(script.string)
            data = dict['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']
            product_data["product_name"] = data['manufacturer'] + " " + data['name']
            product_data["product_price"] = data['price']['formattedValue']
        else:
            print("No script found")
            
            product_data["product_name"] = "N/A"
            product_data["product_price"] = "N/A"
        return product_data







async def main():
    start_time = time.perf_counter()
    # Create a semaphore to limit the number of concurrent requests
    semaphore = asyncio.Semaphore(50)
    # Load the list of product URLs
    with open("/home/chris/Becode/Projects/pongprice/data/krefel_product_urls.json", "r") as infile:
        product_urls = json.load(infile)
    print(f"{len(product_urls)} product urls to scrape")
    # Split the list of product URLs into partitions of 5000
    main_partitions = [
        product_urls[i : i + 5000] for i in range(0, len(product_urls), 5000)
    ]
    print(f"{len(main_partitions)} main partitions of urls")
    # Process each partition of product URLs separately
    total_scraped = 0
    for partition in main_partitions[0]:
        headers = get_headers()
        # Split the partition into sub partitions of 500
        sub_partitions = [
            partition[i : i + 500] for i in range(0, len(partition), 500)
        ]
        print(f"{len(sub_partitions)} sub partitions of urls for each main partition")
        product_data = []
        with tqdm() as pbar:
            # Process each sub partition of product URLs concurrently
            for sub_partition in sub_partitions[:2]:
                async with httpx.AsyncClient(headers= headers, timeout=30) as client:
                    url_tasks = [asyncio.create_task(get_product_data(url,client, semaphore)) for url in sub_partition]
                    sub_partition_data = await asyncio.gather(*url_tasks)
                    product_data.extend(sub_partition_data)
                    print(f"{len(product_data)} products scraped for current partition.")
                    pbar.update(1)
        with open("data/krefel_product_data.json", "a") as outfile:
            json.dump(product_data, outfile, indent=4)
        total_scraped += len(product_data) 
        print(f"{total_scraped} products scraped.")   
        del product_data    
        gc.collect()
    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")


if __name__ == "__main__":
    asyncio.run(main())
