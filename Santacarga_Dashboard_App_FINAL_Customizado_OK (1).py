
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Personalização visual
st.set_page_config(page_title="Painel Santa Carga", layout="wide")

st.markdown(
    '''
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <img src="https://raw.githubusercontent.com/RodrigoSantaCargaPerus/santacarga-assets/main/santacarga_logo_otimizado.png" width="120">
        <h1 style="color:#1e392a;">📊 Painel de Controle Santa Carga Perus</h1>
        <img src="https://raw.githubusercontent.com/RodrigoSantaCargaPerus/santacarga-assets/main/santacarga_mascote_otimizado.png" width="120">
    </div>
    <hr style='border: 1px solid #1e392a;'>
    ''',
    unsafe_allow_html=True
)

# Conteúdo do painel principal - exemplo
st.subheader("Bem-vindo ao painel oficial da Santa Carga ⚡")
st.write("Aqui você gerencia os anunciantes, monitora os planos, controla as despesas e treina seu vendedor virtual.")

# Seção para exemplo do WhatsApp Bot
st.header("🤖 WhatsApp Vendedor Virtual")
st.markdown("""
Este é o início do módulo de integração com um atendente automático no WhatsApp. Ele poderá:
- Apresentar planos e preços
- Tirar dúvidas comuns
- Oferecer link para renovação ou pagamento
- Agendar contato com humano

Este módulo será conectado com ferramentas como Z-API ou Weni.
""")
