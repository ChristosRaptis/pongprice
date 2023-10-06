import json
import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm


def get_headers():
    user_agent = fake_useragent.UserAgent().random
    headers = {"User-Agent": user_agent}
    return headers

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

    dict = json.loads(script.string)
    try:
        data = dict["props"]["pageProps"]["dehydratedState"]["queries"][0][
            "state"
        ]["data"]
        product_data["product_name"] = data["manufacturer"] + " " + data["name"]
        product_data["product_price"] = data["price"]["formattedValue"]
    except:
        print("error getting data")
        product_data["product_name"] = "N/A"
        product_data["product_price"] = "N/A"

    return product_data

def main():
    start_time = time.perf_counter()
    product_urls = [get_product_urls(sitemap) for sitemap in product_sitemaps]
    product_urls = [
        url for sublist in product_urls for url in sublist
    ]
    with ThreadPoolExecutor(max_workers=3) as executor:
        product_list = list(tqdm(executor.map(get_product_data, product_urls[:10]), total=len(product_urls), desc="Scraping Krefel"))
    # with open("data/krefel_product_data.json", "w") as outfile:
    #     json.dump(product_list, outfile, indent=4)
    print(f"Scraped {len(product_list)} products ")   
    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")

if __name__ == "__main__":
   main()


    



