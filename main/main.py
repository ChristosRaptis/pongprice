import pandas as pd
import numpy as np
import streamlit as st
import os
from dotenv import load_dotenv
import psycopg2
import re

input_user = st.text_input("What is the item you are looking for : ").lower()


def get_products():
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    connection = psycopg2.connect(
        host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
    )

    cursor = connection.cursor()

    query = f"SELECT * FROM products WHERE LOWER(product_name) LIKE '%{input_user}%'"

    cursor.execute(query)

    products = cursor.fetchall()

    st.write("Search Results:")
    if products:
        for product in products:
            st.write(product)
    else:
        st.write("No matching products found.")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    get_products()



def search_product(item):
    query = "SELECT * FROM products WHERE product_name LIKE %s"
    


from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

make_searchable()

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    search_vector = db.Column(TSVectorType('product_name'))

    def __init__(self, product_name):
        self.product_name = product_name

    q = request.args.get('q', '')
    products = search(db.session.query(Product), q, sort=True).all()



q = request.args.get("q")
query = "SELECT * FROM products WHERE product_name LIKE %s"
products = search_products(q)

