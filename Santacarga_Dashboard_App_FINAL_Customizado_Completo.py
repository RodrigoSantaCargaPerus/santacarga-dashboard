
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Painel Santa Carga", layout="wide")

# Cabeçalho com logo e mascote
st.markdown("""
<div style='display: flex; align-items: center; justify-content: space-between; background-color: #1e392a; padding: 10px; border-radius: 10px;'>
    <img src='https://sandbox:/mnt/data/Captura de tela 2025-05-30 190954.png' width='100'>
    <h1 style='color: white;'>📊 Painel de Controle - Santa Carga Perus</h1>
    <img src='https://sandbox:/mnt/data/Captura de tela 2025-06-02 171834.png' width='100'>
</div>
<hr>
""", unsafe_allow_html=True)

# Carregamento inicial dos anunciantes
if "anunciantes" not in st.session_state:
    st.session_state.anunciantes = pd.DataFrame([
        {"Nome": "Academia PanoBianco", "Totem": "Perus - PanoBianco", "Plano": "Anual Plus", "Valor Mensal": 547, "Início": "2024-06-01", "Vencimento": "2025-06-01", "Status": "Ativo"},
        {"Nome": "Ótica Zoom", "Totem": "Perus - Centro", "Plano": "Trimestral", "Valor Mensal": 397, "Início": "2024-06-01", "Vencimento": "2024-08-31", "Status": "Próximo do vencimento"},
    ])

anunciantes = st.session_state.anunciantes
anunciantes["Início"] = pd.to_datetime(anunciantes["Início"])
anunciantes["Vencimento"] = pd.to_datetime(anunciantes["Vencimento"])
anunciantes["Dias Restantes"] = (anunciantes["Vencimento"] - datetime.now()).dt.days

# KPIs principais
faturamento = anunciantes["Valor Mensal"].sum()
meta = 15000
pct_meta = (faturamento / meta) * 100

c1, c2, c3 = st.columns(3)
c1.metric("💰 Faturamento Atual", f"R$ {faturamento:,.2f}")
c2.metric("🎯 Meta Mensal", f"R$ {meta:,.2f}")
c3.metric("📈 Progresso", f"{pct_meta:.1f}%")

# Gráfico de faturamento
graf1 = px.bar(anunciantes, x="Nome", y="Valor Mensal", color="Plano", title="Faturamento por Anunciante")
st.plotly_chart(graf1, use_container_width=True)

# Controle de vencimento e alertas
st.subheader("🔔 Controle de Vencimentos")
def msg(row):
    return f"🚨 {row['Nome']} precisa renovar!" if row["Dias Restantes"] <= 15 else "✅ Ativo"
anunciantes["Alerta"] = anunciantes.apply(msg, axis=1)
st.dataframe(anunciantes)

# Novo cadastro
st.subheader("➕ Novo Anunciante")
with st.form("add_anunciante"):
    nome = st.text_input("Nome")
    totem = st.text_input("Totem")
    plano = st.selectbox("Plano", ["Mensal", "Trimestral", "Semestral", "Anual", "Anual Plus"])
    valor = st.number_input("Valor Mensal", 0.0)
    inicio = st.date_input("Início")
    venc = st.date_input("Vencimento")
    enviar = st.form_submit_button("Cadastrar")
    if enviar:
        novo = {
            "Nome": nome, "Totem": totem, "Plano": plano, "Valor Mensal": valor,
            "Início": pd.to_datetime(inicio), "Vencimento": pd.to_datetime(venc),
            "Dias Restantes": (venc - datetime.now().date()).days,
            "Status": "Ativo"
        }
        st.session_state.anunciantes = pd.concat([st.session_state.anunciantes, pd.DataFrame([novo])], ignore_index=True)
        st.success("✅ Anunciante cadastrado com sucesso!")

# Controle de despesas
st.header("📉 Despesas")
if "despesas" not in st.session_state:
    st.session_state.despesas = pd.DataFrame([
        {"Descrição": "Energia Totem", "Categoria": "Energia", "Valor": 180, "Data": "2024-06-01"},
        {"Descrição": "Internet", "Categoria": "Serviço", "Valor": 120, "Data": "2024-06-01"}
    ])

despesas = st.session_state.despesas
despesas["Data"] = pd.to_datetime(despesas["Data"])
total_despesas = despesas["Valor"].sum()
lucro = faturamento - total_despesas

c4, c5, c6 = st.columns(3)
c4.metric("📤 Despesas", f"R$ {total_despesas:,.2f}")
c5.metric("💼 Lucro", f"R$ {lucro:,.2f}")
c6.metric("📊 Margem", f"{(lucro/meta)*100:.1f}%")

# Gráfico comparativo
graf2 = px.pie(pd.DataFrame({"Categoria": ["Faturamento", "Despesas"], "Valor": [faturamento, total_despesas]}),
               names="Categoria", values="Valor", title="Faturamento vs Despesas")
st.plotly_chart(graf2, use_container_width=True)

# Adicionar nova despesa
st.subheader("➕ Nova Despesa")
with st.form("add_despesa"):
    desc = st.text_input("Descrição")
    cat = st.selectbox("Categoria", ["Energia", "Serviço", "Manutenção", "Outros"])
    val = st.number_input("Valor", 0.0)
    data = st.date_input("Data da Despesa")
    enviar_d = st.form_submit_button("Adicionar")
    if enviar_d:
        nova_d = {"Descrição": desc, "Categoria": cat, "Valor": val, "Data": pd.to_datetime(data)}
        st.session_state.despesas = pd.concat([st.session_state.despesas, pd.DataFrame([nova_d])], ignore_index=True)
        st.success("✅ Despesa adicionada!")

st.markdown("---")
st.caption("© 2025 Santa Carga Perus | Painel desenvolvido com ❤️ e dados!")
