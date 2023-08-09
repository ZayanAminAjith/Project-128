from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
# Webdriver
browser = webdriver.Chrome()
browser.get(START_URL)

time.sleep(10)

brown_dwarfs_data = []

def scrape_more_data(hyperlink):    
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content,"html.parser")
    start_table = soup.find_all("table",atts={"class","wikitable sortable jquery-tablesorter"})
    temp = []
    table_rows = soup.find_all("tr")
    table_body = soup.find_all("tbody")

    for i in table_rows:
        td_tags = i.find_all("td")
        for j in td_tags:
            data = j.text.strip()
            temp.append(data)
    brown_dwarfs_data.append(temp)

planet_df_1 = pd.read_csv("updated_scraped_data.csv")

for index, row in planet_df_1.iterrows():
    print(row["hyperlink"])
    # Call scrape_more_data(<hyperlink>)
    scrape_more_data(row["hyperlink"])
    print(f"Data Scraping at hyperlink {index+1} completed")


planet_data = []
for k in range(0,len(brown_dwarfs_data)):
    Name = brown_dwarfs_data[k][0]
    Distance = brown_dwarfs_data[k][5]
    Mass = brown_dwarfs_data[k][7]
    Radius = brown_dwarfs_data[k][8]

    required_data = [Name, Distance, Mass, Radius]
    planet_data.append(required_data)
headers = ["brown_dwarf","distance", "mass", "radius"]

new_planet_df_1 = pd.DataFrame(planet_data,columns = headers)

# Convert to CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
