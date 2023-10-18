"""
This module contains utility functions for scrapers

functions:
- `get_product_urls`
- `get_data_soup`
- `clean_price`
- `get_db_connection`

libraries:
- `requests`
- `fake_useragent`
- `bs4`
- `tqdm`
- `dotenv`
- `os`
- `psycopg2`
"""

import requests
import fake_useragent
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from dotenv import load_dotenv
import os
import psycopg2
import json


def get_product_urls_from_xml(sitemap_urls_list: list) -> list:
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


def get_soup(url: str, parser: str) -> bs:
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


def clean_price(number: str) -> float:
    """Returns a float from a string containing a price

    Args:
        number (str): string containing a price
    Returns:
        float: price as a float

    """
    number = (
        number.replace(" ", "")
        .replace("\xa0", "")
        .replace(".", "")
        .replace("€", "")
        .replace("\u202f", "")
        .replace("–", "")
        .replace(",", ".")
        .rstrip("0")
        .rstrip(",")
        .rstrip("-")
    )
    return float(number)


def get_db_connection():
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


def update_database(product_data: dict, cursor) -> None:
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


def dump_json(list_of_items, name_json_file):
    with open(name_json_file, "w") as outfile:
        json.dump(list_of_items, outfile)


def open_json(name_json_file):
    with open(name_json_file, "r") as file:
        json_list = json.load(file)
        return json_list


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
    print(len(scripts))
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
