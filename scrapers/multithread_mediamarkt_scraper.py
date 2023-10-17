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

main_sitemap_url = "https://www.mediamarkt.be/sitemaps/fr/sitemap-index.xml"
main_sitemap_soup = get_soup(main_sitemap_url, "xml")

product_sitemaps = [
    url.text for url in main_sitemap_soup.find_all("loc") if "productdetailspages" in url.text
]


product_url = "https://www.mediamarkt.be/fr/product/_isy-protection-d-%C3%A9cran-en-verre-black-frame-iphone-x-xs-11-pro-noir-ipg-5009-2-5d-retail-1876303.html"

def main():
    start_time = time.perf_counter()
    product_urls = get_product_urls_from_xml(product_sitemaps)
    print(f"Found {len(product_urls)} product urls")

    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")


if __name__ == "__main__":
    main()