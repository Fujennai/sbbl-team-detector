import streamlit as st
import pandas as pd
import os

# -----------------------
# Cargar dataset
# -----------------------

if os.path.exists("sbbl_players.csv") and os.path.getsize("sbbl_players.csv") > 0:
    df = pd.read_csv("sbbl_players.csv")
else:
    df = pd.DataFrame(columns=["team_id", "team", "player"])

# -----------------------
# Cargar fecha actualización
# -----------------------

if os.path.exists("last_update.txt"):
    with open("last_update.txt") as f:
        last_update = f.read()
else:
    last_update = "desconocida"

# -----------------------
# Estadísticas
# -----------------------

total_teams = df["team"].nunique()
total_players = df["player"].nunique()

# -----------------------
# UI
# -----------------------

st.title("Detector de Equipos SBBL")

st.caption(
    f"Equipos: {total_teams} | Jugadores: {total_players} | "
    f"Última actualización: {last_update}"
)

st.write("Pega una lista de jugadores (uno por línea)")

texto = st.text_area("Jugadores")

min_jugadores = st.slider(
    "Jugadores mínimos para detectar equipo",
    min_value=2,
    max_value=6,
    value=3
)

# -----------------------
# Análisis
# -----------------------

if st.button("Analizar"):

    lista = [j.strip() for j in texto.split("\n") if j.strip()]

    df_temp = df.copy()
    df_temp["player_lower"] = df_temp["player"].str.lower()

    coincidencias = df_temp[
        df_temp["player_lower"].isin([j.lower() for j in lista])
    ]

    resultado = (
        coincidencias
        .groupby("team")
        .agg(
            jugadores=("player", list),
            total=("player", "count")
        )
        .reset_index()
    )

    resultado = resultado[resultado["total"] >= min_jugadores]

      st.subheader("Equipos detectados")

    if resultado.empty:
        st.warning("No se detectaron equipos.")
    else:
        resultado = resultado.sort_values("total", ascending=False)

        st.dataframe(
            resultado,
            use_container_width=True,
            hide_index=True
        )
