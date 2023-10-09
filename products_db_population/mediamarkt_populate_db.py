import psycopg2
import json
<<<<<<< HEAD
<<<<<<< HEAD
import re
from dotenv import load_dotenv
import os


def clean_price(s):
    s = (
        s.replace(" ", "")
        .replace("€", "")
        .replace("\u202f", "")
        .replace("–", "")
        .replace(",", ".")
        .rstrip("0")
        .rstrip(",")
        .rstrip("-")
    )
    return float(s)


load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
)


=======
=======
import re

def clean_price(s):
    s = s.replace(' ', '').replace('€', '').replace('\u202f', '').replace('–', '').replace(',', '.').rstrip('0').rstrip(',').rstrip('-')
    return float(s)    

>>>>>>> ca87103 (modified files for prices)

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)

>>>>>>> 97252e9 (modify json)
cur = conn.cursor()

with open("data/mediamarkt_products.json", "r") as f:
    data = json.load(f)

<<<<<<< HEAD
# cur.execute(
#     "CREATE TABLE products (url TEXT, product_name TEXT, product_price_in_euros REAL);"
# )

for item in data:
    item["product_price"] = clean_price(item["product_price"])
=======
cur.execute(
    "CREATE TABLE products (url TEXT, product_name TEXT, product_price_in_euros REAL);"
)

for item in data:
<<<<<<< HEAD
>>>>>>> 97252e9 (modify json)
=======
    item["product_price"] = clean_price(item["product_price"])
>>>>>>> ca87103 (modified files for prices)
    cur.execute(
        "INSERT INTO products (url, product_name, product_price_in_euros) VALUES (%s, %s, %s);",
        (item["product_url"], item["product_name"], item["product_price"]),
    )

conn.commit()
cur.close()
conn.close()
