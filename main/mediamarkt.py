import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.mediamarkt.be/nl/category/_computer-multimedia-452669.html")

button_cookies = driver.find_element(
    By.XPATH, '//*[@id="pwa-consent-layer-form"]/div[2]/button[1]/span'
)
button_cookies.click()

more_button = driver.find_element(
    By.CSS_SELECTOR,
    "#main-content > div.sc-dbb4f5b6-0.dMPtoe > div.sc-490debc5-0.jhMMyN > div.sc-835d3f28-0.kTdeVZ > div.sc-b059e63d-0.czpKQP > section.sc-fb036814-0.keHeJk > div:nth-child(1) > div > div > aside > div > button > span",
)
more_button.click()

driver_wait = WebDriverWait(driver, 10)

div_element = driver_wait.until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, "sc-e8cb080e-0.hnbKx.sc-2d009fd-2.juHLTV")
    )
)

ul_tags = div_element.find_elements(By.TAG_NAME, "ul")
li_tags = [ul.find_elements(By.TAG_NAME, "li") for ul in ul_tags]

urls_mediamarkt = []
for li_list in li_tags:
    for li in li_list:
        href = li.find_element(By.TAG_NAME, "a").get_attribute("href")
        urls_mediamarkt.append(href)

print(urls_mediamarkt)

driver.quit()
