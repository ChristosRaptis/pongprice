# Pongprice

## Contributors

[ChristosRaptis](https://github.com/ChristosRaptis)

[RamiRambo](https://github.com/RamiRambo)

## Description

This is a project made for training and to display the capabilities of the contributors. Our goal was to practice tools such as Webscrapping with Selenium & Playwright, PostgreSQL, Flask/SQLAlchemy + HTML, htmx.

Our work is structured as follows : 
Main folder includes the scripts for the web visuals (Flask but Streamlit was also used).
Data folder : includes all the json files with the scraped data either urls or product data.
Products_db_population folder : includes all connections to insert our scraped products data into postgresql and a few cleaning steps.
Templates folder : includes the html code that works with Flask and our script app.py in the main folder.


## Installation

Install the following packages to be able to run : 

Playwright
Selenium
BeautifulSoup
Concurrent.futures
Flask
SQLAlchemy
HTMX
Psycopg2


## Visuals

![PongPrice (Image)](Visual_Pongprice.png)

## To do

1) Pipeline : streamline the scraping processes and unify by using sitemaps only.
    - Airflow
    - Mediamarkt, Vandenborre, (Bol if works) : sitemap (create class/function for uniformization)
    - Verifiying if data already in PostgreSQL & price still unchanged & update -> add code for first verifying before inserting into db& unify for the different websites : 4 -> 1 .
    - Clean necessary files in scrapers : keep only necessary ones.

2) Bol : scraping of Bol is complicated, to be continued ...
3) HTML : include the logo in the page. 
