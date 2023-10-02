import json
from bs4 import BeautifulSoup as bs
import httpx
from tqdm import tqdm
import time

base_url = "https://www.mediamarkt.be"


def get_data(url: str) -> list:
    product_list = []
    current_url = url
    page_count = 0
    max_pages = 100
    with tqdm() as pbar:
        while page_count <= max_pages:
            print("-" * 100)
            print(f"Scraping page {page_count + 1}: {current_url}")
            response = httpx.get(current_url, timeout=90.0)
            soup = bs(response.content, "html.parser")
            divs = soup.find_all(
                "div",
                attrs={
                    "class": "sc-57bbc469-0 hhSaVb sc-5bb8ec6d-3 YFARY sc-b0d9c874-1 bRUDYz"
                },
            )
            for div in divs:
                product = {}
                a_tag = div.find(
                    "a", attrs={"class": "sc-db43135e-1 gpEOUZ sc-b0d9c874-0 gJSJVL"}
                )
                try:
                    product["product_url"] = base_url + a_tag["href"]
                except:
                    product["product_url"] = current_url
                print(product["product_url"])
                try:
                    product["product_name"] = a_tag.text
                except AttributeError:
                    try:
                        product["product_name"] = a_tag.find("p").text
                    except AttributeError:
                        product["product_name"] = "name not available"
                price_div = div.find("div", attrs={"class": "sc-3bd4ad78-0 kQSbne"})
                try:
                    product["product_price"] = price_div.find("span").text.strip()
                except AttributeError:
                    product["product_price"] = "price not available"
                product_list.append(product)
            if not soup.find(
                "button", class_="sc-21f2092b-1 eTQftF sc-2469269c-1 eeiKDF"
            ):
                break
            page_count += 1
            current_url = url + f"?page={page_count + 1}"
            pbar.update(1)
    return product_list


def main():
    start_time = time.perf_counter()
    final_list = []
    with open("categories_links.json", "r") as f:
        categories_links = json.load(f)
    for category_link in categories_links:
        print(f"Scraping {category_link}")
        products = get_data(category_link)
        final_list += products
        print(f"{len(final_list)} products scraped.")
        print("-" * 100)
    with open("products.json", "w") as f:
        json.dump(final_list, f, indent=4)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Scraping completed in {elapsed_time/60:.2f} minutes.")


if __name__ == "__main__":
    main()
