import streamlit as st
import json

# ----- CSS CUSTOMIZADO PARA MELHORAR O VISUAL (Adicionado mais consistência) -----
st.markdown("""
<style>
/* Estilo geral (já deveria vir do app.py se for multi-página, mas repetido para segurança aqui) */
body {
    font-family: 'Arial', sans-serif;
    color: #333333;
    background-color: #f0f2f6;
}

/* Títulos h1, h2, h3 - Consistente com outras páginas */
h1, h2, h3 {
    color: #24405a;
    font-weight: bold;
}
h1 {
    font-size: 2.8em;
    text-align: center;
    margin-bottom: 0.5em;
    border-bottom: 2px solid #2a9d8f;
    padding-bottom: 10px;
}
h2 {
    font-size: 1.8em;
    margin-top: 1.5em;
}
h3 {
    font-size: 1.5em;
    margin-top: 1.5em;
}

/* Sidebar (se houver) - Consistente com outras páginas */
section[data-testid="stSidebar"] {
    background: #f0f2f6;
    padding-top: 20px;
    padding-left: 20px;
    padding-right: 20px;
}

/* Imagens */
img {
    border-radius: 12px !important;
    box-shadow: 0 4px 24px rgba(40,40,60,0.08);
}

/* Bloco de citação (fala_personagem) */
.blockquote {
    background-color: #e3f2fd;
    border-left: 4px solid #2196F3;
    padding: 0.7em 1em;
    margin-bottom: 1em;
    margin-top: 1em;
    border-radius: 5px; /* Adicionado borda arredondada */
    box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* Sombra suave */
}
.blockquote span { /* Ícone da aspa */
    color: #2196F3;
    font-size: 1.5em; /* Aumentado um pouco */
    vertical-align: middle;
    margin-right: 5px;
}
.blockquote i {
    font-size: 1.1em; /* Ajustado tamanho da fonte da fala */
    color: #333;
}

/* Título de cada história dentro da aba */
.story-title {
    font-size: 2em; /* Aumentado */
    font-weight: 700;
    color: #264653; /* Consistente com h1 */
    margin-bottom: 0.5em;
    border-bottom: 1px solid #ddd; /* Linha suave */
    padding-bottom: 5px;
}

/* Frase destaque da história */
.frase-destaque {
    font-size: 1.3em; /* Aumentado */
    color: #556677;
    font-style: italic; /* Adicionado itálico para destaque */
    margin-bottom: 1.5em;
    display: block; /* Garante que o span ocupe a linha toda */
}

/* Expander do município */
.stExpander {
    background-color: #f8f9fa; /* Fundo suave */
    border-radius: 8px;
    padding: 10px;
    border: 1px solid #ddd;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.stExpander > div > div > button { /* Ajusta o botão do expander */
    font-weight: bold;
    color: #007bff; /* Cor do link */
}


/* Botão "Voltar ao Topo" */
.scroll-to-top-button {
    background-color: #007bff; /* Azul */
    color: white;
    padding: 10px 15px;
    border-radius: 5px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border: none;
    transition: background-color 0.3s ease;
}
.scroll-to-top-button:hover {
    background-color: #0056b3;
}
</style>
""", unsafe_allow_html=True)

# ----- Carrega os dados das histórias do arquivo JSON -----
try:
    with open('historias.json', 'r', encoding='utf-8') as f:
        historias = json.load(f)
except FileNotFoundError:
    st.error("Erro: O arquivo 'historias.json' não foi encontrado. Certifique-se de que ele está na mesma pasta do seu script.")
    historias = []
except json.JSONDecodeError:
    st.error("Erro: O arquivo 'historias.json' não está em um formato JSON válido.")
    historias = []

# ---------- Título e intro (NOVO) ----------
st.title("Produção Orgânica Certificada na Agricultura Familiar")
st.subheader("E o que eu tenho a ver com isso?")

st.markdown("""
No coração de cada lavoura e em cada rio, reside uma vida de esforço e esperança para a agricultura familiar. Aqui em Sergipe, enfrentamos desafios diários: o clima imprevisível que traz secas e enchentes, a falta de infraestrutura básica como estradas e acesso à saúde, e a necessidade de apoio para que o sustento da terra não se perca.

Mesmo com essas lutas, a busca pela **Produção Orgânica Certificada na Agricultura Familiar** cresce como um caminho. É plantar sem veneno, valorizar o que é puro e garantir que esse alimento chegue à sua mesa com um selo de qualidade. Para isso, o agricultor precisa de conhecimento, de meios para a certificação, de transporte adequado e de um mercado que reconheça seu trabalho e seu produto. É fundamental o apoio coletivo – de governos, associações e da pesquisa – para construir pontes, inovar e criar condições para uma vida mais justa e sustentável no campo.

Por isso, vamos inverter a conversa. Em vez de começar pelas grandes teorias, vamos começar pela gente. Pelas mãos que trabalham na terra, pelos desafios do dia a dia e pelas esperanças que brotam no chão. Convidamos você a conhecer alguns personagens, criados a partir de realidades que existem em todo o nosso país, e descobrir como a vida deles – e a sua – se conecta com o jeito de cuidar da nossa terra e do nosso povo.
""")

# ---------- Abas ----------
if historias:
    tab_labels = [h["titulo"] for h in historias]
    abas = st.tabs(tab_labels)

    for idx, (tab, historia) in enumerate(zip(abas, historias)):
        with tab:
            st.markdown(f"<div class='story-title'>{historia['titulo']}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='frase-destaque'>\"{historia['frase_destaque']}\"</span>", unsafe_allow_html=True) # Aplicando classe
            st.write("")
            
            # ---- layout principal
            col1, col2 = st.columns([1.2, 2])
            with col1:
                st.image(historia['mapa_img'], use_container_width=True) 
                
                # Apenas o expander, usando municipio_texto como rótulo
                with st.expander(historia['municipio_texto']):
                    st.write(historia['mapa_texto_detalhado'])

            with col2:
                st.image(historia['personagem_img'], caption="Retrato ilustrativo", use_container_width=True)
            st.write("")

            st.subheader("📚 História Completa") # Subheader mais descritivo com ícone
            st.write(historia['historia'])

            # ---- Bloco de fala destacada
            st.markdown(f"<div class='blockquote'><span style='font-size:1.3em;'>&#10077;</span> <i>{historia['fala_personagem']}</i></div>", unsafe_allow_html=True)
            st.write(historia['continua'])

            st.caption(f"História {idx+1} de {len(historias)}")
            st.divider()

            # ----- Botão "Voltar ao Topo" -----
            col_bt_left, col_bt_right = st.columns([1, 5]) # Colunas para alinhar o botão
            with col_bt_left: # Coloque o botão numa coluna menor para ele não ocupar a largura toda
                if st.button("⬆️ Voltar ao Topo", key=f"top_button_{idx}"):
                    st.markdown(
                        """
                        <script>
                            window.parent.document.querySelector("section.main").scrollTo(0, 0);
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
else:
    st.info("Nenhuma história encontrada ou houve um erro ao carregar as histórias.")

# ---------- Rodapé opcional ----------
st.markdown("""
<div style='margin-top:2em;text-align:right;color:#9ca3af;font-size:0.95em'>
**Quer compartilhar sua história?** Escreva para: <a href='mailto:email@instituicao.org'>email@instituicao.org</a><br>
Projeto fictício para apresentação — 2024.
</div>
""", unsafe_allow_html=True)