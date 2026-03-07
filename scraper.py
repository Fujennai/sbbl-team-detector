import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime

BASE_URL = "https://sbbl.es"

print("Iniciando scraper...")

scraper = cloudscraper.create_scraper()

scraper.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": BASE_URL
})

# visitar la home primero
scraper.get(BASE_URL)

# ------------------------------------------------
# 1️⃣ Obtener lista de equipos
# ------------------------------------------------

print("Buscando equipos...")

response = scraper.get(f"{BASE_URL}/equipos")

soup = BeautifulSoup(response.text, "html.parser")

team_links = soup.select("a[href^='/equipos/']")

team_ids = set()

for link in team_links:
    href = link.get("href")
    try:
        team_id = int(href.split("/")[-1])
        team_ids.add(team_id)
    except:
        pass

team_ids = sorted(team_ids)

print(f"Equipos detectados: {len(team_ids)}")

# ------------------------------------------------
# 2️⃣ Scraping de jugadores
# ------------------------------------------------

data = []

for team_id in tqdm(team_ids):

    url = f"{BASE_URL}/equipos/{team_id}"

    try:
        response = scraper.get(url)
    except:
        continue

    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    team_name_tag = soup.select_one("h1")

    if not team_name_tag:
        continue

    team_name = team_name_tag.text.strip()

    players = soup.select(".agent-name")

    for p in players:

        player = p.text.strip()

        data.append({
            "team_id": team_id,
            "team": team_name,
            "player": player
        })

    time.sleep(0.05)

# ------------------------------------------------
# 3️⃣ Crear dataset
# ------------------------------------------------

print("Jugadores encontrados:", len(data))

df = pd.DataFrame(data)

if df.empty:
    raise Exception("No se extrajeron jugadores")

df.to_csv("sbbl_players.csv", index=False)

print("Dataset guardado")

# ------------------------------------------------
# 4️⃣ Guardar fecha
# ------------------------------------------------

with open("last_update.txt", "w") as f:
    f.write(datetime.now().strftime("%d %b %Y %H:%M"))

print("Fecha de actualización guardada")
