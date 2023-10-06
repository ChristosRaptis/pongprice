import requests
from bs4 import BeautifulSoup
import json

vandenborre_urls = [
    "https://www.vandenborre.be/fr/multimedia",
    "https://www.vandenborre.be/fr/telephonie",
]
list_all_urls = []
list_urls_multim_teleph = []

session = requests.Session()


def getting_urls(urls, tag1, class1, tag2, class2, urls_list):
    for url in urls:
        url_text = session.get(url).text
        soup = BeautifulSoup(url_text, "html.parser")
        paragraphs = soup.find_all(
            tag1,
            class_=class1,
        )
        for paragraph in paragraphs:
            urls_list.append(paragraph.find(tag2, class_=class2)["href"])


getting_urls(
    vandenborre_urls,
    "div",
    "accordion-image-grid accordion--mobile col-xs-12 col-sm-6 col-md-4 margin-btm-40-md margin-btm-20-sm",
    "a",
    "h2-title hidden-xs default-txt-color no-border",
    list_all_urls,
)

list_all_urls = [f"https:{url}" for url in list_all_urls]

getting_urls(
    list_all_urls,
    "div",
    "accordion-image-grid accordion--mobile col-xs-12 col-sm-6 col-md-4 margin-btm-40-md margin-btm-20-sm",
    "a",
    "no-border padding-topbtm-10 display-block",
    list_urls_multim_teleph,
)
# deleting duplicates

list_urls_multim_teleph = list(set(list_urls_multim_teleph))
list_urls_multim_teleph = [f"https:{url}" for url in list_urls_multim_teleph]

with open("list_urls_multim_teleph.json", "w") as outfile:
    json.dump(list_urls_multim_teleph, outfile)
