import streamlit as st
import pandas as pd

# cargar dataset
df = pd.read_csv("sbbl_players.csv")

st.title("Detector de Equipos SBBL")

st.write("Pega una lista de jugadores (uno por línea)")

texto = st.text_area("Jugadores")

min_jugadores = st.slider("Jugadores mínimos para detectar equipo", 2, 6, 3)

if st.button("Analizar"):

    lista = [j.strip() for j in texto.split("\n") if j.strip()]

    df_temp = df.copy()
    df_temp["player_lower"] = df_temp["player"].str.lower()

    coincidencias = df_temp[df_temp["player_lower"].isin([j.lower() for j in lista])]

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

    if len(resultado) == 0:
        st.write("No se detectaron equipos.")
    else:
        st.dataframe(resultado)