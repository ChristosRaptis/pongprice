import psycopg2
import json
import re

def clean_price(s):
    s = s.replace(' ', '').replace('€', '').replace('\u202f', '').replace('–', '').replace(',', '.').rstrip('0').rstrip(',').rstrip('-')
    return float(s)    


conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)

cur = conn.cursor()

with open("data/mediamarkt_products.json", "r") as f:
    data = json.load(f)

cur.execute(
    "CREATE TABLE products (url TEXT, product_name TEXT, product_price_in_euros REAL);"
)

for item in data:
    item["product_price"] = clean_price(item["product_price"])
    cur.execute(
        "INSERT INTO products (url, product_name, product_price_in_euros) VALUES (%s, %s, %s);",
        (item["product_url"], item["product_name"], item["product_price"]),
    )

conn.commit()
cur.close()
conn.close()
