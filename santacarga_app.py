import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Título
st.set_page_config(page_title="Painel Santa Carga", layout="wide")
st.title("📊 Painel de Controle Santa Carga Perus")

# Dados fictícios iniciais
if "anunciantes" not in st.session_state:
    st.session_state.anunciantes = pd.DataFrame([
        {"Nome": "Academia PanoBianco", "Totem": "Perus - PanoBianco", "Plano": "Anual Plus", "Valor Mensal": 547, "Início": "2024-06-01", "Vencimento": "2025-06-01", "Status": "Ativo"},
        {"Nome": "Ótica Zoom", "Totem": "Perus - Centro", "Plano": "Trimestral", "Valor Mensal": 397, "Início": "2024-06-01", "Vencimento": "2024-08-31", "Status": "Próximo do vencimento"},
    ])

anunciantes = st.session_state.anunciantes

# Conversões de datas
anunciantes["Início"] = pd.to_datetime(anunciantes["Início"])
anunciantes["Vencimento"] = pd.to_datetime(anunciantes["Vencimento"])
anunciantes["Dias Restantes"] = (anunciantes["Vencimento"] - datetime.now()).dt.days

# Cálculo do total e meta
total = anunciantes["Valor Mensal"].sum()
meta = 15000
porcentagem = (total / meta) * 100

# Layout em colunas
col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento Mensal", f"R$ {total:,.2f}")
col2.metric("🎯 Meta Mensal", f"R$ {meta:,.2f}")
col3.metric("📈 Meta Atingida", f"{porcentagem:.1f}%")

# Gráfico
graf = px.bar(anunciantes, x="Nome", y="Valor Mensal", color="Plano", title="Distribuição de Faturamento por Cliente")
st.plotly_chart(graf, use_container_width=True)

# Tabela com mensagens automáticas
st.subheader("🔔 Controle de Vencimento e Mensagens")
def gerar_mensagem(row):
    if row["Dias Restantes"] <= 15:
        return f"Olá {row['Nome']}, sua veiculação está prestes a vencer. Vamos renovar?"
    return "—"
anunciantes["Mensagem WhatsApp"] = anunciantes.apply(gerar_mensagem, axis=1)

# Filtro por plano ou status
with st.expander("🔍 Filtrar anunciantes"):
    plano_opcao = st.multiselect("Filtrar por plano", anunciantes["Plano"].unique())
    status_opcao = st.multiselect("Filtrar por status", anunciantes["Status"].unique())
    filtrado = anunciantes
    if plano_opcao:
        filtrado = filtrado[filtrado["Plano"].isin(plano_opcao)]
    if status_opcao:
        filtrado = filtrado[filtrado["Status"].isin(status_opcao)]
    st.dataframe(filtrado)

# Formulário para novo cadastro
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

# Rodapé
st.caption("Desenvolvido para Santa Carga Perus 🚀")