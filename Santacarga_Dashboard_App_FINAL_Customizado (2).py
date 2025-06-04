import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configurações da página
st.set_page_config(page_title="Painel Santa Carga", layout="wide")

# Cabeçalho com logo e mascote
st.markdown("""
    <div style='display: flex; align-items: center; justify-content: space-between; background-color: #1e392a; padding: 10px; border-radius: 10px;'>
        <img src="https://raw.githubusercontent.com/RodrigoSantaCargaPerus/santacarga-dashboard/main/assets/logo.png" width="100">
        <h1 style='color: white;'>📊 Painel de Controle Santa Carga Perus</h1>
        <img src="https://raw.githubusercontent.com/RodrigoSantaCargaPerus/santacarga-dashboard/main/assets/mascote.png" width="100">
    </div>
""", unsafe_allow_html=True)

# Sessão de boas-vindas
st.markdown("### Bem-vindo ao painel oficial da Santa Carga ⚡")
st.markdown("Aqui você gerencia os anunciantes, monitora os planos, controla as despesas e treina seu vendedor virtual.")

# Dados fictícios de anunciantes
if "anunciantes" not in st.session_state:
    st.session_state.anunciantes = pd.DataFrame([
        {"Nome": "Academia PanoBianco", "Totem": "Perus - PanoBianco", "Plano": "Anual Plus", "Valor Mensal": 547, "Início": "2024-06-01", "Vencimento": "2025-06-01", "Status": "Ativo"},
        {"Nome": "Ótica Zoom", "Totem": "Perus - Centro", "Plano": "Trimestral", "Valor Mensal": 397, "Início": "2024-06-01", "Vencimento": "2024-08-31", "Status": "Próximo do vencimento"},
    ])

anunciantes = st.session_state.anunciantes
anunciantes["Início"] = pd.to_datetime(anunciantes["Início"])
anunciantes["Vencimento"] = pd.to_datetime(anunciantes["Vencimento"])
anunciantes["Dias Restantes"] = (anunciantes["Vencimento"] - datetime.now()).dt.days

total = anunciantes["Valor Mensal"].sum()
meta = 15000
porcentagem = (total / meta) * 100

# Indicadores
col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento Mensal", f"R$ {total:,.2f}")
col2.metric("🎯 Meta Mensal", f"R$ {meta:,.2f}")
col3.metric("📈 Meta Atingida", f"{porcentagem:.1f}%")

# Gráfico
graf = px.bar(anunciantes, x="Nome", y="Valor Mensal", color="Plano", title="Faturamento por Cliente")
st.plotly_chart(graf, use_container_width=True)

# Tabela e filtros
st.subheader("🔍 Anunciantes e Mensagens")
def gerar_mensagem(row):
    if row["Dias Restantes"] <= 15:
        return f"Olá {row['Nome']}, sua veiculação está prestes a vencer. Vamos renovar?"
    return "—"
anunciantes["Mensagem"] = anunciantes.apply(gerar_mensagem, axis=1)
st.dataframe(anunciantes)

# Cadastro
st.subheader("➕ Cadastrar novo anunciante")
with st.form("novo_anunciante"):
    nome = st.text_input("Nome do Anunciante")
    totem = st.text_input("Local do Totem")
    plano = st.selectbox("Plano", ["Mensal", "Trimestral", "Semestral", "Anual", "Anual Plus"])
    valor = st.number_input("Valor Mensal (R$)", min_value=0.0, format="%.2f")
    inicio = st.date_input("Data de Início")
    vencimento = st.date_input("Data de Vencimento")
    enviado = st.form_submit_button("Cadastrar")
    if enviado:
        novo = {"Nome": nome, "Totem": totem, "Plano": plano, "Valor Mensal": valor,
                "Início": pd.to_datetime(inicio), "Vencimento": pd.to_datetime(vencimento),
                "Status": "Ativo", "Dias Restantes": (vencimento - datetime.now().date()).days}
        st.session_state.anunciantes = pd.concat([st.session_state.anunciantes, pd.DataFrame([novo])], ignore_index=True)
        st.success("✅ Anunciante cadastrado com sucesso!")

# Controle de despesas
st.header("📉 Controle de Despesas")
if "despesas" not in st.session_state:
    st.session_state.despesas = pd.DataFrame([
        {"Descrição": "Energia Totem PanoBianco", "Categoria": "Energia", "Valor": 180, "Data": "2024-06-01"},
        {"Descrição": "Internet", "Categoria": "Serviço", "Valor": 120, "Data": "2024-06-01"},
    ])

despesas = st.session_state.despesas
despesas["Data"] = pd.to_datetime(despesas["Data"])
total_despesas = despesas["Valor"].sum()
lucro = total - total_despesas

col4, col5, col6 = st.columns(3)
col4.metric("📤 Total de Despesas", f"R$ {total_despesas:,.2f}")
col5.metric("💼 Lucro Mensal", f"R$ {lucro:,.2f}")
col6.metric("📊 Margem Lucro", f"{(lucro/meta)*100:.1f}%")

# Adicionar despesa
st.subheader("➕ Adicionar nova despesa")
with st.form("nova_despesa"):
    desc = st.text_input("Descrição")
    cat = st.selectbox("Categoria", ["Energia", "Serviço", "Manutenção", "Outros"])
    val = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    data = st.date_input("Data")
    enviar_despesa = st.form_submit_button("Adicionar")
    if enviar_despesa:
        nova = {"Descrição": desc, "Categoria": cat, "Valor": val, "Data": pd.to_datetime(data)}
        st.session_state.despesas = pd.concat([st.session_state.despesas, pd.DataFrame([nova])], ignore_index=True)
        st.success("✅ Despesa adicionada com sucesso!")

# Rodapé
st.caption("Desenvolvido para Santa Carga Perus 🚀")
