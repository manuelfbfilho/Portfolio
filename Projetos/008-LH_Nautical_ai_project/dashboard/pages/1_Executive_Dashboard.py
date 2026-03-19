import streamlit as st
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.filters import aplicar_filtros
from utils.metrics import calcular_kpis
from utils.ui import card

st.title("📊 Executive Dashboard")

df = aplicar_filtros(carregar_dados())

receita, vendas, ticket = calcular_kpis(df)

c1, c2, c3 = st.columns(3)

with c1: card("Receita Total", f"R$ {receita:,.2f}")
with c2: card("Vendas Qtd.", vendas)
with c3: card("Ticket Médio", f"R$ {ticket:,.2f}")

fig = px.line(df.groupby('sale_date')['total'].sum().reset_index(),
              x='sale_date', y='total')

st.plotly_chart(fig, use_container_width=True)