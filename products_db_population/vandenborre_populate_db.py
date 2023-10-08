import psycopg2
import json
import pandas as pd
import re 

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)

cur = conn.cursor()
# open the csv file data/df_products_vandeborre.csv and store it in a variable called data
data = pd.read_csv("data/df_products_vandeborre.csv", index_col=0)
data['product_name'] = data['product_name'].str.replace(r'(\d+)GB', r'\1 GB', regex=True)

data = data.to_dict("records")

for item in data:
        
    cur.execute(
        "INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
        (item.get("url"), item.get("product_name"), item.get("product_price")),
    )

conn.commit()
cur.close()
conn.close()
