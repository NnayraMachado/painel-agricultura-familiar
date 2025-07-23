import streamlit as st

def ficha_tecnica(row):
    st.markdown(f"""
    ## FICHA TÉCNICA

    **Nome:** {row['Nome da Família']}  
    **Município:** {row['Município']}  
    **Comunidade:** {row['Comunidade']}  
    **Gênero Responsável:** {row['Gênero Responsável']}  
    **Item de Produção Principal:** {row['Item de Produção Principal']}  
    **Produção Secundária:** {row['Item de Produção Secundário']}  
    **Certificação:** {row['Tipo de Certificação']}  
    **Área Cultivada (ha):** {row['Área Cultivada (ha)']}  
    **Volume Produção Anual (Kg):** {row['Volume Produção Anual (Kg)']}  
    **Método de Venda Principal:** {row['Método de Venda Principal']}  
    **Associação/Cooperativa:** {row['Associação/Cooperativa']}  
    **Telefone:** {row['Telefone']}  
    **Email:** {row['Email']}  
    """)
