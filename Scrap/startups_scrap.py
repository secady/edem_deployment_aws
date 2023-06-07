
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import requests
import time
import os
import pandas as pd


def clear(): 
    if os.name == "posix":
        os.system("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system("cls")


# Dado que la página tiene un sistema anti-bot, creamos un fake-agent:
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}


# Instalamos el driver para Chrome.
service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Comprobamos la disponibilidad de la web.
url = "https://lanzadera.es/proyectos/"
response = requests.get(url, headers=HEADERS)

# Extraemos el contenido de la web.
html = response.content
soup = bs(html, "lxml")

# Abrimos el navegador y vamos cargando los datos.
driver.get(url)
time.sleep(1)
cookies = driver.find_element(by="xpath", value="/html/body/div[2]/div/div[3]/button[1]")
if cookies.is_displayed() == True:
    cookies.click()
    time.sleep(0.5)
driver.maximize_window()
time.sleep(0.5)

total_page_height = driver.execute_script("return document.body.scrollHeight")
browser_window_height = driver.get_window_size(windowHandle='current')['height']
current_position = driver.execute_script('return window.pageYOffset')
scrolls = 0

while total_page_height - current_position > browser_window_height:
    driver.execute_script('window.scrollBy(0,500)')
    total_page_height = driver.execute_script("return document.body.scrollHeight")
    browser_window_height = driver.get_window_size(windowHandle='current')['height']
    current_position = driver.execute_script('return window.pageYOffset')
    scrolls += 1
    clear()
    print(scrolls)
    time.sleep(1)

# Desplegados ya todos los elementos de la página, empezamos el scrap:

# Lista de Start-ups (html)
all_startups = soup.select("div.elementor-widget-wrap section.projects-grid article")

# Lista de tópicos:
topic_list = []
for startup in all_startups:
    if startup.select("div.projects-grid__topic") == []:
        topic_list.append(None)
    else:
        pre_topic_list = [topic.get_text() for topic in startup.select("div.projects-grid__topic")]
        topic_list.append(pre_topic_list)

# Lista de enlaces a logos:
logo_link_list = [startup.select("figure a img")[0].get("data-lazy-src") for startup in all_startups]

# Lista de enlaces a la página de la Start-up:
link_list = [startup.find("a").get("href") for startup in all_startups]

# Lista de nombres de Start-ups:
name_list = [startup.select("figure a img")[0].get("alt") for startup in all_startups]

# Lista de texto descriptivo:
text_list = [" ".join(startup.select("div.projects-grid__description")[0].get_text().split()) for startup in all_startups]

# Lista de estado de fase:
phase_list = []
for startup in all_startups:
    phase = startup.select("div.projects-grid__phase")
    if phase == []:
        phase_list.append(None)
    else:
        phase_list.append(phase[0].get_text())


# Ahora convertimos las listas en un dataframe:
df = pd.DataFrame({
    "name": name_list,
    "phase": phase_list,
    "topics": topic_list,
    "description": text_list,
    "url": link_list,
    "logo_link": logo_link_list
})

# Y finalmente las convertimos en json y archivamos:
df.to_json("startups_data.json", index=True)
df.to_json("startups_by_rows.json", orient= "index")

# Cerramos:
driver.close()
cwd = os.getcwd()
print(f"Documento creado en {cwd}")
print("Proceso terminado")