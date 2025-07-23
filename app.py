import streamlit as st
import base64 # Importa a biblioteca base64 para codificação

# ----- CONFIGURAÇÕES INICIAIS DA PÁGINA -----
st.set_page_config(
    page_title="Agricultura Familiar - Painel",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌿"
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

/* Bloco de destaque para a chamada */
.call-to-action-box {
    background-color: #e6f7ff; /* Azul claro */
    border-left: 5px solid #007bff; /* Linha azul */
    padding: 1.5em;
    margin-top: 3em;
    margin-bottom: 3em;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
}
.call-to-action-box p {
    font-size: 1.1em;
    font-weight: bold;
    color: #004085;
    text-align: center;
}

/* Seções de destaque das páginas */
.section-card {
    background-color: white;
    padding: 1.5em;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 1.5em;
    transition: transform 0.2s ease-in-out;
}
.section-card:hover {
    transform: translateY(-5px);
}
.section-card h3 {
    color: #2a9d8f; /* Verde vibrante */
    margin-top: 0;
    font-size: 1.5em;
}
.section-card p {
    color: #666666;
    font-size: 0.95em;
}

/* Alinhamento de colunas para as seções */
.st-emotion-cache-nahz7x { /* Adjusts spacing between elements in columns */
    gap: 2rem;
}

/* Estilo para imagem de destaque na intro - Aplicado via HTML */
.intro-image {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 60%; /* Ajuste conforme necessário */
    max-width: 400px; /* Limita o tamanho máximo */
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    margin-bottom: 2em;
}

</style>
""", unsafe_allow_html=True)


# ----- CONTEÚDO DA PÁGINA PRINCIPAL -----

st.title("🌱 Painel da Agricultura Familiar")

# NOVO BLOCO PARA CARREGAR E EXIBIR A IMAGEM COM BASE64 E CSS
image_path = "imagens/logo.jpg"
try:
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    image_html = f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{encoded_string}" 
             class="intro-image" alt="A força que vem da terra.">
        <p class="small-font" style="margin-top: 0.5em;">A força que vem da terra.</p>
    </div>
    """
    st.markdown(image_html, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning(f"A imagem '{image_path}' não foi encontrada. Por favor, verifique o caminho.")
    # Fallback para um ícone ou texto se a imagem não carregar
    st.markdown("<div style='text-align: center; font-size: 3em;'>🌾</div>", unsafe_allow_html=True)


st.markdown("""
<p class="main-intro">
Bem-vindo(a) ao seu portal de informações sobre as **famílias agricultoras**! 
Aqui, você pode explorar dados valiosos, conhecer histórias inspiradoras e descobrir o potencial 
da produção orgânica certificada, que sustenta tantas vidas e enriquece nosso alimento.
</p>
""", unsafe_allow_html=True)

# ----- SEÇÕES DE DESTAQUE DAS PÁGINAS -----
st.subheader("💡 O que você pode explorar aqui?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="section-card">
        <h3>📊 Tendências e Dados</h3>
        <p>Entenda o volume de produção, os produtos mais cultivados e a evolução ao longo dos anos. Veja os rankings por município, produto e comunidade.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="section-card">
        <h3>🗺️ Histórias Vivas</h3>
        <p>Conheça a vida e os desafios de agricultores de Sergipe através de relatos poéticos e inspiradores. Descubra a força e a resiliência de cada um.</p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="section-card">
        <h3>👨🏾‍🌾 Minha Comunidade</h3>
        <p>Encontre os dados específicos da sua comunidade: número de famílias cadastradas, produção total e detalhes de contato. Mantenha suas informações atualizadas!</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="section-card">
        <h3>🌍 Mapa Interativo</h3>
        <p>Explore as comunidades e seus dados em um mapa dinâmico para visualizar a distribuição da agricultura familiar em Sergipe.</p>
    </div>
    """, unsafe_allow_html=True)

# ----- CHAMADA PARA AÇÃO FINAL -----
st.markdown("""
<div class="call-to-action-box">
    <p>
    Para navegar entre as seções, utilize o **menu lateral** (clique no ">" no canto superior esquerdo, se estiver no celular) e selecione a página desejada.
    </p>
</div>
""", unsafe_allow_html=True)

# ----- Rodapé Básico (se não tiver um rodapé global em todas as páginas) -----
st.markdown("""
<div style='margin-top:2em;text-align:center;color:#9ca3af;font-size:0.85em'>
Desenvolvido com carinho para a Agricultura Familiar.
</div>
""", unsafe_allow_html=True)