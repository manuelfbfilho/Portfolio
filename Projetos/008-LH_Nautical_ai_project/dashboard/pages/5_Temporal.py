import streamlit as st
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.filters import aplicar_filtros

st.title("📅 Temporal")

df = aplicar_filtros(carregar_dados())

df['dia'] = df['sale_date'].dt.day_name()

fig = px.bar(df.groupby('dia')['total'].mean().reset_index(),
             x='dia', y='total')

st.plotly_chart(fig)