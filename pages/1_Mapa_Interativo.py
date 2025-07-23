import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import json

# Supondo que suas funções de `src` estão funcionando como antes.
# Se precisar, podemos adaptá-las também.
from src.loader import carregar_dados
from src.filtros import filtros_menu, aplicar_filtros

# ----- CONFIGURAÇÕES DA PÁGINA E ESTILOS -----
st.set_page_config(layout="wide", page_title="Análise da Agricultura Familiar em Sergipe")

# Estilos podem ser mantidos ou simplificados.
st.markdown("""
<style>
    /* Centralizar o título da página */
    h1 {
        text-align: center;
    }
    /* Estilo para as métricas */
    .stMetric {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    /* Melhorar a aparência do expander */
    .st-expander {
        border-radius: 10px;
        border: 1px solid #E0E0E0;
    }
</style>
""", unsafe_allow_html=True)


# ----- FUNÇÕES AUXILIARES PARA ESTA PÁGINA -----

def carregar_geojson(path):
    """Carrega o arquivo GeoJSON dos municípios."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Arquivo GeoJSON não encontrado em '{path}'. O mapa coroplético não pode ser gerado. Faça o download e coloque na pasta 'data'.")
        return None

# ----- TÍTULO E INTRODUÇÃO -----
st.title("🗺️ Análise da Agricultura Familiar em Sergipe")
st.write("""
    Esta plataforma permite a exploração interativa de dados sobre famílias agricultoras no estado de Sergipe.
    Use os filtros na barra lateral para segmentar os dados e veja os resultados atualizados instantaneamente.
