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
    get_product_data,
)

main_sitemap_url = "https://www.vandenborre.be/web/productcatalog.xml"
main_sitemap_soup = get_soup(main_sitemap_url, "xml")

# find sitemaps that contain 'smartphone' or 'laptop' in the url
product_sitemaps = [
    url.text
    for url in main_sitemap_soup.find_all("loc")
    if "/smartphone" in url.text or "/laptop" in url.text or "/multimedia" in url.text
]

# quick way to delete duplicates
product_sitemaps = list(set(product_sitemaps))

dump_json(product_sitemaps, "data/vandenborre_urls_sitemap.json")


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
