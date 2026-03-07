import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from tqdm import tqdm
from datetime import datetime

START_TEAM = 1
END_TEAM = 200

DELAY_MIN = 3
DELAY_MAX = 6

MAX_RETRIES = 3

print("Iniciando scraping...")

scraper = cloudscraper.create_scraper()

scraper.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://sbbl.es/"
})

# visitar home primero para generar cookies
scraper.get("https://sbbl.es")

data = []

for team_id in tqdm(range(START_TEAM, END_TEAM + 1)):

    url = f"https://sbbl.es/equipos/{team_id}"

    response = None

    for attempt in range(MAX_RETRIES):

        try:
            response = scraper.get(url, timeout=15)

            if response.status_code == 200:
                break

        except Exception as e:
            print(f"Error en equipo {team_id}, intento {attempt+1}")

        time.sleep(5)

    if response is None or response.status_code != 200:
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

    # delay aleatorio para evitar bloqueo
    delay = random.uniform(DELAY_MIN, DELAY_MAX)
    time.sleep(delay)

print("Jugadores encontrados:", len(data))

df = pd.DataFrame(data)

if df.empty:
    raise Exception("No se extrajeron jugadores")

df.to_csv("sbbl_players.csv", index=False)

print("Dataset guardado")

with open("last_update.txt", "w") as f:
    f.write(datetime.now().strftime("%d %b %Y %H:%M"))

print("Fecha de actualización guardada")
