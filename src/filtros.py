import streamlit as st

def filtros_menu(df):
    st.markdown("### 🔎 Filtros para Buscar Famílias e Produção")

    # Obtém do session_state ou define padrão
    busca = st.session_state.get("menu_busca", "")
    municipio = st.session_state.get("menu_municipio", "Todos")
    produto = st.session_state.get("menu_produto", "Todos")
    certificacao = st.session_state.get("menu_certificacao", "Todos")
    genero = st.session_state.get("menu_genero", "Todos")
    comunidade = st.session_state.get("menu_comunidade", "Todos")

    # Trava: só deixa um filtro ativo (exceto busca)
    trava_municipio = municipio != "Todos"
    trava_produto = produto != "Todos"
    trava_certificacao = certificacao != "Todos"
    trava_genero = genero != "Todos"
    trava_comunidade = comunidade != "Todos"
    n_filtros = sum([trava_municipio, trava_produto, trava_certificacao, trava_genero, trava_comunidade])
    
    bloqueia_geral = n_filtros > 0

    col1, col2, col3 = st.columns([2,2,2])
    col4, col5, col6 = st.columns([2,2,2])

    with col1:
        busca = st.text_input("Busca (família, produto, município...)", value=busca, key="menu_busca", disabled=bloqueia_geral)
    with col2:
        municipio = st.selectbox(
            "Município",
            ["Todos"] + sorted(df["Município"].fillna("Indefinido").astype(str).unique().tolist()),
            index=(["Todos"] + sorted(df["Município"].fillna("Indefinido").astype(str).unique().tolist())).index(municipio) if municipio in (["Todos"] + sorted(df["Município"].fillna("Indefinido").astype(str).unique().tolist())) else 0,
            key="menu_municipio",
            disabled=not (municipio == "Todos" or not bloqueia_geral)
        )
    with col3:
        produto = st.selectbox(
            "Produção Principal",
            ["Todos"] + sorted(df["Item de Produção Principal"].fillna("Indefinido").astype(str).unique().tolist()),
            index=(["Todos"] + sorted(df["Item de Produção Principal"].fillna("Indefinido").astype(str).unique().tolist())).index(produto) if produto in (["Todos"] + sorted(df["Item de Produção Principal"].fillna("Indefinido").astype(str).unique().tolist())) else 0,
            key="menu_produto",
            disabled=not (produto == "Todos" or not bloqueia_geral)
        )
    with col4:
        certificacao = st.selectbox(
            "Certificação",
            ["Todos"] + sorted(df["Tipo de Certificação"].fillna("Indefinido").astype(str).unique().tolist()),
            index=(["Todos"] + sorted(df["Tipo de Certificação"].fillna("Indefinido").astype(str).unique().tolist())).index(certificacao) if certificacao in (["Todos"] + sorted(df["Tipo de Certificação"].fillna("Indefinido").astype(str).unique().tolist())) else 0,
            key="menu_certificacao",
            disabled=not (certificacao == "Todos" or not bloqueia_geral)
        )
    with col5:
        genero = st.selectbox(
            "Gênero Responsável",
            ["Todos"] + sorted(df["Gênero Responsável"].fillna("Indefinido").astype(str).unique().tolist()),
            index=(["Todos"] + sorted(df["Gênero Responsável"].fillna("Indefinido").astype(str).unique().tolist())).index(genero) if genero in (["Todos"] + sorted(df["Gênero Responsável"].fillna("Indefinido").astype(str).unique().tolist())) else 0,
            key="menu_genero",
            disabled=not (genero == "Todos" or not bloqueia_geral)
        )
    with col6:
        comunidade = st.selectbox(
            "Comunidade",
            ["Todos"] + sorted(df["Comunidade"].fillna("Indefinido").astype(str).unique().tolist()),
            index=(["Todos"] + sorted(df["Comunidade"].fillna("Indefinido").astype(str).unique().tolist())).index(comunidade) if comunidade in (["Todos"] + sorted(df["Comunidade"].fillna("Indefinido").astype(str).unique().tolist())) else 0,
            key="menu_comunidade",
            disabled=not (comunidade == "Todos" or not bloqueia_geral)
        )

    # Botão limpar
    limpar = st.button("🧹 Limpar filtros")
    if limpar:
        st.session_state.menu_busca = ""
        st.session_state.menu_municipio = "Todos"
        st.session_state.menu_produto = "Todos"
        st.session_state.menu_certificacao = "Todos"
        st.session_state.menu_genero = "Todos"
        st.session_state.menu_comunidade = "Todos"
        st.experimental_rerun()

    return busca, municipio, produto, certificacao, genero, comunidade

def aplicar_filtros(df, busca, municipio, produto, certificacao, genero, comunidade):
    df_filtrado = df.copy()
    if busca:
        busca = busca.lower()
        df_filtrado = df_filtrado[df_filtrado.apply(lambda row: busca in " ".join([str(val).lower() for val in row]), axis=1)]
    if municipio != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Município"].fillna("Indefinido").astype(str) == municipio]
    if produto != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Item de Produção Principal"].fillna("Indefinido").astype(str) == produto]
    if certificacao != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Tipo de Certificação"].fillna("Indefinido").astype(str) == certificacao]
    if genero != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Gênero Responsável"].fillna("Indefinido").astype(str) == genero]
    if comunidade != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Comunidade"].fillna("Indefinido").astype(str) == comunidade]
    return df_filtrado
