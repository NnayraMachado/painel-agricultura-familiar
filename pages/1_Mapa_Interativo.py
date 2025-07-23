import streamlit as st
import pandas as pd
# Importar numpy caso 'sum' retorne NaN ou para outras operações numéricas
import numpy as np

# Apenas importe o que é necessário para esta página diretamente.
# As funções carregar_dados, filtros_menu, aplicar_filtros, mostrar_mapa_folium
# são importadas dos seus respectivos arquivos na pasta 'src'.
from src.loader import carregar_dados
from src.filtros import filtros_menu, aplicar_filtros
from src.mapas_folium import mostrar_mapa_folium # Esta função já deve importar folium e st_folium internamente

# Para o mapa vazio de fallback, precisamos do folium e st_folium AQUI TAMBÉM
# Isso garante que mesmo se mostrar_mapa_folium não for chamada, o Streamlit ainda possa renderizar um mapa vazio.
import folium
from streamlit_folium import st_folium


# ----- CONFIGURAÇÕES E ESTILOS CUSTOMIZADOS PARA ESTA PÁGINA -----
st.markdown("""
<style>
/* Estilos específicos para esta página */
.ficha-box {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    height: 100%; /* Ocupa a altura da coluna */
    display: flex;
    flex-direction: column;
    justify-content: flex-start; /* Alinha o conteúdo ao topo */
}
.ficha-detail {
    line-height: 1.8;
    font-size: 1.05em;
    color: #343a40;
}
.ficha-detail b {
    color: #264653; /* Cor dos títulos dos campos */
}
.stMetric {
    background-color: #e9ecef;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: none; /* Remove sombra extra para métricas dentro da ficha */
}
.stMetric > div > div:first-child { font-size: 1em; color: #495057; }
.stMetric > div > div:nth-child(2) { font-size: 2.2em; font-weight: bold; color: #264653; }
.stImage > img {
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #2a9d8f;
    display: block;
    margin: 0 auto 15px auto;
}
.placeholder-image {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background-color: #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3em;
    color: #666;
    margin: 0 auto 15px auto;
    border: 3px solid #2a9d8f;
}
</style>
""", unsafe_allow_html=True)


# ----- TÍTULO E INTRODUÇÃO DA PÁGINA -----
st.title("🗺️ Mapa Interativo das Famílias Agricultoras")
st.write("""
Explore a distribuição das famílias agricultoras em Sergipe. Use os filtros no menu lateral para encontrar o que procura e clique nos marcadores do mapa para ver os detalhes de cada família!
""")

df = carregar_dados("data/familias_agricultoras.csv")

# --- Filtros na BARRA LATERAL ---
busca, municipio, produto, certificacao, genero, comunidade = filtros_menu(df)

# Aplica filtros
df_filtrado = aplicar_filtros(df, busca, municipio, produto, certificacao, genero, comunidade)

# Remove linhas sem localização antes de tudo para o mapa
df_filtrado_mapa = df_filtrado.dropna(subset=["Latitude", "Longitude"])

# Mensagem se não houver dados
if df_filtrado.empty:
    st.warning("Nenhum resultado encontrado para os filtros aplicados. Tente ajustar os filtros na barra lateral.")
    st.stop()

# Layout principal: Mapa e Ficha Técnica
col_mapa, col_ficha = st.columns([2.2, 1.2], gap="small")

with col_mapa:
    st.subheader("🗺️ Famílias no Mapa")
    if not df_filtrado_mapa.empty:
        st.info(f"Mostrando {len(df_filtrado_mapa)} famílias no mapa. Clique nos marcadores para ver a ficha técnica!")
        output = mostrar_mapa_folium(df_filtrado_mapa, height=540)
    else:
        st.warning("Nenhuma família encontrada com dados de localização para os filtros selecionados.")
        # Exibe um mapa vazio com centro em Sergipe se não houver dados filtrados com localização
        m = folium.Map(location=[-10.57, -37.38], zoom_start=8, tiles="CartoDB positron")
        st_folium(m, width=900, height=540, key="empty_map")
        output = {} # Garante que output seja um dict vazio

with col_ficha:
    st.subheader("📄 Ficha Técnica da Família")
    st.markdown("<div class='ficha-box'>", unsafe_allow_html=True) # Container para a ficha

    ficha_mostrada = False
    if output and output.get("last_object_clicked"):
        coords = output["last_object_clicked"]
        lat_clicked, lon_clicked = coords["lat"], coords["lng"]
        
        familia_encontrada_df = df_filtrado_mapa[
            (abs(df_filtrado_mapa["Latitude"] - lat_clicked) < 0.00001) &
            (abs(df_filtrado_mapa["Longitude"] - lon_clicked) < 0.00001)
        ].head(1)
        
        if not familia_encontrada_df.empty:
            row = familia_encontrada_df.iloc[0]
            
            st.markdown("<div class='placeholder-image'>👨‍🌾</div>", unsafe_allow_html=True) 
            
            st.markdown(f"""
            <div class="ficha-detail">
            <b>👪 Família:</b> {row.get('Nome da Família', 'Não Informado')}<br>
            <b>📍 Município:</b> {row.get('Município', 'Não Informado')}<br>
            <b>🏘️ Comunidade:</b> {row.get('Comunidade', 'Não Informado')}<br>
            <b>🚻 Gênero Responsável:</b> {row.get('Gênero Responsável', 'Não Informado')}<br>
            <b>🥕 Produção Principal:</b> {row.get('Item de Produção Principal', 'Não Informado')}<br>
            <b>🌶️ Produção Secundária:</b> {row.get('Item de Produção Secundário', 'Não Informado')}<br>
            <b>📜 Certificação:</b> {row.get('Tipo de Certificação', 'Não Informado')}<br>
            <b>📏 Área Cultivada (ha):</b> {row.get('Área Cultivada (ha)', 0):.2f} ha<br>
            <b>📦 Volume Anual (Kg):</b> {row.get('Volume Produção Anual (Kg)', 0):.0f} Kg<br>
            <b>🛒 Método de Venda:</b> {row.get('Método de Venda Principal', 'Não Informado')}<br>
            <b>🤝 Associação/Cooperativa:</b> {row.get('Associação/Cooperativa', 'Não Informado')}<br>
            <b>📞 Contato:</b> {row.get('Telefone', 'Não Informado')}
            {f" | <a href='mailto:{row['Email']}'>{row['Email']}</a>" if pd.notna(row.get('Email')) and row['Email'] != '' else ''}
            </div>
            """, unsafe_allow_html=True)
            ficha_mostrada = True
    
    if not ficha_mostrada:
        st.info("Aguardando seu clique no mapa para carregar os detalhes da família.")
    
    st.markdown("</div>", unsafe_allow_html=True) # Fecha o container da ficha

st.markdown("---")

# ---------- Rodapé opcional (consistente com outras páginas) ----------
st.markdown("""
<div style='margin-top:2em;text-align:right;color:#9ca3af;font-size:0.95em'>
Projeto fictício para apresentação — 2024.<br>
Contato: <a href='mailto:email@instituicao.org'>email@instituicao.org</a>
</div>
""", unsafe_allow_html=True)