from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import time
import json

base_url = "https://www.mediamarkt.be"

multimedia_url = (
    "https://www.mediamarkt.be/fr/category/_ordinateur-multim%C3%A9dia-452669.html"
)

phone_url = (
    "https://www.mediamarkt.be/fr/category/_t%C3%A9l%C3%A9phone-navigation-509451.html"
)

def get_main_links(url: str) -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        try:
            page.get_by_text("Tout accepter").click(timeout=5000)
            print("Consent button clicked")
        except:
            print("Consent button not found")    
        # page.wait_for_selector(':nth-match(:text("Afficher plus"), 3)').click(timeout=10000)    
        # page.locator(':nth-match(:text("Afficher plus"), 3)').click(timeout=10000)
        buttons = page.query_selector_all("button[class^='sc-21f2092b-1 bEkkuF']")
    
        print(len(buttons))
        print(buttons)
        for button in buttons:
            button.wait_for_element_state("visible", timeout=10000)
            button.click(timeout=5000)
        
       
       
        # more_buttons = [page.get_by_text("Afficher plus")for _ in range(4)]
        # print(len(more_buttons))
        
          
        html = page.content()
        soup = bs(html, "html.parser")
        li_tags = soup.find_all("li", attrs={"class": "sc-f741f313-2 kTVmzt"})
        categories = [li.find("a") for li in li_tags]
        category_links = []
        for category in tqdm(categories):
            first_url = base_url + category["href"]
            print(first_url)
            response = page.goto(first_url)
            final_url = response.url
            print(final_url)    
            category_links.append(final_url)
        browser.close()
        print(len(category_links))
    return category_links

def get_data(url: str) -> list:
    product_list = []
    current_url = url
    page_count = 0
    max_pages = 100
    with tqdm() as pbar:
        while page_count <= max_pages:
            print("-" * 100)
            print(f"Scraping page {page_count + 1}: {current_url}")
            response = requests.get(current_url, timeout=90.0)
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
    print(multimedia_url)
    multimedia_links = get_main_links(multimedia_url)
    phone_links = get_main_links(phone_url)
    categories_links = multimedia_links + phone_links
    print(len(categories_links))
    # final_list = []
    # # with open("data/categories_links.json", "r") as f:
    # #     categories_links = json.load(f)
    # products_list = []
    # for category_link in categories_links:
    #     print(f"Scraping {category_link}")
    #     task = get_data(category_link)
    #     products_list.append(task)
    # for products in products_list:
    #     final_list += products
    #     print(f"{len(final_list)} products scraped.")
    #     print("-" * 100)
    # with open("data/products.json", "w") as f:
    #     json.dump(final_list, f, indent=4)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Scraping completed in {elapsed_time/60:.2f} minutes.")

if __name__ == "__main__":
    main()
