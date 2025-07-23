# Em src/filtros.py

import streamlit as st
import pandas as pd

def filtros_menu(df: pd.DataFrame):
    """
    Cria e gerencia os filtros na barra lateral usando callbacks para uma limpeza de estado segura.
    """
    st.sidebar.header("🔍 Filtros para Buscar")

    # --- NOVO: Função de Callback ---
    # Esta função será chamada ANTES da página recarregar quando o botão for clicado.
    def limpar_filtros_callback():
        """Reseta todos os valores dos filtros no session_state."""
        keys_to_clear = [
            'filtro_busca', 'filtro_municipio', 'filtro_produto',
            'filtro_certificacao', 'filtro_genero', 'filtro_comunidade'
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                # Reseta para os valores padrão
                if key == 'filtro_busca':
                    st.session_state[key] = ""
                else:
                    st.session_state[key] = "Todos"

    # --- WIDGETS DE FILTRO ---
    # Usamos o `st.session_state` para manter o estado dos filtros.
    # Isso é crucial para que o botão de limpar funcione corretamente.

    busca = st.sidebar.text_input(
        "Busca (família, produto, município...)",
        value=st.session_state.get('filtro_busca', ''), # Pega o valor ou um padrão
        key='filtro_busca' # Chave para o session_state
    )

    municipio = st.sidebar.selectbox(
        "Município",
        options=["Todos"] + sorted(df["Município"].unique().tolist()),
        key='filtro_municipio'
    )

    produto = st.sidebar.selectbox(
        "Produção Principal",
        options=["Todos"] + sorted(df["Item de Produção Principal"].unique().tolist()),
        key='filtro_produto'
    )

    certificacao = st.sidebar.selectbox(
        "Certificação",
        options=["Todos"] + sorted(df["Tipo de Certificação"].unique().tolist()),
        key='filtro_certificacao'
    )

    genero = st.sidebar.selectbox(
        "Gênero Responsável",
        options=["Todos"] + sorted(df["Gênero Responsável"].unique().tolist()),
        key='filtro_genero'
    )

    comunidade = st.sidebar.selectbox(
        "Comunidade",
        options=["Todos"] + sorted(df["Comunidade"].unique().tolist()),
        key='filtro_comunidade'
    )

    # --- ALTERADO: Botão com Callback ---
    # Removemos o `if` e adicionamos o argumento `on_click`.
    st.sidebar.button(
        "🧹 Limpar filtros",
        on_click=limpar_filtros_callback, # A mágica acontece aqui!
        use_container_width=True
    )

    return busca, municipio, produto, certificacao, genero, comunidade


def aplicar_filtros(df: pd.DataFrame, busca, municipio, produto, certificacao, genero, comunidade):
    """Aplica os filtros selecionados ao DataFrame."""
    df_filtrado = df.copy()

    if busca:
        # Busca em múltiplas colunas de forma insensível a maiúsculas/minúsculas
        df_filtrado = df_filtrado[
            df_filtrado.apply(lambda row: busca.lower() in str(row).lower(), axis=1)
        ]

    if municipio != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Município"] == municipio]

    if produto != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Item de Produção Principal"] == produto]

    if certificacao != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Tipo de Certificação"] == certificacao]

    if genero != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Gênero Responsável"] == genero]

    if comunidade != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Comunidade"] == comunidade]

    return df_filtrado
