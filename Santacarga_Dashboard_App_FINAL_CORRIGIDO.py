
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Painel Santa Carga", layout="wide")

# CABEÇALHO
st.markdown("""
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <img src='https://raw.githubusercontent.com/RodrigoSantaCargaPerus/santacarga-assets/main/logo.png' width='100'>
        <h1 style='color: #1e392a;'>📊 Painel de Controle Santa Carga Perus</h1>
        <img src='https://raw.githubusercontent.com/RodrigoSantaCargaPerus/santacarga-assets/main/robo.png' width='100'>
    </div>
    <hr style='border: 1px solid #1e392a;'>
""", unsafe_allow_html=True)

st.markdown("### Bem-vindo ao painel oficial da Santa Carga ⚡")
st.markdown("Aqui você gerencia os anunciantes, monitora os planos, controla as despesas e treina seu vendedor virtual.")

# DADOS INICIAIS
if "anunciantes" not in st.session_state:
    st.session_state.anunciantes = pd.DataFrame([
        {"Nome": "Academia PanoBianco", "Totem": "Perus - PanoBianco", "Plano": "Anual Plus", "Valor Mensal": 547, "Início": "2024-06-01", "Vencimento": "2025-06-01", "Status": "Ativo"},
        {"Nome": "Ótica Zoom", "Totem": "Perus - Centro", "Plano": "Trimestral", "Valor Mensal": 397, "Início": "2024-06-01", "Vencimento": "2024-08-31", "Status": "Próximo do vencimento"},
    ])

if "despesas" not in st.session_state:
    st.session_state.despesas = pd.DataFrame([
        {"Descrição": "Energia Totem PanoBianco", "Categoria": "Energia", "Valor": 180, "Data": "2024-06-01"},
        {"Descrição": "Internet", "Categoria": "Serviço", "Valor": 120, "Data": "2024-06-01"},
    ])

anunciantes = st.session_state.anunciantes
despesas = st.session_state.despesas

# CONVERSÃO DE DATAS
anunciantes["Início"] = pd.to_datetime(anunciantes["Início"])
anunciantes["Vencimento"] = pd.to_datetime(anunciantes["Vencimento"])
anunciantes["Dias Restantes"] = (anunciantes["Vencimento"] - datetime.now()).dt.days
despesas["Data"] = pd.to_datetime(despesas["Data"])

# DASHBOARD FINANCEIRO
total = anunciantes["Valor Mensal"].sum()
total_despesas = despesas["Valor"].sum()
meta = 15000
lucro = total - total_despesas
porcentagem = (total / meta) * 100

col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento Mensal", f"R$ {total:,.2f}")
col2.metric("🎯 Meta Mensal", f"R$ {meta:,.2f}")
col3.metric("📈 Meta Atingida", f"{porcentagem:.1f}%")

col4, col5, col6 = st.columns(3)
col4.metric("📤 Total de Despesas", f"R$ {total_despesas:,.2f}")
col5.metric("💼 Lucro Mensal", f"R$ {lucro:,.2f}")
col6.metric("📊 Margem Lucro", f"{(lucro/meta)*100:.1f}%")

# GRÁFICOS
graf = px.bar(anunciantes, x="Nome", y="Valor Mensal", color="Plano", title="Faturamento por Cliente")
st.plotly_chart(graf, use_container_width=True)

graf2 = px.pie(pd.DataFrame({"Categoria": ["Faturamento", "Despesas"], "Valor": [total, total_despesas]}), names="Categoria", values="Valor", title="Faturamento vs Despesas")
st.plotly_chart(graf2, use_container_width=True)

# WHATSAPP VIRTUAL
st.header("🤖 WhatsApp Vendedor Virtual")
st.markdown("""
- Apresentar planos e preços  
- Tirar dúvidas comuns  
- Oferecer link para renovação  
- Agendar contato com humano  
""")
