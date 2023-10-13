import requests
from bs4 import BeautifulSoup

vandenborre_urls = [
    "https://www.vandenborre.be/fr/multimedia",
    "https://www.vandenborre.be/fr/telephonie",
]
list_all_urls = []


def getting_urls(urls, tag1, class1, tag2, class2):
    for url in urls:
        with requests.Session() as session:
            url_text = session.get(url).text
        soup = BeautifulSoup(url_text, "html.parser")
        paragraphs = soup.find_all(
            tag1,
            class_=class1,
        )
        for paragraph in paragraphs:
            list_all_urls.append(paragraph.find(tag2, class_=class2)["href"])


getting_urls(
    vandenborre_urls,
    "div",
    "accordion-image-grid accordion--mobile col-xs-12 col-sm-6 col-md-4 margin-btm-40-md margin-btm-20-sm",
    "a",
    "h2-title hidden-xs default-txt-color no-border",
)

list_urls_multim_teleph = []


# for url in urls:
#     with requests.Session() as session:
#         url_text = session.get(url).text
#     soup = BeautifulSoup(url_text, "html.parser")
#     paragraphs = soup.find_all(
#         "div",
#         class_="accordion-image-grid accordion--mobile col-xs-12 col-sm-6 col-md-4 margin-btm-40-md margin-btm-20-sm",
#     )
#     for paragraph in paragraphs:
#         list_all_urls.append(
#             paragraph.find(
#                 "a", class_="h2-title hidden-xs default-txt-color no-border"
#             )["href"]
#         )


list_urls_multim_teleph = []

for url in list_all_urls:
    with requests.Session() as session:
        url_text = session.get(f"https:{url}").text
    soup = BeautifulSoup(url_text, "html.parser")
    paragraphs = soup.find_all(
        "div",
        class_="accordion-image-grid accordion--mobile col-xs-12 col-sm-6 col-md-4 margin-btm-40-md margin-btm-20-sm",
    )
    for paragraph in paragraphs:
        list_urls_multim_teleph.append(
            paragraph.find("a", class_="no-border padding-topbtm-10 display-block")[
                "href"
            ]
        )

 [url in list_all_urls] 
getting_urls(list_all_urls, 
# deleting duplicates

list_urls_multim_teleph = list(set(list_urls_multim_teleph))
print(list_urls_multim_teleph)
