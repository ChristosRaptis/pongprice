<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 9e9b930 (renamed file)
import json
import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm


<<<<<<< HEAD
=======

with open(
    "/home/chris/Becode/Projects/pongprice/data/krefel_product_urls.json", "r"
) as infile:
    product_urls = json.load(infile)

partial_urls = product_urls[:500]



>>>>>>> 9e9b930 (renamed file)
def get_headers():
    user_agent = fake_useragent.UserAgent().random
    headers = {"User-Agent": user_agent}
    return headers

<<<<<<< HEAD
product_sitemaps = [
    f"https://media.krefel.be/sys-master/sitemap/product-fr-{n}.xml"
    for n in range(0, 20)
]

def get_product_urls(sitemap_url):
    headers= get_headers()
    response = requests.get(sitemap_url, headers=headers)
    soup = bs(response.text, "xml")
    urls = [url.text for url in soup.find_all("loc")]
    return urls

def get_product_data(product_url):
    print(f"Scraping {product_url}")
    headers = get_headers()
    try:
        response = requests.get(product_url, headers=headers, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        print(f"Retrying {product_url}")
        return {}

    product_data = {}
    try:
        soup = bs(response.text, "html.parser")
    except Exception as e:
        print(f"Error occurred: {e}")
        print(f"Retrying {product_url}")
        return {}

    product_data["url"] = product_url
    script = soup.find("script", type="application/json")

=======

headers = get_headers()


def get_product_data(product_url):
    response = requests.get(product_url, headers= headers, timeout=30)
    print(f"Scraping {product_url}")
    product_data = {}
    soup = bs(response.text, "html.parser")
    product_data["url"] = product_url
    script = soup.find("script", type="application/json")
   
>>>>>>> 9e9b930 (renamed file)
    dict = json.loads(script.string)
    try:
        data = dict["props"]["pageProps"]["dehydratedState"]["queries"][0][
            "state"
        ]["data"]
        product_data["product_name"] = data["manufacturer"] + " " + data["name"]
        product_data["product_price"] = data["price"]["formattedValue"]
    except:
<<<<<<< HEAD
        print("error getting data")
        product_data["product_name"] = "N/A"
        product_data["product_price"] = "N/A"

=======
        print("Error")
        product_data["product_name"] = "N/A"
        product_data["product_price"] = "N/A"    
    
>>>>>>> 9e9b930 (renamed file)
    return product_data

def main():
    start_time = time.perf_counter()
<<<<<<< HEAD
    product_urls = [get_product_urls(sitemap) for sitemap in product_sitemaps]
    product_urls = [
        url for sublist in product_urls for url in sublist
    ]
    with ThreadPoolExecutor(max_workers=3) as executor:
        product_list = list(tqdm(executor.map(get_product_data, product_urls[:10]), total=len(product_urls), desc="Scraping Krefel"))
    # with open("data/krefel_product_data.json", "w") as outfile:
    #     json.dump(product_list, outfile, indent=4)
    print(f"Scraped {len(product_list)} products ")   
=======

    with ThreadPoolExecutor(max_workers=100) as executor:
        product_list = list(tqdm(executor.map(get_product_data, partial_urls), total=len(partial_urls), desc="Scraping Krefel"))
    with open("data/krefel_product_data.json", "w") as outfile:
        json.dump(product_list, outfile, indent=4)
>>>>>>> 9e9b930 (renamed file)
    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")

if __name__ == "__main__":
   main()


    



<<<<<<< HEAD
=======
import re
from urllib import response
from bs4 import BeautifulSoup as bs
=======
>>>>>>> 6cce8ab (stil lworking on krefel)
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
<<<<<<< HEAD
>>>>>>> 715254c (attempting to scrape Krefel)
=======
>>>>>>> 6cce8ab (stil lworking on krefel)
=======
>>>>>>> 9e9b930 (renamed file)
