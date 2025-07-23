import streamlit as st
import folium
from streamlit_folium import st_folium
import random

def mostrar_mapa_folium(df, height=540):
    df = df.dropna(subset=["Latitude", "Longitude"])
    if df.empty:
        st.warning("Nenhuma família encontrada para esse filtro.")
        return None

    municipios = sorted(df["Município"].unique())
    cores_base = ["red", "blue", "green", "purple", "orange", "darkred", "lightgray", "beige", "darkblue", "cadetblue", "darkgreen"]
    while len(cores_base) < len(municipios):
        cores_base.append('#%06X' % random.randint(0, 0xFFFFFF))
    cor_por_municipio = {mun: cor for mun, cor in zip(municipios, cores_base)}

    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=7, control_scale=True)
    for _, row in df.iterrows():
        mun = row["Município"]
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            tooltip=row['Nome da Família'],
            popup=row['Nome da Família'],
            icon=folium.Icon(color=cor_por_municipio[mun], icon="info-sign")
        ).add_to(m)

    # Legenda customizada
    legenda_html = """
    <div style="position: fixed; bottom: 30px; left: 20px; width: 210px; z-index:9999; font-size:15px; 
                background-color: white; border: 1px solid #aaa; border-radius: 7px; padding: 8px 10px;">
      <b>Legenda: Município</b><br>
      """ + "".join([f'<span style="color:{cor_por_municipio[m]}; font-size:1.2em;">&#9679;</span> {m}<br>' for m in municipios]) + """
    </div>
    """
    m.get_root().html.add_child(folium.Element(legenda_html))
    output = st_folium(m, width=850, height=height, returned_objects=["last_object_clicked"])
    return output
