import streamlit as st
import pandas as pd
from urllib.parse import quote_plus
from src.loader import carregar_dados

# ----- CONFIGURAÇÕES INICIAIS DA PÁGINA -----
st.set_page_config(
    page_title="Onde Comprar da Agricultura Familiar",
    layout="wide",
    page_icon="🛒"
)

# ----- CSS CUSTOMIZADO (COM FONT AWESOME PARA ÍCONES) -----
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<style>
    h1 {
        color: #264653;
        font-size: 2.8em;
        text-align: center;
        margin-bottom: 0.5em;
        border-bottom: 2px solid #2a9d8f;
        padding-bottom: 10px;
    }
    .main-intro {
        font-size: 1.2em;
        color: #555555;
        text-align: center;
        margin-bottom: 2em;
    }
    .filter-section {
        background-color: white;
        padding: 1.5em;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 2em;
    }
    
    .producer-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-left: 8px solid #2a9d8f;
        border-radius: 10px;
        padding: 2em;
        margin-top: 2em;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .producer-card h2 {
        color: #264653;
    }
    .producer-photo {
        font-size: 6em;
        text-align: center;
        line-height: 1.5;
        color: #2a9d8f;
    }
    /* Removido o estilo .stDataFrame a, pois a coluna de telefone será removida */
