import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ----- CONFIGURAÇÕES E ESTILOS (MELHORIA DE UX) -----
st.set_page_config(layout="wide", page_title="Tendências da Produção Orgânica")

st.markdown("""
    <style>
    .big-font {
        font-size:2em !important;
        font-weight: bold;
        color: #24405a;
    }
    .medium-font {
        font-size:1.4em !important;
        font-weight: bold;
        color: #426b8c;
    }
    .small-font {
        font-size:0.9em !important;
        color: #6c757d;
    }
    .insight-box {
        background-color: #e6f7ff; /* light blue for insights */
        border-left: 5px solid #007bff;
        padding: 1em;
        margin-bottom: 1.5em;
        border-radius: 5px;
        font-size: 1.05em;
    }
    .st-emotion-cache-nahz7x { /* Adjusts spacing between elements */
        gap: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


# ---- CARREGAR DADOS
try:
    df = pd.read_csv("data/familias_agricultoras.csv", sep=";", encoding='utf-8')
    df.columns = df.columns.str.strip()
    
    if "Estado" not in df.columns:
        df["Estado"] = "SE"
    if "Região" not in df.columns:
        df["Região"] = "Nordeste"

    if 'Ano' in df.columns:
        df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce').fillna(0).astype(int)
    
    required_cols = ["Município", "Item de Produção Principal", "Comunidade", "Volume Produção Anual (Kg)", "Ano", "Estado", "Região"]
    if not all(col in df.columns for col in required_cols):
        st.error("Erro: O arquivo CSV não contém todas as colunas necessárias.")
        st.stop()
        
except FileNotFoundError:
    st.error("Erro: O arquivo 'data/familias_agricultoras.csv' não foi encontrado. Certifique-se de que ele está na pasta 'data' no mesmo diretório do seu script.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao carregar ou processar o arquivo CSV: {e}")
    st.stop()


# --- TÍTULO E INTRODUÇÃO REVISADA ---
st.markdown("<p class='big-font'>Produção Orgânica Certificada na Agricultura Familiar</p>", unsafe_allow_html=True)
st.markdown("<p class='medium-font'>E o que eu tenho a ver com isso?</p>", unsafe_allow_html=True)

st.markdown("""
<div class='insight-box'>
    Aqui exploramos os números por trás do esforço e dedicação de quem alimenta nossa mesa com produtos orgânicos. Cada quilo colhido reflete o compromisso com a terra, o clima e a saúde de todos. Mergulhe nos dados para entender as tendências e o impacto da agricultura familiar em Sergipe e no Brasil.
</div>
""")

# --- SELECIONE UM FILTRO
st.markdown("<p class='medium-font'>Selecione o que você quer explorar:</p>", unsafe_allow_html=True)
filtro_tipo = st.radio(" ", ["Município", "Produto", "Comunidade"], horizontal=True, label_visibility="collapsed")

if filtro_tipo == "Município":
    col_filtro = "Município"
    sub_titulo_grafico = "Municípios"
    col_analise_secundaria = "Item de Produção Principal" # Para o novo gráfico
    titulo_analise_secundaria = "Principais Itens Produzidos"
elif filtro_tipo == "Produto":
    col_filtro = "Item de Produção Principal"
    sub_titulo_grafico = "Produtos"
    col_analise_secundaria = "Município" # Para o novo gráfico
    titulo_analise_secundaria = "Municípios Produtores"
else: # Comunidade
    col_filtro = "Comunidade"
    sub_titulo_grafico = "Comunidades"
    col_analise_secundaria = "Item de Produção Principal" # Para o novo gráfico
    titulo_analise_secundaria = "Principais Itens Produzidos"


filtro_opcoes = sorted(df[col_filtro].dropna().unique())
filtro_valor = st.selectbox(f"Escolha o {filtro_tipo.lower()} para analisar", filtro_opcoes)

if not df[df[col_filtro] == filtro_valor].empty:
    linha = df[df[col_filtro] == filtro_valor].iloc[0]
    estado = linha["Estado"]
    regiao = linha["Região"]
else:
    estado = "SE"
    regiao = "Nordeste"


# --- FUNÇÃO DE RANKING ---
def display_ranking(df_data, col_agrup, selected_value, filter_state=None, filter_region=None, ranking_name="Nacional"):
    
    df_filtered = df_data.copy()
    if filter_state:
        df_filtered = df_filtered[df_filtered["Estado"] == filter_state]
    if filter_region:
        df_filtered = df_filtered[df_filtered["Região"] == filter_region]

    if df_filtered.empty:
        st.info(f"Não há dados para o ranking {ranking_name} com o filtro atual.")
        return

    rk = df_filtered.groupby(col_agrup)["Volume Produção Anual (Kg)"].sum().sort_values(ascending=False).reset_index()
    
    rk["Destaque"] = rk[col_agrup] == selected_value
    
    top10 = rk.head(10)
    if selected_value not in top10[col_agrup].values:
        selected_row = rk[rk[col_agrup] == selected_value]
        if not selected_row.empty:
            top10 = pd.concat([top10, selected_row]).drop_duplicates(subset=[col_agrup])
            top10 = top10.sort_values(by="Volume Produção Anual (Kg)", ascending=False)

    fig = px.bar(
        top10,
        x=col_agrup, y="Volume Produção Anual (Kg)",
        color="Destaque", 
        color_discrete_map={True: "#E76F51", False: "#264653"},
        text="Volume Produção Anual (Kg)",
        title=f"Ranking {ranking_name} de {sub_titulo_grafico}"
    )
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Volume (kg)", title_font_size=18)
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    try:
        pos = rk[rk[col_agrup] == selected_value].index[0] + 1
        total_items = len(rk)
        st.markdown(f"<p class='small-font'>O <b>{filtro_tipo} {selected_value}</b> está na <b>{pos}ª posição</b> de {total_items} no ranking <b>{ranking_name}</b>, mostrando seu impacto na produção orgânica.</p>", unsafe_allow_html=True)
    except IndexError:
        st.info(f"O {filtro_tipo} **{selected_value}** não possui dados suficientes para ser classificado no ranking {ranking_name}.")


# ------------------ RANKINGS EM COLUNAS ------------------
st.markdown("---")
st.markdown("<p class='medium-font' style='margin-top: 25px;'>Posicionamento nos Rankings</p>", unsafe_allow_html=True)

col_rank1, col_rank2, col_rank3 = st.columns(3)

with col_rank1:
    display_ranking(df, col_filtro, filtro_valor, ranking_name="Nacional")

with col_rank2:
    display_ranking(df, col_filtro, filtro_valor, filter_state=estado, ranking_name=f"Estadual ({estado})")

with col_rank3:
    display_ranking(df, col_filtro, filtro_valor, filter_region=regiao, ranking_name=f"Regional ({regiao})")


# ------------------ TENDÊNCIAS - SÉRIE TEMPORAL ------------------
st.markdown("---")
st.markdown("<p class='medium-font' style='margin-top: 35px;'>📈 Evolução Histórica (Série Temporal)</p>", unsafe_allow_html=True)

df_trend = df[df[col_filtro] == filtro_valor].copy()
df_trend_agg = df_trend.groupby("Ano")["Volume Produção Anual (Kg)"].sum().reset_index()
df_trend_agg = df_trend_agg.sort_values("Ano")

if df_trend_agg.empty or len(df_trend_agg) < 2:
    st.warning(f"Não há dados históricos suficientes para analisar tendências de '{filtro_valor}' ou há menos de 2 anos de dados.")
else:
    ano_inicio = df_trend_agg["Ano"].min()
    ano_fim = df_trend_agg["Ano"].max()
    prod_inicio = df_trend_agg.iloc[0]["Volume Produção Anual (Kg)"]
    prod_fim = df_trend_agg.iloc[-1]["Volume Produção Anual (Kg)"]
    
    crescimento = ((prod_fim - prod_inicio) / prod_inicio * 100) if prod_inicio > 0 else 0
    crescimento = round(crescimento, 1)

    ano_pico = df_trend_agg.iloc[df_trend_agg["Volume Produção Anual (Kg)"].idxmax()]["Ano"]
    ano_vale = df_trend_agg.iloc[df_trend_agg["Volume Produção Anual (Kg)"].idxmin()]["Ano"]

    if crescimento > 0:
        cor = "#2a9d8f"
        simbolo = "▲"
        tendencia_txt = "Crescimento notável"
    elif crescimento < 0:
        cor = "#e76f51"
        simbolo = "▼"
        tendencia_txt = "Queda observada"
    else:
        cor = "#6c757d"
        simbolo = "▬"
        tendencia_txt = "Estabilidade"

    st.markdown(f"""
    <div style="padding:1em;background-color:#f8f9fa;border-radius:8px;border-left:8px solid {cor};font-size:1.15em; margin-bottom:25px;">
        <b>{tendencia_txt} no período {ano_inicio}-{ano_fim}:</b> <span style="color:{cor};font-size:1.2em">{simbolo} {crescimento:.1f}%</span>
        <br>
        Volume inicial: <b>{int(prod_inicio):,} kg</b> &nbsp; | &nbsp;
        Volume final: <b>{int(prod_fim):,} kg</b>
        <br>
        <i>Pico de produção em {ano_pico}. Menor produção em {ano_vale}.</i>
    </div>
    """, unsafe_allow_html=True)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_trend_agg["Ano"], y=df_trend_agg["Volume Produção Anual (Kg)"],
        mode="lines+markers", name=f"{filtro_valor}",
        line=dict(color="#264653", width=3), marker=dict(size=10)
    ))

    if len(df_trend_agg) >= 3:
        z = np.polyfit(df_trend_agg["Ano"], df_trend_agg["Volume Produção Anual (Kg)"], 1)
        p = np.poly1d(z)
        fig_line.add_trace(go.Scatter(
            x=df_trend_agg["Ano"],
            y=p(df_trend_agg["Ano"]),
            mode="lines",
            line=dict(color="#E76F51", dash="dash"),
            name="Tendência Linear"
        ))

    fig_line.update_layout(
        yaxis_title="Volume Produção Anual (kg)",
        xaxis_title="Ano",
        template="plotly_white",
        legend_title="",
        height=430,
        title_text=f"Evolução Anual da Produção de {filtro_valor}",
        title_font_size=18
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
        <div class='insight-box'>
            Acompanhar a evolução anual é crucial para entender o impacto de fatores como o clima, novas técnicas de cultivo e políticas de incentivo à produção orgânica. Observe os anos de maior e menor produção.
        </div>
    """, unsafe_allow_html=True)


