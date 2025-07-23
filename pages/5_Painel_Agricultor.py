import streamlit as st
import pandas as pd
import numpy as np # Importar numpy caso 'sum' retorne NaN

# Supondo que src/loader.py existe e tem carregar_dados
# Se não existir, você pode colocar a lógica de carregamento aqui diretamente
# Ex: df = pd.read_csv("data/familias_agricultoras.csv", sep=";")
# df.columns = df.columns.str.strip()
# if "Estado" not in df.columns: df["Estado"] = "SE"
# if "Região" not in df.columns: df["Região"] = "Nordeste"
from src.loader import carregar_dados

# ----- CONFIGURAÇÕES E ESTILOS (MELHORIA DE UX) -----
st.set_page_config(layout="centered", page_title="Painel do Agricultor", page_icon="👨🏾‍🌾") # Adiciona ícone e centraliza

st.markdown("""
<style>
/* Cores e fontes para um visual mais acolhedor e claro */
body { background-color: #f8f9fa; color: #343a40; }
h1, h2, h3 { color: #24405a; }
.stSelectbox label, .stRadio label { font-weight: bold; color: #495057; }
.stMetric { background-color: #e9ecef; border-radius: 8px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.stMetric > div > div:first-child { font-size: 1em; color: #495057; } /* Título do metric */
.stMetric > div > div:nth-child(2) { font-size: 2.2em; font-weight: bold; color: #264653; } /* Valor do metric */
.stDataFrame { border-radius: 8px; overflow: hidden; }
.stAlert { border-radius: 8px; padding: 15px; font-size: 1.1em; }
.whatsapp-button {
    background-color: #25D366; /* Cor do WhatsApp */
    color: white;
    padding: 12px 20px;
    border-radius: 50px; /* Mais arredondado */
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 18px;
    font-weight: bold;
    margin-top: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: background-color 0.3s ease;
}
.whatsapp-button:hover {
    background-color: #1DA851;
    color: white !important; /* Garante que o texto fique branco ao passar o mouse */
    text-decoration: none !important;
}
.whatsapp-button-container {
    text-align: center;
    margin-top: 30px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


st.title("👨🏾‍🌾 Painel do Agricultor – Veja Sua Comunidade")
st.write("""
**Bem-vindo!** Aqui você, agricultor familiar, pode ver de forma simples e clara as informações da sua comunidade registradas no nosso projeto.
Entenda quantos produtores estão ativos, qual o volume total de produção e os principais produtos cultivados, além de como manter seu contato atualizado.
""")

df = carregar_dados("data/familias_agricultoras.csv")

# --- Seleção de Município e Comunidade ---
st.subheader("📍 Encontre Sua Comunidade")
col_mun, col_comun = st.columns(2)

with col_mun:
    mun = st.selectbox("Selecione seu município", sorted(df["Município"].dropna().unique()), key="municipio_selector")

with col_comun:
    # Garante que as opções da comunidade dependam do município selecionado
    comunidades_no_municipio = sorted(df[df["Município"] == mun]["Comunidade"].dropna().unique())
    if not comunidades_no_municipio:
        st.warning(f"Não há comunidades cadastradas para o município de {mun}.")
        st.stop() # Parar a execução se não houver comunidades para evitar erros
    comun = st.selectbox(
        "Agora escolha sua comunidade",
        comunidades_no_municipio,
        key="comunidade_selector"
    )

# --- Filtrar dados para a comunidade selecionada ---
df_comun = df[(df["Município"] == mun) & (df["Comunidade"] == comun)].copy() # Use .copy() para evitar SettingWithCopyWarning

if df_comun.empty:
    st.warning(f"Nenhum dado encontrado para a comunidade **{comun}** em **{mun}**. Por favor, verifique a seleção ou entre em contato para cadastrar.")
    st.stop() # Parar aqui se não houver dados

# --- Métricas Principais ---
st.subheader("📊 Resumo da Sua Produção")
col_metric1, col_metric2 = st.columns(2)

with col_metric1:
    num_familias = len(df_comun["Nome da Família"].unique()) # Conta famílias únicas
    st.metric("👥 Famílias Cadastradas", num_familias)

with col_metric2:
    producao_total = df_comun["Volume Produção Anual (Kg)"].sum()
    st.metric("🌱 Produção Total (Kg/Ano)", int(producao_total))

# --- Principais Produtos ---
st.subheader("Harvest: Principais produtos")
top_produtos = df_comun.groupby("Item de Produção Principal")["Volume Produção Anual (Kg)"].sum().nlargest(3).reset_index()
if not top_produtos.empty:
    st.write("Os principais itens cultivados na sua comunidade são:")
    for idx, row in top_produtos.iterrows():
        st.markdown(f"- **{row['Item de Produção Principal']}** ({int(row['Volume Produção Anual (Kg)']):,} kg)")
else:
    st.info("Não há dados de produtos para esta comunidade.")

# --- Tabela Detalhada ---
st.subheader("📚 Detalhes dos Cadastros")
st.write("Veja as informações de contato e produção das famílias da sua comunidade:")

# Formata o telefone para exibição
# df_comun["Telefone Formatado"] = df_comun["Telefone"].astype(str).str.replace(r'(\d{2})(\d{5})(\d{4})', r'(\1) \2-\3', regex=True)

st.dataframe(
    df_comun[["Nome da Família", "Item de Produção Principal", "Tipo de Certificação", "Telefone"]], # Use 'Telefone' original ou formatado
    use_container_width=True,
    hide_index=True # Esconde o índice numérico
)

st.write("Se a sua família não está listada ou se os dados precisam ser atualizados, entre em contato:")

# --- Chamada para Ação com Botão de WhatsApp ---
st.markdown("""
<div class="whatsapp-button-container">
    <a href="https://wa.me/5579999999999?text=Ol%C3%A1%2C%20gostaria%20de%20atualizar%20meus%20dados%20no%20Painel%20do%20Agricultor." 
       target="_blank" class="whatsapp-button">
       📲 Falar com a Equipe (WhatsApp)
    </a>
</div>
""", unsafe_allow_html=True)

st.info("Sua participação é fundamental para mantermos as informações atualizadas e para que possamos oferecer o melhor apoio ao desenvolvimento da sua comunidade!")