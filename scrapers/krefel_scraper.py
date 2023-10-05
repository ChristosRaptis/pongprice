import json
import requests
from bs4 import BeautifulSoup as bs
import fake_useragent
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm



with open(
    "/home/chris/Becode/Projects/pongprice/data/krefel_product_urls.json", "r"
) as infile:
    product_urls = json.load(infile)

partial_urls = product_urls[:500]



def get_headers():
    user_agent = fake_useragent.UserAgent().random
    headers = {"User-Agent": user_agent}
    return headers


headers = get_headers()


def get_product_data(product_url):
    response = requests.get(product_url, headers= headers, timeout=30)
    print(f"Scraping {product_url}")
    product_data = {}
    soup = bs(response.text, "html.parser")
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
        print("Error")
        product_data["product_name"] = "N/A"
        product_data["product_price"] = "N/A"    
    
    return product_data

def main():
    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=100) as executor:
        product_list = list(tqdm(executor.map(get_product_data, partial_urls), total=len(partial_urls), desc="Scraping Krefel"))
    with open("data/krefel_product_data.json", "w") as outfile:
        json.dump(product_list, outfile, indent=4)
    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")

if __name__ == "__main__":
   main()


    



