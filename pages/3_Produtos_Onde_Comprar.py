import streamlit as st
import pandas as pd
# Importar urlencode para codificação de URL segura
from urllib.parse import urlencode 

from src.loader import carregar_dados
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# ----- CONFIGURAÇÕES INICIAIS DA PÁGINA -----
st.set_page_config(
    page_title="Produtos da Agricultura Familiar",
    layout="wide",
    page_icon="🛒" # Ícone de carrinho de compras
)

# ----- CSS CUSTOMIZADO PARA MELHORAR O VISUAL -----
st.markdown("""
<style>
/* Estilo geral */
body {
    font-family: 'Arial', sans-serif;
    color: #333333;
    background-color: #f0f2f6;
}

/* Título principal */
h1 {
    color: #264653; /* Azul escuro */
    font-size: 2.8em;
    text-align: center;
    margin-bottom: 0.5em;
    border-bottom: 2px solid #2a9d8f; /* Linha verde abaixo do título */
    padding-bottom: 10px;
}

/* Subtítulo/Descrição principal */
.main-intro {
    font-size: 1.2em;
    color: #555555;
    text-align: center;
    margin-bottom: 2em;
}

/* Seção de filtros */
.filter-section {
    background-color: white;
    padding: 1.5em;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 2em;
}
.filter-section h3 {
    color: #2a9d8f;
    margin-top: 0;
    margin-bottom: 1em;
}

/* Ajustes para a tabela AgGrid */
.ag-theme-streamlit {
    border-radius: 10px !important;
    overflow: hidden; /* Garante que as bordas arredondadas funcionem */
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.ag-header-cell-text {
    font-weight: bold !important;
    color: #264653 !important;
}
.ag-cell a { /* Estilo para os links dentro da tabela */
    color: #007bff;
    text-decoration: none;
    font-weight: bold;
}
.ag-cell a:hover {
    text-decoration: underline;
}

/* Mensagens de informação/alerta */
.stAlert {
    border-radius: 8px;
    font-size: 1.05em;
}
</style>
""", unsafe_allow_html=True)


st.title("🛒 Produtos da Agricultura Familiar: Onde Comprar?")

st.markdown("""
<p class="main-intro">
Encontre os produtos frescos e orgânicos da agricultura familiar! Use os filtros para buscar por tipo de produto, município ou certificação, e veja como entrar em contato direto com os produtores.
</p>
""", unsafe_allow_html=True)

df = carregar_dados("data/familias_agricultoras.csv")

# --- Funções para links ---
def link_email(email, nome_familia="", produto="", municipio=""):
    if pd.isna(email) or not str(email).strip():
        return ''
    email_str = str(email).strip()
    assunto = f"Interesse em produtos de {produto} - Família {nome_familia} ({municipio})"
    texto = (
        f"Olá, família {nome_familia} de {municipio},\n\n"
        f"Gostaria de saber mais sobre a disponibilidade e os preços dos seus produtos de {produto}.\n"
        "Por favor, me envie informações sobre como posso adquirir seus produtos e as formas de entrega.\n\n"
        "Obrigado(a)!"
    )
    # CORREÇÃO AQUI: Usar urlencode da urllib.parse
    assunto_params = urlencode({'s': assunto})[2:] # Remove 's='
    texto_params = urlencode({'b': texto})[2:] # Remove 'b='
    return f'<a href="mailto:{email_str}?{assunto_params}&{texto_params}">E-mail</a>'

def link_como_chegar(lat, lon):
    if pd.isna(lat) or pd.isna(lon):
        return ""
    # Mapeamento do Google Maps URL para coordenadas
    # ATENÇÃO: A URL maps.google.com pode precisar ser https://www.google.com/maps/search/?api=1&query=
    # dependendo de como você quer a funcionalidade de "como chegar".
    # A URL atual: https://www.google.com/maps/search/?api=1&query={lat},{lon} parece estar incorreta ou ser um placeholder.
    # A URL padrão para coordenadas no Google Maps é: https://www.google.com/maps/search/?api=1&query=LATITUDE,LONGITUDE
    maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    return f'<a href="{maps_url}" target="_blank">Como chegar</a>'

# --- Filtros ---
st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
st.subheader("🔍 Encontre o que você busca")
st.write("Use os filtros abaixo para refinar sua pesquisa na tabela.")

