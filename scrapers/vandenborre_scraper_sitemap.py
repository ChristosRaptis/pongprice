import json
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm
from scraper_utils import (
    get_soup,
    get_product_urls_from_xml,
    clean_price,
    get_db_connection,
    update_database,
    dump_json,
    open_json,
)

main_sitemap_url = "https://www.vandenborre.be/web/productcatalog.xml"
main_sitemap_soup = get_soup(main_sitemap_url, "xml")

# find sitemaps that contain 'smartphone' or 'laptop' in the url
product_sitemaps = [
    url.text
    for url in main_sitemap_soup.find_all("loc")
    if "/smartphone" in url.text or "/laptop" in url.text
]

# quick way to delete duplicates
product_sitemaps = list(set(product_sitemaps))

dump_json(product_sitemaps, "data/vandenborre_urls_sitemap.json")


def get_product_data(product_url: str, conn):
    """
    Returns a dictionary containing the product url, name and price from a product url

    Args:
        product_url (str): product url
    Returns:
        dict: dictionary containing the product url, name and price

    """
    print(f"Scraping {product_url}")
    product_data = {}

    soup = get_soup(product_url, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        data = json.loads(script.string)
        if "offers" in data:
            # Process the data as needed
            try:
                product_data["url"] = product_url
                product_data["product_name"] = data["name"]
                product_data["product_price"] = clean_price(data["offers"]["price"])
            except:
                print("error getting data")
                pass
    
    # verifies if product_data not empty
    if bool(product_data):
        cur = conn.cursor()
        update_database(product_data, cur)
        conn.commit()
        cur.close()

    return product_data


def main():
    start_time = time.perf_counter()
    print(f"Found {len(product_sitemaps)} product urls")

    conn = get_db_connection()

    with ThreadPoolExecutor(max_workers=3) as executor:
        product_list = list(
            tqdm(
                executor.map(
                    get_product_data, product_sitemaps, [conn] * len(product_sitemaps)
                ),
                total=len(product_sitemaps),
                desc="Scraping Vandenborre",
            )
        )

    conn.close()

    dump_json(product_list, "data/vandenborre_product_data.json")
    # print(product_list)
    print(f"Scraped {len(product_list)} products ")
    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")


if __name__ == "__main__":
    main()
