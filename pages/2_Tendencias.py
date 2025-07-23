import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----- CONFIGURAÇÕES E ESTILOS -----
st.set_page_config(layout="wide", page_title="Tendências e Rankings da Produção")

st.markdown("""
    <style>
    /* ... (seus estilos podem ser mantidos aqui) ... */
    .big-font { font-size:2em !important; font-weight: bold; color: #24405a; }
    .medium-font { font-size:1.4em !important; font-weight: bold; color: #426b8c; }
    .small-font { font-size:0.9em !important; color: #6c757d; }
    .insight-box { background-color: #f0f8ff; border-left: 5px solid #007bff; padding: 1em; margin-bottom: 1.5em; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)


# ---- CARREGAR E PREPARAR DADOS -----
@st.cache_data
def carregar_dados_completos():
    try:
        df = pd.read_csv("data/familias_agricultoras.csv", sep=';', encoding='utf-8')
        df.columns = df.columns.str.strip()
        
        # Garantir colunas de localização (para o caso de arquivos sem elas)
        if "Estado" not in df.columns: df["Estado"] = "SE"
        if "Região" not in df.columns: df["Região"] = "Nordeste"

        # Limpeza e conversão de tipos
        numeric_cols = ['Ano', 'Volume Produção Anual (Kg)', 'Área Cultivada (ha)']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        df['Ano'] = df['Ano'].astype(int)
        
        # Criar métrica de produtividade
        # Usamos np.divide para evitar divisão por zero, resultando em 0
        df['Produtividade (Kg/ha)'] = np.divide(df['Volume Produção Anual (Kg)'], df['Área Cultivada (ha)'], 
                                             out=np.zeros_like(df['Volume Produção Anual (Kg)'], dtype=float), 
                                             where=df['Área Cultivada (ha)']!=0)

        return df.copy()
    except FileNotFoundError:
        st.error("Erro: O arquivo 'data/familias_agricultoras.csv' não foi encontrado.")
        return None
    except KeyError as e:
        st.error(f"Erro de processamento: a coluna {e} não foi encontrada no CSV. Verifique o arquivo e o separador (deve ser ';').")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar ou processar o arquivo CSV: {e}")
        return None

df = carregar_dados_completos()

if df is None:
    st.stop()

# --- TÍTULO E INTRODUÇÃO ---
st.markdown("<p class='big-font'>Análise de Desempenho e Tendências</p>", unsafe_allow_html=True)
st.markdown("""
<div class='insight-box'>
    Esta seção oferece uma análise aprofundada do desempenho da produção agrícola familiar. Compare itens, analise a eficiência e explore a evolução temporal para descobrir padrões e oportunidades.
</div>
""")

# --- SELETORES DE ANÁLISE ---
st.markdown("<p class='medium-font'>Selecione o que você quer explorar:</p>", unsafe_allow_html=True)
col_radio, col_select = st.columns([1, 2])

with col_radio:
    filtro_tipo = st.radio("Analisar por:", ["Município", "Produto", "Comunidade"], horizontal=True, label_visibility="collapsed")

col_map = {
    "Município": "Município",
    "Produto": "Item de Produção Principal",
    "Comunidade": "Comunidade"
}
col_filtro = col_map[filtro_tipo]
sub_titulo_grafico = filtro_tipo + "s"

with col_select:
    filtro_opcoes = sorted(df[col_filtro].dropna().unique())
    filtro_valor = st.selectbox(f"Escolha o {filtro_tipo.lower()} para analisar em detalhe", filtro_opcoes)


# --- NOVA SEÇÃO DE RANKINGS MULTIDIMENSIONAIS ---
st.markdown("---")
st.markdown(f"<p class='medium-font' style='margin-top: 25px;'>Análise de Performance de <i>{filtro_valor}</i></p>", unsafe_allow_html=True)

col_rank1, col_rank2, col_rank3 = st.columns(3, gap="large")

# Ranking 1: Por Volume Total (o principal)
with col_rank1:
    st.subheader("Ranking por Volume (Kg)")
    rk_volume = df.groupby(col_filtro)["Volume Produção Anual (Kg)"].sum().sort_values(ascending=False).reset_index()
    pos_volume = rk_volume[rk_volume[col_filtro] == filtro_valor].index[0] + 1
    
    st.metric(f"Posição de {filtro_valor}", f"{pos_volume}º", f"de {len(rk_volume)} {sub_titulo_grafico}")

    rk_volume["Destaque"] = rk_volume[col_filtro] == filtro_valor
    fig_vol = px.bar(
        rk_volume.head(10), x=col_filtro, y="Volume Produção Anual (Kg)",
        color="Destaque", color_discrete_map={True: "#E76F51", False: "#264653"},
        text_auto=True, title="Top 10 por Volume Total"
    )
    fig_vol.update_layout(showlegend=False, xaxis_title="", yaxis_title="Volume (kg)", height=400)
    st.plotly_chart(fig_vol, use_container_width=True)

# Ranking 2: Por Produtividade Média (Eficiência)
with col_rank2:
    st.subheader("Ranking por Produtividade (Kg/ha)")
    rk_produtividade = df.groupby(col_filtro)['Produtividade (Kg/ha)'].mean().sort_values(ascending=False).reset_index()
    pos_produtividade = rk_produtividade[rk_produtividade[col_filtro] == filtro_valor].index[0] + 1

    st.metric(f"Posição de {filtro_valor}", f"{pos_produtividade}º", f"de {len(rk_produtividade)} {sub_titulo_grafico}")

    rk_produtividade["Destaque"] = rk_produtividade[col_filtro] == filtro_valor
    fig_prod = px.bar(
        rk_produtividade.head(10), x=col_filtro, y="Produtividade (Kg/ha)",
        color="Destaque", color_discrete_map={True: "#E76F51", False: "#2a9d8f"},
        text_auto='.2f', title="Top 10 por Eficiência Média"
    )
    fig_prod.update_layout(showlegend=False, xaxis_title="", yaxis_title="Kg por Hectare", height=400)
    st.plotly_chart(fig_prod, use_container_width=True)

# Ranking 3: Por Número de Famílias (Capilaridade)
with col_rank3:
    st.subheader("Ranking por Nº de Famílias")
    rk_familias = df.groupby(col_filtro)['Nome da Família'].nunique().sort_values(ascending=False).reset_index()
    pos_familias = rk_familias[rk_familias[col_filtro] == filtro_valor].index[0] + 1

    st.metric(f"Posição de {filtro_valor}", f"{pos_familias}º", f"de {len(rk_familias)} {sub_titulo_grafico}")

    rk_familias["Destaque"] = rk_familias[col_filtro] == filtro_valor
    fig_fam = px.bar(
        rk_familias.head(10), x=col_filtro, y="Nome da Família",
        color="Destaque", color_discrete_map={True: "#E76F51", False: "#457b9d"},
        text_auto=True, title="Top 10 por Base de Produtores"
    )
    fig_fam.update_layout(showlegend=False, xaxis_title="", yaxis_title="Nº de Famílias", height=400)
    st.plotly_chart(fig_fam, use_container_width=True)

# --- NOVA ANÁLISE TEMPORAL COM ABAS ---
st.markdown("---")
st.markdown(f"<p class='medium-font' style='margin-top: 35px;'>📈 Análise de Desempenho ao Longo do Tempo para <i>{filtro_valor}</i></p>", unsafe_allow_html=True)

df_item_selecionado = df[df[col_filtro] == filtro_valor]

# Verifica se há dados suficientes
if df_item_selecionado.empty or df_item_selecionado['Ano'].nunique() < 2:
    st.warning(f"Não há dados históricos suficientes para analisar tendências de '{filtro_valor}'.")
else:
    tab1, tab2, tab3 = st.tabs(["Evolução Comparativa", "Crescimento Ano a Ano (YoY)", "Composição da Produção"])

    with tab1:
        # Gráfico Comparativo
        st.markdown("##### Como a produção de '{filtro_valor}' se compara com a média de seus pares?")
        
        # 1. Agrega dados para o item selecionado
        trend_selecionado = df_item_selecionado.groupby('Ano')['Volume Produção Anual (Kg)'].sum().reset_index()
        
        # 2. Calcula a média de produção por item/ano para todos os outros
        df_outros = df[df[col_filtro] != filtro_valor]
        trend_media_outros = df_outros.groupby(['Ano', col_filtro])['Volume Produção Anual (Kg)'].sum().reset_index()
        trend_media_geral = trend_media_outros.groupby('Ano')['Volume Produção Anual (Kg)'].mean().reset_index().rename(columns={'Volume Produção Anual (Kg)': 'Média dos Pares'})

        # 3. Plota os dois
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(x=trend_selecionado['Ano'], y=trend_selecionado['Volume Produção Anual (Kg)'], mode='lines+markers', name=filtro_valor, line=dict(color='#E76F51', width=4)))
        fig_comp.add_trace(go.Scatter(x=trend_media_geral['Ano'], y=trend_media_geral['Média dos Pares'], mode='lines', name='Média dos Pares', line=dict(color='#264653', dash='dash')))
        fig_comp.update_layout(title_text=f"Produção de '{filtro_valor}' vs. Média da Categoria", yaxis_title="Volume (Kg)", xaxis_title="Ano", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_comp, use_container_width=True)

    with tab2:
        # Crescimento Ano a Ano (YoY)
        st.markdown(f"##### Qual foi a variação da produção de '{filtro_valor}' a cada ano?")
        
        yoy_data = trend_selecionado.set_index('Ano').sort_index()
        yoy_data['YoY (%)'] = yoy_data['Volume Produção Anual (Kg)'].pct_change() * 100
        yoy_data = yoy_data.dropna()

        fig_yoy = px.bar(yoy_data, x=yoy_data.index, y='YoY (%)', text_auto='.1f', title=f"Crescimento Ano a Ano (YoY) para '{filtro_valor}'")
        fig_yoy.update_traces(marker_color=['#2a9d8f' if v > 0 else '#e76f51' for v in yoy_data['YoY (%)']])
        fig_yoy.update_layout(yaxis_title="Variação Percentual (%)", xaxis_title="Ano")
        st.plotly_chart(fig_yoy, use_container_width=True)

    with tab3:
        # Composição da Produção
        if filtro_tipo == "Produto":
            col_composicao = 'Município'
            titulo_comp = f"Quais municípios mais produziram '{filtro_valor}' a cada ano?"
        else:
            col_composicao = 'Item de Produção Principal'
            titulo_comp = f"Quais produtos mais se destacaram em '{filtro_valor}' a cada ano?"
            
        st.markdown(f"##### {titulo_comp}")
        
        comp_data = df_item_selecionado.groupby(['Ano', col_composicao])['Volume Produção Anual (Kg)'].sum().reset_index()
        top_items = comp_data.groupby(col_composicao)['Volume Produção Anual (Kg)'].sum().nlargest(5).index
        comp_data_top = comp_data[comp_data[col_composicao].isin(top_items)]

        fig_comp = px.bar(comp_data_top, x="Ano", y="Volume Produção Anual (Kg)", color=col_composicao, title=f"Composição da Produção de '{filtro_valor}' (Top 5)")
        fig_comp.update_layout(yaxis_title="Volume (Kg)", xaxis_title="Ano")
        st.plotly_chart(fig_comp, use_container_width=True)
