import psycopg2
import json
import re

def clean_price(s):
    s = s.replace(' ', '').replace('\xa0', '').replace('.', '').replace('€', '').replace('\u202f', '').replace('–', '').replace(',', '.').rstrip('0').rstrip(',').rstrip('-')
    return float(s)    

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)

cur = conn.cursor()

with open("data/krefel_product_data.json", "r") as f:
    data = json.load(f)
print(len(data))
print(data[0])
print("before")
for item in data:
    try:
        if item != None and item["product_price"] != 'N/A':
              
            
            item["product_price"] = clean_price(item["product_price"])
            
    except :
        continue
print(data[0])        
print(len(data))
for item in data:
    try:
        if item != None and item["product_price"] != 'N/A' :
                
            cur.execute(
                "INSERT INTO products (url, product_name, product_price_in_euros) VALUES (%s, %s, %s);",
                (item.get("url"), item.get("product_name"), item.get("product_price")),
            )
    except :    
        continue        

conn.commit()
cur.close()
conn.close()
