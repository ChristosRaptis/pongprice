import json
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm
import requests
import fake_useragent
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
import os
import psycopg2
import re


class Scraper:
    
    def __init__(self, url,sitemap_condition) -> None:
        self.url = url
        self.product_sitemaps = self.get_sitemaps(url, sitemap_condition)

    def get_soup(self, url: str, parser: str) -> bs:
        """Returns a BeautifulSoup object from a product url
        Args:
            product_url (str): product url
            parser (str): parser to use, 'html.parser' or 'xml'
        Returns:
            bs: BeautifulSoup object
        """

        user_agent = fake_useragent.UserAgent().random
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers)
        soup = bs(response.text, parser)
        return soup

    def get_product_urls_from_xml(self, sitemap_urls_list: list) -> list:
        """Returns a list of product urls from a list of sitemap urls
        Args:
            sitemap_urls_list (list): list of sitemap urls
        Returns:
            list: list of product urls
        """
        product_urls = []
        for sitemap_url in tqdm(
            sitemap_urls_list, desc="Getting product urls", total=len(sitemap_urls_list)
        ):
            user_agent = fake_useragent.UserAgent().random
            headers = {"User-Agent": user_agent}
            response = requests.get(sitemap_url, headers=headers)
            soup = bs(response.text, "xml")
            urls = [url.text for url in soup.find_all("loc")]
            product_urls.extend(urls)
        return product_urls

    def get_sitemaps(self, url, sitemap_condition):
        
        main_sitemap_soup = self.get_soup(url, "xml")

        # find sitemaps that contain 'smartphone' or 'laptop' in the url
        product_sitemaps = [
            url.text
            for url in main_sitemap_soup.find_all("loc")
            if sitemap_condition in url.text
        ]

        all_product_sitemaps = self.get_product_urls_from_xml(product_sitemaps)

        # quick way to delete duplicates
        all_product_sitemaps = list(set(all_product_sitemaps))
        
        return all_product_sitemaps[:100]

    def get_db_connection(self):
        """Returns a connection to the postgreSQL database
        Returns:
            psycopg2.connection: connection to the database
        """
        load_dotenv()
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        conn = psycopg2.connect(
            host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
        )
        return conn


    def update_database(self, product_data: dict, cursor) -> None:
        """Checks the database for the product url (unique key) of the product data, if it exists it updates the price,
        if not it inserts the product data
        Args:
            product_data (dict): dictionary containing the product url, name and price
            cursor: cursor to the database
        """
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM products WHERE url=%s);", (product_data["url"],)
        )
        exists = cursor.fetchone()[0]
        if exists:
            print("the product already exists, updating the price ...")
            cursor.execute(
                "UPDATE products SET product_price = %s WHERE url = %s;",
                (product_data["product_price"], product_data["url"]),
            )
        else:
            print("the product does not exist, inserting the product data ...")
            cursor.execute(
                "INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
                (
                    product_data["url"],
                    product_data["product_name"],
                    product_data["product_price"],
                ),
            )
    
    # Define a function to replace storage capacity values with the desired format
    def replace_capacity(self, match):
        if match.group(4):
            return f"{match.group(1)} {match.group(2)} / {match.group(3)} {match.group(4)}"
        else:
            return f"{match.group(1)} {match.group(2)}"

    def get_product_data(self, product_url: str, conn):
        """
        Returns a dictionary containing the product url, name and price from a product url

        Args:
            product_url (str): product url
        Returns:
            dict: dictionary containing the product url, name and price

        """
        print(f"Scraping {product_url}")
        product_data = {}
        soup = self.get_soup(product_url, "html.parser")

        if "krefel" in product_url :
            script = soup.find("script", type="application/json")
            dict = json.loads(script.string)
            try:
                data = dict["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"][
                    "data"
                ]
                product_data["url"] = product_url
                product_data["product_name"] = data["manufacturer"] + " " + data["name"]
                product_data["product_price"] = data["price"]["value"]
            except:
                print("error getting data")
                pass
        
        elif "mediamarkt" in product_url or "vandenborre" in product_url :
            scripts = soup.find_all("script", type="application/ld+json")
            for script in scripts:
                data = json.loads(script.string)
                if "offers" in data:
                    # Process the data as needed
                    try:
                        pattern = r"(\d+)(G[Bo]|T[Bo])(?:/(\d+)(G[Bo]|T[Bo]))?"
                        product_data["url"] = product_url
                        product_data['product_name'] = re.sub(pattern, self.replace_capacity, data["name"])
                        # product_data["product_name"] = data["name"]
                        product_data["product_price"] = data["offers"]["price"]
                    except:
                        print("error getting data from vandenborre")
                        pass
                elif "object" in data :
                    try:
                        product_data["url"] = product_url
                        product_data["product_name"] = data["object"]["name"]
                        product_data["product_price"] = data["object"]["offers"]["price"]
                    except:
                        print("error getting data from mediamarkt")
                        pass
                else :
                    pass
        
        # verifies if product_data not empty
        if bool(product_data):
            cur = conn.cursor()
            self.update_database(product_data, cur)
            conn.commit()
            cur.close()

        return product_data

    def run_scraper(self):

        start_time = time.perf_counter()     
        print(f"Found {len(self.product_sitemaps)} product urls")
        conn = self.get_db_connection()

        with ThreadPoolExecutor(max_workers=3) as pool:
            product_list = list(
                tqdm(
                    pool.map(
                        self.get_product_data, self.product_sitemaps, [conn] * len(self.product_sitemaps)
                    ),
                    total=len(self.product_sitemaps),
                    desc= self.url.split(".")[1] ,
                )
            )

        conn.close()

        print(product_list)
        print(f"Scraped {len(product_list)} products ")
        end_time = time.perf_counter()
        print(f"Finished in {round((end_time - start_time)/60, 2)} minutes")


# sitemap_condition :
# krefel : "product"
# vandenborre : "productcatalog.xml"
# mediamarkt : "productdetailspages"