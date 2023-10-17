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

def get_product_data(product_url: str):
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
    scripts = soup.find_all("script", attrs={'type':'application/ld+json'})
    
    for script in scripts:
        data = json.loads(script.string)
        if "object" in data.keys():
            
            # Process the data as needed
            try:
                product_data["url"] = product_url
                product_data["product_name"] = data["object"]["name"]
                product_data["product_price"] = data["object"]["offers"]["price"]
                
            except:
                print("error getting data")
                pass

    # verifies if product_data not empty
    if bool(product_data):
        
        update_database(product_data)
        
    return product_data

def main():
    start_time = time.perf_counter()
    product_urls = get_product_urls_from_xml(product_sitemaps)
    print(f"Found {len(product_urls)} product urls")

    with ThreadPoolExecutor(max_workers=3) as executor:
        product_list = list(
            tqdm(
                executor.map(get_product_data, product_urls[:2]),
                total=len(product_urls),
                desc="Scraping Krefel",
            )
        )
    
    print(f"Scraped {len(product_list)} products ")
    end_time = time.perf_counter()
    print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")


if __name__ == "__main__":
    main()