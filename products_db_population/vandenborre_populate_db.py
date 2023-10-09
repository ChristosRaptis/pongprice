import psycopg2
import json
import pandas as pd
import re 

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

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)

cur = conn.cursor()
# open the csv file data/df_products_vandeborre.csv and store it in a variable called data
data = pd.read_csv("data/df_products_vandeborre.csv", index_col=0)
data["product_name"] = data["product_name"].apply(lambda x: re.sub(pattern, replace_capacity, x))
data["product_price"] = data["product_price"].apply(lambda x: clean_price(x))

data = data.to_dict("records")

for item in data:
        
    cur.execute(
        "INSERT INTO products (url, product_name, product_price_in_euros) VALUES (%s, %s, %s);",
        (item.get("url"), item.get("product_name"), item.get("product_price")),
    )

conn.commit()
cur.close()
conn.close()
