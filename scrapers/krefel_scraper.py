import json
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm
from scraper_utils import (
    get_soup,
    get_product_urls_from_xml,
    clean_price,
    update_database,
)

main_sitemap_url = "https://media.krefel.be/sys-master/sitemap/index-fr.xml"
main_sitemap_soup = get_soup(main_sitemap_url, "xml")
# find sitemaps that contain 'product' in the url
product_sitemaps = [
    url.text for url in main_sitemap_soup.find_all("loc") if "product" in url.text
]


def get_product_data(product_url: str):
    """
    Checks if the product is in the database, if yes updates the price, if not adds it to the database
    
    Returns a dictionary containing the product url, name and price from a product url

    Args:
        product_url (str): product url
    Returns:
        dict: dictionary containing the product url, name and price

    """
    product_data = {}
    soup = get_soup(product_url, "html.parser")
    product_data["url"] = product_url
    script = soup.find("script", type="application/json")
    dict = json.loads(script.string)
    try:
        data = dict["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"][
            "data"
        ]
        product_data["product_name"] = data["manufacturer"] + " " + data["name"]
        product_data["product_price"] = data["price"]["value"]
    except:
        print("error getting data")
        product_data["product_name"] = None
        product_data["product_price"] = None

    update_database(product_data)
    return product_data


def main():
    start_time = time.perf_counter()
    product_urls = get_product_urls_from_xml(product_sitemaps)
    print(f"Found {len(product_urls)} product urls")

    with ThreadPoolExecutor(max_workers=3) as executor:
        product_list = list(
            tqdm(
                executor.map(get_product_data, product_urls[:3]),
                total=len(product_urls),
                desc="Scraping Krefel",
            )
        )

    print(product_list)
    print(f"Scraped {len(product_list)} products ")
    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")


if __name__ == "__main__":
    main()
