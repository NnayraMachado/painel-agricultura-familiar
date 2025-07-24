import streamlit as st

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
body {
    font-family: 'Arial', sans-serif;
    color: #333333;
    background-color: #f0f2f6;
}
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
.call-to-action-box {
    background-color: #e6f7ff;
    border-left: 5px solid #007bff;
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
    color: #2a9d8f;
    margin-top: 0;
    font-size: 1.5em;
}
.section-card p {
    color: #666666;
    font-size: 0.95em;
}
.st-emotion-cache-nahz7x { gap: 2rem; }

/* BANNER COM OVERLAY */
.hero-banner {
    position: relative;
    width: 95%;
    max-width: 650px;
    margin: 2em auto 2.5em auto;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(40,90,60,0.11), 0 2px 8px rgba(0,0,0,0.05);
}
.hero-banner img {
    display: block;
    width: 100%;
    height: 250px;
    object-fit: cover;
    filter: brightness(0.88) saturate(1.05);
}
.hero-overlay {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(90deg, #2a9d8fdd 10%, #26465388 85%, #ffffff00 100%);
    display: flex;
    align-items: center;
    justify-content: flex-start;
}
.hero-content {
    position: absolute;
    left: 0;
    top: 0;
    padding: 32px 30px;
    color: #fff;
    max-width: 70%;
    font-size: 1.38em;
    font-weight: 600;
    text-shadow: 0 3px 14px rgba(44,66,70,0.15);
}
.hero-subtitle {
    font-size: 1.07em;
    font-weight: 400;
    margin-top: 7px;
    color: #e5fff5;
}
@media (max-width: 600px) {
    .hero-banner img { height: 140px;}
    .hero-content { font-size: 1em; padding: 12px 12px; max-width: 92%;}
}
</style>
""", unsafe_allow_html=True)

# ----- TÍTULO -----
st.title("🌱 Painel da Agricultura Familiar")

# ----- BANNER INICIAL IMPACTANTE -----
banner_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"
st.markdown(f"""
<div class="hero-banner">
  <img src="{banner_url}" alt="Capa Agricultura Familiar">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    A força que vem da terra.<br>
    <span class="hero-subtitle">
        Agricultura familiar, alimento saudável, futuro sustentável.<br>
        <span style='font-size:0.98em;font-weight:400;'>Explore dados, histórias e comunidades que mudam a vida no campo.</span>
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ----- INTRODUÇÃO (opcional, pode remover pois o banner já faz o papel) -----
# st.markdown("""
# <p class="main-intro">
# Bem-vindo(a) ao seu portal de informações sobre as <b>famílias agricultoras</b>!
# Aqui, você pode explorar dados valiosos, conhecer histórias inspiradoras e descobrir o potencial
# da produção orgânica certificada, que sustenta tantas vidas e enriquece nosso alimento.
# </p>
# """, unsafe_allow_html=True)

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
    Para navegar entre as seções, utilize o <b>menu lateral</b> (clique no ">" no canto superior esquerdo, se estiver no celular) e selecione a página desejada.
    </p>
</div>
""", unsafe_allow_html=True)

# ----- Rodapé Básico -----
st.markdown("""
<div style='margin-top:2em;text-align:center;color:#9ca3af;font-size:0.85em'>
Desenvolvido com carinho para a Agricultura Familiar.
</div>
""", unsafe_allow_html=True)