# ------------------ NOVO GRÁFICO: DISTRIBUIÇÃO DE PRODUÇÃO (AGORA SIM, HORIZONTAL) ------------------
st.markdown("---")
st.markdown(f"<p class='medium-font' style='margin-top:35px;'>📊 {titulo_analise_secundaria} para {filtro_valor}</p>", unsafe_allow_html=True)

df_distribuicao = df[df[col_filtro] == filtro_valor].copy()

if df_distribuicao.empty:
    st.warning(f"Não há dados para exibir a distribuição de produção para '{filtro_valor}'.")
else:
    # Agrupa por col_analise_secundaria e soma o volume
    # Ordena pelo volume em ordem crescente para que o maior fique no topo das barras horizontais
    df_grouped_dist = df_distribuicao.groupby(col_analise_secundaria)["Volume Produção Anual (Kg)"].sum().sort_values(ascending=True).reset_index()

    if df_grouped_dist.empty:
         st.warning(f"Não há dados para exibir a distribuição de produção para '{filtro_valor}'.")
    else:
        # Aqui está a correção principal: x é o volume, y é a categoria
        fig_dist = px.bar(
            df_grouped_dist,
            x="Volume Produção Anual (Kg)", # Volume no eixo X (horizontal)
            y=col_analise_secundaria,       # Categoria no eixo Y (vertical)
            orientation='h',                # Garante que as barras sejam horizontais
            text="Volume Produção Anual (Kg)",
            color_discrete_sequence=["#2a9d8f"],
            title=f"Distribuição de Produção por {col_analise_secundaria} para {filtro_valor}"
        )
        fig_dist.update_layout(
            xaxis_title="Volume Produção Anual (kg)",
            yaxis_title=col_analise_secundaria, # Rótulo do eixo Y
            showlegend=False,
            height=min(500, len(df_grouped_dist) * 40 + 100),
            title_font_size=18
        )
        fig_dist.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig_dist, use_container_width=True)

        st.markdown(f"""
            <div class='insight-box'>
                Este gráfico mostra a diversidade e o foco da produção de {filtro_valor}. Analisar os principais {col_analise_secundaria.lower()} ajuda a entender as vocações locais e onde o investimento e apoio podem ter maior impacto.
            </div>
        """, unsafe_allow_html=True)


# ---------- Rodapé opcional ----------
st.markdown("""
<div style='margin-top:2em;text-align:right;color:#9ca3af;font-size:0.95em'>
Projeto fictício para apresentação — 2024.<br>
Contato: <a href='mailto:email@instituicao.org'>email@instituicao.org</a>
</div>
""", unsafe_allow_html=True)