import pandas as pd
import requests
import os

HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

df = pd.read_json("startups_data.json")

names_list = df["name"]
url_list = df["logo_link"]

os.mkdir("Logos")
os.chdir("Logos")

for ind,url in enumerate(url_list):
    name = f"{names_list[ind]}.png"
    logo = requests.get(url, headers=HEADERS).content
    with open(name, "wb") as handler:
        handler.write(logo)