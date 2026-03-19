import streamlit as st
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.filters import aplicar_filtros

st.title("👥 Clientes")

df = aplicar_filtros(carregar_dados())

clientes = df.groupby('id_client')['total'].sum().sort_values(ascending=False).head(10)

fig = px.bar(clientes)

st.plotly_chart(fig)