""")

# ----- CARREGAMENTO E FILTROS -----
df = carregar_dados("data/familias_agricultoras.csv")
geojson_sergipe = carregar_geojson("data/sergipe_municipios.json")

# Filtros na BARRA LATERAL
busca, municipio, produto, certificacao, genero, comunidade = filtros_menu(df)

# Aplica filtros
df_filtrado = aplicar_filtros(df, busca, municipio, produto, certificacao, genero, comunidade)

# ----- FEEDBACK IMEDIATO: MÉTRICAS (KPIs) -----
st.markdown("---")
st.subheader("Resumo da Seleção Atual")

if df_filtrado.empty:
    st.warning("Nenhum resultado encontrado para os filtros aplicados. Tente uma busca mais ampla.")
    st.stop()

# Calcula as métricas com base no dataframe filtrado
total_familias = len(df_filtrado)
total_area = df_filtrado['Área Cultivada (ha)'].sum()
total_producao = df_filtrado['Volume Produção Anual (Kg)'].sum()
municipios_unicos = df_filtrado['Município'].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total de Famílias", value=f"{total_familias:,.0f}".replace(",", "."))
with col2:
    st.metric(label="Municípios Abrangidos", value=f"{municipios_unicos}")
with col3:
    st.metric(label="Área Cultivada Total (ha)", value=f"{total_area:,.2f}".replace(",", "."))
with col4:
    st.metric(label="Produção Anual Total (Kg)", value=f"{total_producao:,.0f}".replace(",", "."))

st.markdown("---")


# ----- VISUALIZAÇÕES EM ABAS -----
st.subheader("Visualizações Geográficas e de Dados")

tab_mapa, tab_coropletico, tab_dados = st.tabs(["📍 Mapa de Produtores", "📊 Mapa de Densidade", "📄 Tabela de Dados"])

# Prepara dados para os mapas (sem NaNs em lat/lon)
df_mapa = df_filtrado.dropna(subset=["Latitude", "Longitude"]).copy()

with tab_mapa:
    st.info(f"Mostrando {len(df_mapa)} famílias no mapa. Use o zoom para separar os marcadores agrupados e clique para ver detalhes.")
    
    if not df_mapa.empty:
        # Centro do mapa calculado a partir da média dos pontos filtrados
        map_center = [df_mapa['Latitude'].mean(), df_mapa['Longitude'].mean()]
        
        m_cluster = folium.Map(location=map_center, zoom_start=8, tiles="CartoDB positron")
        
        # Agrupamento de marcadores
        marker_cluster = MarkerCluster().add_to(m_cluster)

        # Adicionar marcadores ao cluster
        for idx, row in df_mapa.iterrows():
            popup_html = f"""
            <b>Família:</b> {row.get('Nome da Família', 'N/I')}<br>
            <b>Município:</b> {row.get('Município', 'N/I')}<br>
            <b>Produção:</b> {row.get('Item de Produção Principal', 'N/I')}<br>
            """
            folium.Marker(
                [row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(marker_cluster)

        st_folium(m_cluster, height=500, width=1200, use_container_width=True)
    else:
        st.warning("Nenhuma família com dados de localização para os filtros selecionados.")

with tab_coropletico:
    if geojson_sergipe:
        st.info("Mapa de densidade por município. A cor representa o número de famílias agricultoras na seleção atual.")
        
        # Agrega dados por município para o mapa coroplético
        dados_municipio = df_filtrado.groupby('Município').size().reset_index(name='contagem_familias')
        
        m_coropleth = folium.Map(location=[-10.57, -37.38], zoom_start=8, tiles="CartoDB positron")

        folium.Choropleth(
            geo_data=geojson_sergipe,
            name='choropleth',
            data=dados_municipio,
            columns=['Município', 'contagem_familias'],
            key_on='feature.properties.NM_MUN', # Verifique essa chave no seu GeoJSON! Pode ser 'name', 'NM_MUN', etc.
            fill_color='YlGn', # Paleta de cores Verde-Amarelado
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Número de Famílias Agricultoras por Município',
            highlight=True,
        ).add_to(m_coropleth)
        
        st_folium(m_coropleth, height=500, use_container_width=True)
    else:
        st.warning("Não foi possível carregar o arquivo GeoJSON para gerar o mapa de densidade.")


with tab_dados:
    st.info("Explore os dados detalhados da sua seleção na tabela abaixo. Você pode ordenar as colunas clicando nos cabeçalhos.")
    # Exibe colunas relevantes
    colunas_para_exibir = [
        'Nome da Família', 'Município', 'Comunidade', 'Item de Produção Principal',
        'Tipo de Certificação', 'Área Cultivada (ha)', 'Volume Produção Anual (Kg)', 'Gênero Responsável'
    ]
    st.dataframe(df_filtrado[colunas_para_exibir], use_container_width=True, height=500)


# ----- SEÇÃO DE METODOLOGIA -----
st.markdown("---")
with st.expander("ℹ️ Sobre a Pesquisa e Metodologia", expanded=False):
    st.markdown("""
    #### Fonte dos Dados
    Os dados apresentados nesta plataforma foram coletados através de [descrever a fonte, ex: questionários aplicados em campo, bases de dados de secretarias, etc.] durante o período de [mês/ano] a [mês/ano].

    #### Público-Alvo
    A pesquisa focou em famílias agricultoras localizadas no estado de Sergipe, que se enquadram nos critérios de [descrever os critérios, ex: agricultura familiar, produção orgânica, participação em feiras, etc.].

    #### Metodologia de Coleta
    A coleta foi realizada por uma equipe de [número] pesquisadores que visitaram [número] municípios. Foram utilizadas entrevistas estruturadas e georreferenciamento dos estabelecimentos com o consentimento dos participantes.

    #### Limitações e Observações
    - Os dados de geolocalização (latitude e longitude) podem apresentar imprecisões pontuais.
    - O 'Volume de Produção Anual' é uma estimativa fornecida pelo produtor e pode variar sazonalmente.
    - Este é um projeto fictício para fins de demonstração e portfólio.
    """)

# ----- RODAPÉ -----
st.markdown("""
<hr>
<div style='text-align:center;color:#9ca3af;font-size:0.9em'>
    Projeto Fictício para Apresentação — 2024 | Desenvolvido com Streamlit
</div>
""", unsafe_allow_html=True)
