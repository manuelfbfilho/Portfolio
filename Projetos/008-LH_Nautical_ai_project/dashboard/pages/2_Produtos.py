import streamlit as st
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.filters import aplicar_filtros

st.title("📦 Produtos")

df = aplicar_filtros(carregar_dados())

top = df.groupby('name')['total'].sum().sort_values(ascending=False).head(10)

fig = px.bar(top)

st.plotly_chart(fig)