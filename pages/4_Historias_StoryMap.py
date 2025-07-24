import streamlit as st
import json
import os

# Configuração da página
st.set_page_config(
    page_title="Produção Orgânica Certificada",
    layout="wide",
    page_icon="🌱"
)

# Caminho correto considerando que este arquivo está em /pages
current_script_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_script_dir, '..'))

# Carrega CSS externo
css_file_path = os.path.join(root_dir, "styles.css")
try:
    with open(css_file_path, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"Erro: O arquivo '{css_file_path}' não foi encontrado.")

# Carrega histórias do JSON na raiz
json_file_path = os.path.join(root_dir, "historias.json")
with st.spinner('Carregando histórias dos agricultores...'):
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                historias = json.load(f)
        else:
            st.error(f"Erro: O arquivo '{json_file_path}' não foi encontrado.")
            historias = []
    except json.JSONDecodeError:
        st.error("Erro: O arquivo de histórias não está em formato JSON válido.")
        historias = []

# Título e introdução
st.title("🌱 Produção Orgânica Certificada na Agricultura Familiar")
st.subheader("Conheça as histórias que transformam vidas e o meio ambiente.")

st.markdown("""
<div class="intro-section">
    <i class="fa-solid fa-seedling"></i>
    <p>No coração de cada lavoura e em cada rio, reside uma vida de esforço e esperança para a agricultura familiar. Em Sergipe, enfrentamos desafios diários: o clima imprevisível, a falta de infraestrutura básica e a necessidade de apoio para que o sustento da terra não se perca.</p>
    <p>Mesmo assim, a busca pela <b>Produção Orgânica Certificada</b> cresce. É plantar sem veneno, valorizar o que é puro e garantir alimento de qualidade. Para isso, é preciso conhecimento, certificação, transporte adequado e um mercado justo. Apoio coletivo — governos, associações, pesquisa — é fundamental para construir uma vida mais justa e sustentável no campo.</p>
    <p>Vamos inverter a conversa: comece pelas pessoas e suas histórias reais. Descubra como elas — e você — se conectam com o cuidado da terra e do nosso povo.</p>
</div>
""", unsafe_allow_html=True)

# Abas de histórias
if historias:
    tab_labels = [h["titulo"] for h in historias]
    abas = st.tabs(tab_labels)
    for idx, tab in enumerate(abas):
        with tab:
            historia = historias[idx]
            st.markdown(f"<div class='story-title'>{historia['titulo']}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='frase-destaque'>{historia['frase_destaque']}</span>", unsafe_allow_html=True)
            st.write("")

            # Layout das imagens (usar st.image para servir imagens locais)
            col1, col2 = st.columns([1.25, 2])
            with col1:
                st.image(os.path.join(root_dir, historia['mapa_img']), use_container_width=True)
                with st.expander(historia['municipio_texto']):
                    st.write(historia['mapa_texto_detalhado'])

            with col2:
                st.image(os.path.join(root_dir, historia['personagem_img']), use_container_width=True)
                st.markdown("<div class='img-caption'>Retrato ilustrativo</div>", unsafe_allow_html=True)
            st.write("")

            st.subheader("📚 História Completa")
            st.write(historia['historia'])

            st.markdown(
                f"<div class='blockquote'><span>&#10077;</span> <i>{historia['fala_personagem']}</i></div>",
                unsafe_allow_html=True
            )
            st.write(historia['continua'])

            st.caption(f"História {idx + 1} de {len(historias)}")
            st.markdown("<hr class='stDivider'>", unsafe_allow_html=True)

            # Chamada para ação (Catálogo)
            st.markdown("""
            <div class="cta-catalogo">
                <p>Quer encontrar produtores como este? Visite nosso <a href="/Catalogo_de_Produtores" target="_self">Catálogo de Produtores</a>!</p>
            </div>
            """, unsafe_allow_html=True)

else:
    st.info("Nenhuma história encontrada ou houve um erro ao carregar as histórias.")

# Rodapé
st.markdown("""
<div class='footer-links' style='margin-top:2.5em;text-align:right;color:#9ca3af;font-size:0.95em'>
<i class="fa-solid fa-handshake"></i> <b>Quer compartilhar sua história?</b> Escreva para: <a href='mailto:email@instituicao.org'>email@instituicao.org</a><br>
Projeto fictício para apresentação — 2024.
</div>
""", unsafe_allow_html=True)
