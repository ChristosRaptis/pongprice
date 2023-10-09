import psycopg2
import pandas as pd
from config import DATABASE_CONFIG
import json

conn = psycopg2.connect(
    host=DATABASE_CONFIG["host"],
    port=DATABASE_CONFIG["port"],
    user=DATABASE_CONFIG["user"],
    password=DATABASE_CONFIG["password"],
)

cur = conn.cursor()

with open("bol/bol_products.json", "r") as file:
    data = json.load(file)

data = [item for sublist in data for item in sublist]

insert_query = (
    "INSERT INTO products (product_name, url, product_price) VALUES (%s, %s, %s)"
)


for record in data:
    if record is not None:
        try:
            data_tuple = (
                record["product_name"],
                # some urls are too long therefore need to be limited to 255, this is a solution for test run but for deployment table must be able to take >255 characters for urls
                record["url"][:255],
                record["product_price"],
            )
            cur.execute(insert_query, data_tuple)

        except KeyError:
            url = record.get("url")
            product_name = record.get("product_name")
            product_price = record.get("product_price")
            if product_name is None or url is None or product_price is None:
                print("Skipping a record with missing data.")


conn.commit()
cur.close()
conn.close()
