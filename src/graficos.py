import streamlit as st
import plotly.express as px

def graficos_principais(df):
    st.markdown("")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top 10 Produtos por Volume Anual**")
        prod = df.groupby('Item de Produção Principal')["Volume Produção Anual (Kg)"].sum().sort_values(ascending=False).reset_index()
        fig1 = px.bar(prod.head(10), y="Item de Produção Principal", x="Volume Produção Anual (Kg)",
                      color="Item de Produção Principal", orientation="h", text="Volume Produção Anual (Kg)")
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.markdown("**Distribuição dos Gêneros Responsáveis**")
        fig2 = px.pie(df, names="Gênero Responsável", title=None, hole=0.5)
        fig2.update_traces(textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("**Top 10 Municípios por Volume Anual**")
    mun = df.groupby('Município')["Volume Produção Anual (Kg)"].sum().sort_values(ascending=False).reset_index()
    fig3 = px.bar(mun.head(10), x="Município", y="Volume Produção Anual (Kg)", color="Município", text="Volume Produção Anual (Kg)")
    fig3.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig3, use_container_width=True)
