for team_id in tqdm(range(START_TEAM, END_TEAM + 1)):

    url = f"https://sbbl.es/equipos/{team_id}"
    response = session.get(url)

    # DEBUG SOLO PARA UN EQUIPO
    if team_id == 53:
        print("DEBUG HTML:")
        print(response.text[:1000])

    if response.status_code != 200:
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    team_name_tag = soup.select_one("h1")
    team_name = team_name_tag.text.strip() if team_name_tag else f"team_{team_id}"

    players = soup.select(".agent-name")

    for p in players:
        data.append({
            "team_id": team_id,
            "team": team_name,
            "player": p.text.strip()
        })

    time.sleep(DELAY)

print("Jugadores encontrados:", len(data))

df = pd.DataFrame(data)

if df.empty:
    raise Exception("No se extrajeron jugadores. Posible cambio en la web.")

df.to_csv("sbbl_players.csv", index=False)
print("Dataset guardado")