produtos = sorted(df["Item de Produção Principal"].dropna().astype(str).unique())
municipios = sorted(df["Município"].dropna().astype(str).unique())
certificacoes = sorted(df["Tipo de Certificação"].dropna().astype(str).unique())

col1, col2, col3 = st.columns(3)
with col1:
    produto_selecionado = st.selectbox("Filtrar por Produto", ["Todos"] + produtos, key="filter_produto")
with col2:
    municipio_selecionado = st.selectbox("Filtrar por Município", ["Todos"] + municipios, key="filter_municipio")
with col3:
    certificacao_selecionada = st.selectbox("Filtrar por Certificação", ["Todos"] + certificacoes, key="filter_certificacao")

st.markdown("</div>", unsafe_allow_html=True) # Fecha a seção de filtros

# --- Aplica filtros ---
df_filtro = df.copy()
if produto_selecionado != "Todos":
    df_filtro = df_filtro[df_filtro["Item de Produção Principal"].astype(str) == produto_selecionado]
if municipio_selecionado != "Todos":
    df_filtro = df_filtro[df_filtro["Município"].astype(str) == municipio_selecionado]
if certificacao_selecionada != "Todos":
    df_filtro = df_filtro[df_filtro["Tipo de Certificação"].astype(str) == certificacao_selecionada]

# --- Mensagem de Sem Resultados ---
if df_filtro.empty:
    st.warning("Nenhum produtor encontrado com os filtros selecionados. Por favor, ajuste suas opções.")
    st.stop()

# --- Links (mantém HTML para AgGrid) ---
df_filtro["E-mail"] = df_filtro.apply(
    lambda row: link_email(
        row.get("Email", None), # Passa None se não encontrar a chave
        nome_familia=row.get("Nome da Família", ""),
        produto=row.get("Item de Produção Principal", ""),
        municipio=row.get("Município", ""),
    ), axis=1
)
df_filtro["Como chegar"] = df_filtro.apply(
    lambda row: link_como_chegar(
        row.get("Latitude", None), # Passa None se não encontrar a chave
        row.get("Longitude", None),
    ), axis=1
)

# Colunas a serem exibidas e seus nomes de cabeçalho
colunas_exibir = [
    "Nome da Família", "Município", "Comunidade", "Item de Produção Principal",
    "Tipo de Certificação", "E-mail", "Como chegar"
]

# --- AgGrid options ---
gd = GridOptionsBuilder.from_dataframe(df_filtro[colunas_exibir])
gd.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)
gd.configure_default_column(editable=False, groupable=True, sortable=True, filter=True, resizable=True)

# Configura as colunas de link para renderizar HTML
gd.configure_column("E-mail", header_name="📧 E-mail", cellRenderer=JsCode('''function(params) {return params.value}'''), width=120)
gd.configure_column("Como chegar", header_name="🗺️ Como Chegar", cellRenderer=JsCode('''function(params) {return params.value}'''), width=150)

gd.configure_side_bar()
gridoptions = gd.build()

st.subheader("📋 Produtores Encontrados")
st.write("A tabela abaixo lista os produtores que correspondem aos seus filtros. Clique nos cabeçalhos para ordenar, use a barra lateral para mais filtros e os links para contato ou rota.")

# --- Mostra tabela interativa ---
AgGrid(
    df_filtro[colunas_exibir],
    gridOptions=gridoptions,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    height=400,
    fit_columns_on_grid_load=True,
    theme="streamlit"
)

# --- Download dos dados filtrados ---
st.markdown("---")
st.subheader("📥 Baixar Dados")
st.write("Baixe a lista de contatos dos produtores filtrados para usar offline.")

csv = df_filtro[colunas_exibir].to_csv(index=False).encode("utf-8")
st.download_button(
    "Baixar contatos filtrados (.csv)",
    data=csv,
    file_name="contatos_agricultores.csv",
    mime="text/csv",
    help="Clique para baixar a tabela visível em formato CSV."
)

st.markdown("---")

# ---------- Rodapé opcional ----------
st.markdown("""
<div style='margin-top:2em;text-align:right;color:#9ca3af;font-size:0.95em'>
Projeto fictício para apresentação — 2024.<br>
Contato: <a href='mailto:email@instituicao.org'>email@instituicao.org</a>
</div>
""", unsafe_allow_html=True)