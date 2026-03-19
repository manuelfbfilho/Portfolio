import streamlit as st
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.filters import aplicar_filtros
from utils.profitability import calcular_margem

st.title("💸 Rentabilidade")

df = calcular_margem(aplicar_filtros(carregar_dados()))

# Agrupar
df_agg = df.groupby('name').agg(
    lucro=('lucro', 'sum'),
    qtd=('qtd', 'sum')
).sort_values(by='lucro', ascending=True).reset_index()

# Gráfico horizontal
fig = px.bar(
    df_agg,
    x='lucro',
    y='name',
    orientation='h',
    text='qtd',
    title="Lucro por Produto (Qtd Vendida)"
)

fig.update_traces(textposition='outside')

st.plotly_chart(fig, use_container_width=True)