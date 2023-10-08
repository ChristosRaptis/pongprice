import psycopg2
import json
import pandas as pd
import re 
<<<<<<< HEAD
from dotenv import load_dotenv
import os


# Define a regular expression pattern to match storage capacity values
pattern = r"(\d+)(G[Bo]|T[Bo])(?:/(\d+)(G[Bo]|T[Bo]))?"

# Define a function to replace storage capacity values with the desired format
def replace_capacity(match):
    if match.group(4):
        return f"{match.group(1)} {match.group(2)} / {match.group(3)} {match.group(4)}"
    else:
        return f"{match.group(1)} {match.group(2)}"

def clean_price(s):
    s = s.replace(' ', '').replace('\xa0', '').replace('.', '').replace('€', '').replace('\u202f', '').replace('–', '').replace(',', '.').rstrip('0').rstrip(',').rstrip('-')
    return float(s)    

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
=======

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
>>>>>>> 2bb951a (populated products db and tested app)
)

cur = conn.cursor()
# open the csv file data/df_products_vandeborre.csv and store it in a variable called data
data = pd.read_csv("data/df_products_vandeborre.csv", index_col=0)
<<<<<<< HEAD
data["product_name"] = data["product_name"].apply(lambda x: re.sub(pattern, replace_capacity, x))
data["product_price"] = data["product_price"].apply(lambda x: clean_price(x))
=======
data['product_name'] = data['product_name'].str.replace(r'(\d+)GB', r'\1 GB', regex=True)
>>>>>>> 2bb951a (populated products db and tested app)

data = data.to_dict("records")

for item in data:
        
    cur.execute(
        "INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
        (item.get("url"), item.get("product_name"), item.get("product_price")),
    )

conn.commit()
cur.close()
conn.close()