</style>
""", unsafe_allow_html=True)


# ----- TÍTULO, DADOS E FILTROS -----
st.title("🛒 Catálogo de Produtores")
st.markdown("<p class='main-intro'>Encontre produtos frescos e orgânicos diretamente de quem produz! Use os filtros para refinar sua busca e clique em uma linha da tabela para ver mais detalhes.</p>", unsafe_allow_html=True)

df = carregar_dados("data/familias_agricultoras.csv")

# Garante que as colunas Latitude e Longitude são numéricas, se existirem
if 'Latitude' in df.columns:
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
if 'Longitude' in df.columns:
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')


with st.container(border=True):
    st.subheader("🔍 Encontre o que você busca")
    col1, col2, col3 = st.columns(3)
    
    df_filtro = df.copy()
    produto_selecionado = col1.selectbox("Filtrar por Produto", ["Todos"] + sorted(df["Item de Produção Principal"].dropna().unique()))
    municipio_selecionado = col2.selectbox("Filtrar por Município", ["Todos"] + sorted(df["Município"].dropna().unique()))
    certificacao_selecionada = col3.selectbox("Filtrar por Certificação", ["Todos"] + sorted(df["Tipo de Certificação"].dropna().unique()))

    if produto_selecionado != "Todos": df_filtro = df_filtro[df_filtro["Item de Produção Principal"] == produto_selecionado]
    if municipio_selecionado != "Todos": df_filtro = df_filtro[df_filtro["Município"] == municipio_selecionado]
    if certificacao_selecionada != "Todos": df_filtro = df_filtro[df_filtro["Tipo de Certificação"] == certificacao_selecionada]

# ----- PREPARAÇÃO E EXIBIÇÃO DA TABELA USANDO ST.DATAFRAME -----
if df_filtro.empty:
    st.warning("Nenhum produtor encontrado com os filtros selecionados. Por favor, ajuste suas opções.")
else:
    # Prepara o DataFrame para exibição no st.dataframe
    # REMOVIDA A COLUNA "Telefone Contato" daqui
    df_exibicao = df_filtro[[
        "Nome da Família", 
        "Município", 
        "Item de Produção Principal"
    ]].copy() 
    
    # Renomeia as colunas para exibição
    df_exibicao.rename(columns={
        "Nome da Família": "Produtor(a)",
        "Município": "Município",
        "Item de Produção Principal": "Produto Principal"
    }, inplace=True)

    st.subheader("📋 Produtores Encontrados")
    st.info("Clique em uma linha da tabela para ver todos os detalhes do produtor e seus contatos.")
    
    # Inicializa selected_index se não existir
    if 'selected_index' not in st.session_state:
        st.session_state.selected_index = None

    if not df_exibicao.empty:
        st.write("Selecione um produtor da lista para ver os detalhes:")
        
        produtor_nomes = ["Selecione um produtor..."] + df_exibicao["Produtor(a)"].tolist()
        
        selected_produtor_name_from_selectbox = st.selectbox(
            "Escolha um produtor:",
            produtor_nomes,
            key="produtor_selector"
        )

        selected_row_data = None
        if selected_produtor_name_from_selectbox != "Selecione um produtor...":
            selected_row_data = df_filtro[df_filtro['Nome da Família'] == selected_produtor_name_from_selectbox].iloc[0]
            selected_data = [{'Produtor(a)': selected_row_data['Nome da Família']}]
        else:
            selected_data = [] 

        st.dataframe(
            df_exibicao, 
            hide_index=True, 
            use_container_width=True,
            height=400,
        )
    else:
        selected_data = [] 


    # ----- FICHA DE DETALHES DO PRODUTOR SELECIONADO -----
    if selected_data and not pd.DataFrame(selected_data).empty:
        st.markdown("<div class='producer-card'>", unsafe_allow_html=True)
        col_foto, col_info = st.columns([1, 3])
        with col_foto:
            st.markdown("<div class='producer-photo'><i class='fa-solid fa-user-circle'></i></div>", unsafe_allow_html=True)
        with col_info:
            st.subheader(f"{selected_row_data.get('Nome da Família', 'Nome não informado')}")
            st.write(f"**Localização:** {selected_row_data.get('Comunidade', '')}, {selected_row_data.get('Município', '')}")
            st.write(f"**Certificação:** {selected_row_data.get('Tipo de Certificação', 'Não informado')}")
            st.write(f"**Principal Método de Venda:** {selected_row_data.get('Método de Venda Principal', 'Não informado')}")
        st.markdown("---")
        st.subheader("Produtos Oferecidos")
        prod_principal = selected_row_data.get('Item de Produção Principal', 'N/I')
        prod_secundario = selected_row_data.get('Item de Produção Secundário', 'N/I')
        st.info(f"**Principal:** {prod_principal}")
        if pd.notna(prod_secundario) and prod_secundario.strip():
            st.success(f"**Outros:** {prod_secundario}")
        st.markdown("---")
        st.subheader("Entrar em Contato")
        
        telefone_num = ''.join(filter(str.isdigit, str(selected_row_data.get("Telefone", ""))))
        if len(telefone_num) >= 10:
            msg_wpp = quote_plus(f"Olá {selected_row_data.get('Nome da Família', '')}, vi seus produtos na plataforma e tenho interesse.")
            st.link_button("📲 Contatar via WhatsApp", f"https://wa.me/55{telefone_num}?text={msg_wpp}")
        
        if pd.notna(selected_row_data.get("Email")):
            st.link_button("📧 Enviar E-mail", f"mailto:{selected_row_data.get('Email')}")

        lat, lon = selected_row_data.get("Latitude"), selected_row_data.get("Longitude")
        if pd.notna(lat) and pd.notna(lon):
            maps_url = f"http://maps.google.com/maps?q={lat},{lon}"
            st.link_button("🗺️ Ver no Mapa", maps_url)

        st.markdown("</div>", unsafe_allow_html=True)
    elif st.session_state.get('selected_index') is None and not df_filtro.empty:
        st.info("Por favor, selecione um produtor da lista acima para ver os detalhes.")


# ----- SEÇÃO DE DOWNLOAD -----
st.markdown("---")
st.subheader("📥 Baixar Dados")
st.write("Baixe a lista de contatos dos produtores filtrados para usar offline.")

colunas_download = [
    "Nome da Família", "Município", "Comunidade", 
    "Item de Produção Principal", "Tipo de Certificação",
    "Telefone", "Email" 
]
colunas_download_existentes = [col for col in colunas_download if col in df_filtro.columns]
df_download = df_filtro[colunas_download_existentes]

csv = df_download.to_csv(index=False).encode("utf-8")

st.download_button(
    "Baixar contatos filtrados (.csv)",
    data=csv,
    file_name="contatos_agricultores.csv",
    mime="text/csv",
    help="Clique para baixar a tabela com os contatos em formato CSV."
)
