import streamlit as st
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.clustering import segmentar_clientes

st.title("📊 Segmentação de Clientes")

df = carregar_dados()

cluster = segmentar_clientes(df)

fig = px.scatter(cluster, x='total', y='qtd', color='cluster')

st.plotly_chart(fig)