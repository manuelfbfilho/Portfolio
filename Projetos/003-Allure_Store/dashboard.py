import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Configuração da página
st.set_page_config(
    page_title="Allure Store - Análise de Desempenho",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric h3 {
        color: #1e88e5;
    }
    .stMetric div {
        color: #424242;
    }
    .css-1d391kg {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stCheckbox > label {
        font-size: 16px;
        font-weight: 500;
    }
    .stSelectbox > label {
        font-size: 16px;
        font-weight: 500;
    }
    .stDateInput > label {
        font-size: 16px;
        font-weight: 500;
    }
    .stMarkdown h1 {
        color: #1e88e5;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .stMarkdown h2 {
        color: #424242;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    .stMarkdown h3 {
        color: #424242;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .stMarkdown h4 {
        color: #424242;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    .stMarkdown p {
        color: #424242;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .stMarkdown li {
        color: #424242;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Carregando os dados
@st.cache_data
def carregar_dados():
    url1 = "BD/loja_1.csv"
    url2 = "BD/loja_2.csv"
    url3 = "BD/loja_3.csv"
    url4 = "BD/loja_4.csv"
    
    loja1 = pd.read_csv(url1)
    loja2 = pd.read_csv(url2)
    loja3 = pd.read_csv(url3)
    loja4 = pd.read_csv(url4)
    
    loja1['Loja'] = 'Loja 1'
    loja2['Loja'] = 'Loja 2'
    loja3['Loja'] = 'Loja 3'
    loja4['Loja'] = 'Loja 4'
    
    dados_completos = pd.concat([loja1, loja2, loja3, loja4], ignore_index=True)
    dados_completos['Data da Compra'] = pd.to_datetime(dados_completos['Data da Compra'], format='%d/%m/%Y')
    dados_completos['Mês'] = dados_completos['Data da Compra'].dt.to_period('M')
    dados_completos['Margem'] = dados_completos['Preço'] - dados_completos['Frete']
    
    return dados_completos

dados_completos = carregar_dados()

# Título do dashboard
st.markdown("# 📊 Allure Store - Análise de Desempenho")

# Sidebar para filtros
st.sidebar.markdown("## 🔍 Filtros")

# Informações do período
min_date = dados_completos['Data da Compra'].min()
max_date = dados_completos['Data da Compra'].max()
st.sidebar.markdown(f"**Período disponível:**")
st.sidebar.markdown(f"De: {min_date.strftime('%d/%m/%Y')}")
st.sidebar.markdown(f"Até: {max_date.strftime('%d/%m/%Y')}")

# Filtro de período
st.sidebar.markdown("### Período de Análise")
ano_inicio = st.sidebar.selectbox(
    "Ano Inicial",
    options=range(min_date.year, max_date.year + 1),
    index=0
)
ano_fim = st.sidebar.selectbox(
    "Ano Final",
    options=range(min_date.year, max_date.year + 1),
    index=len(range(min_date.year, max_date.year + 1)) - 1
)

# Filtro de lojas
st.sidebar.markdown("### Lojas")
lojas = dados_completos['Loja'].unique()
loja_selecionada = []
for loja in lojas:
    if st.sidebar.checkbox(loja, value=True):
        loja_selecionada.append(loja)

# Aplicando filtros
dados_filtrados = dados_completos[
    (dados_completos['Loja'].isin(loja_selecionada)) &
    (dados_completos['Data da Compra'].dt.year >= ano_inicio) &
    (dados_completos['Data da Compra'].dt.year <= ano_fim)
]

# Métricas principais
st.markdown("## 📈 Métricas Principais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Faturamento Total",
        f"R$ {dados_filtrados['Preço'].sum():,.2f}",
        help="Soma total dos preços de todos os produtos vendidos"
    )
with col2:
    st.metric(
        "Média de Avaliações",
        f"{dados_filtrados['Avaliação da compra'].mean():.2f}",
        help="Média das avaliações dos clientes (1-5)"
    )
with col3:
    st.metric(
        "Frete Médio",
        f"R$ {dados_filtrados['Frete'].mean():.2f}",
        help="Custo médio de frete por venda"
    )
with col4:
    st.metric(
        "Margem Média",
        f"R$ {dados_filtrados['Margem'].mean():.2f}",
        help="Diferença média entre preço e frete"
    )

# Gráficos em duas colunas
st.markdown("## 📊 Análise de Desempenho")

# Primeira linha de gráficos
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💰 Faturamento por Loja")
    fig_faturamento = px.bar(
        dados_filtrados.groupby('Loja')['Preço'].sum().reset_index(),
        x='Loja',
        y='Preço',
        title='Faturamento Total por Loja',
        color='Loja',
        text_auto='.2s'
    )
    fig_faturamento.update_layout(
        xaxis_title="Loja",
        yaxis_title="Faturamento (R$)",
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_faturamento, use_container_width=True)

with col2:
    st.markdown("### ⭐ Média de Avaliações")
    fig_avaliacoes = px.bar(
        dados_filtrados.groupby('Loja')['Avaliação da compra'].mean().reset_index(),
        x='Loja',
        y='Avaliação da compra',
        title='Média de Avaliações por Loja',
        color='Loja',
        text_auto='.2f'
    )
    fig_avaliacoes.update_layout(
        yaxis_range=[0, 5],
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_avaliacoes, use_container_width=True)

# Segunda linha de gráficos
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📦 Vendas por Categoria")
    fig_categoria = px.bar(
        dados_filtrados.groupby(['Loja', 'Categoria do Produto']).size().reset_index(name='Quantidade'),
        x='Loja',
        y='Quantidade',
        color='Categoria do Produto',
        title='Quantidade de Vendas por Categoria',
        barmode='stack'
    )
    fig_categoria.update_layout(height=400)
    st.plotly_chart(fig_categoria, use_container_width=True)

with col2:
    st.markdown("### 💳 Métodos de Pagamento")
    pagamento = dados_filtrados.groupby('Tipo de pagamento').agg({
        'Preço': 'sum',
        'Quantidade de parcelas': 'mean'
    }).reset_index()
    pagamento['% Faturamento'] = pagamento['Preço'] / pagamento['Preço'].sum() * 100

    fig_pagamento = px.pie(
        pagamento,
        values='Preço',
        names='Tipo de pagamento',
        title='Distribuição do Faturamento por Método de Pagamento',
        hole=0.4
    )
    fig_pagamento.update_layout(height=400)
    st.plotly_chart(fig_pagamento, use_container_width=True)

# Terceira linha de gráficos - Storytelling de Vendas
st.markdown("### 📈 Storytelling de Vendas")
# Convertendo o período para string para evitar problemas de formatação
dados_storytelling = dados_filtrados.copy()
dados_storytelling['Mês_Formatado'] = dados_storytelling['Mês'].astype(str)
fig_storytelling = px.line(
    dados_storytelling.groupby(['Mês_Formatado', 'Loja'])['Preço'].sum().reset_index(),
    x='Mês_Formatado',
    y='Preço',
    color='Loja',
    title='Evolução do Faturamento por Loja',
    markers=True
)
fig_storytelling.update_layout(
    xaxis_title="Mês",
    yaxis_title="Faturamento (R$)",
    height=400,
    xaxis=dict(
        tickangle=45,
        tickmode='auto',
        nticks=len(dados_storytelling['Mês_Formatado'].unique())
    )
)
st.plotly_chart(fig_storytelling, use_container_width=True)

# Quarta linha de gráficos
st.markdown("### 🌍 Análise Geográfica")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Mapa de Calor das Vendas")
    mapa = folium.Map(location=[-15.77972, -47.92972], zoom_start=4)
    heat_data = [[row['lat'], row['lon'], row['Preço']] for index, row in dados_filtrados.iterrows()]
    HeatMap(heat_data).add_to(mapa)
    folium_static(mapa)

with col2:
    st.markdown("#### Distribuição Geográfica por Loja")
    fig_geo = px.scatter_geo(
        dados_filtrados,
        lat='lat',
        lon='lon',
        color='Loja',
        size='Preço',
        title='Distribuição Geográfica das Vendas'
    )
    st.plotly_chart(fig_geo, use_container_width=True)

# Score de Desempenho
st.markdown("### 📈 Score de Desempenho por Loja")
def calcular_score(loja):
    dados_loja = dados_filtrados[dados_filtrados['Loja'] == loja]
    faturamento = dados_loja['Preço'].sum() / dados_filtrados['Preço'].sum()
    avaliacao = dados_loja['Avaliação da compra'].mean() / 5
    margem = dados_loja['Margem'].mean() / dados_filtrados['Margem'].mean()
    score = (faturamento * 0.4) + (avaliacao * 0.3) + (margem * 0.3)
    return score

scores = {loja: calcular_score(loja) for loja in dados_filtrados['Loja'].unique()}
scores_series = pd.Series(scores).sort_values(ascending=False)

fig_score = px.bar(
    scores_series.reset_index(),
    x='index',
    y=0,
    color='index',
    title='Score de Desempenho por Loja',
    text_auto='.2f'
)
fig_score.update_layout(
    xaxis_title="Loja",
    yaxis_title="Score",
    showlegend=False,
    height=400
)
st.plotly_chart(fig_score, use_container_width=True)

# Recomendação
st.markdown("### 🎯 Recomendação")
loja_para_fechar = scores_series.idxmin()
st.markdown(f"""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
    <h3 style='color: #dc3545;'>Recomendação de Fechamento</h3>
    <p style='color: #000000;'>Baseado na análise de múltiplos indicadores, a <strong>{loja_para_fechar}</strong> apresenta o pior desempenho e deve ser considerada para fechamento.</p>
    <h4 style='color: #000000;'>Fatores Considerados:</h4>
    <ul>
        <li style='color: #000000;'>Faturamento Total (40%)</li>
        <li style='color: #000000;'>Média de Avaliações (30%)</li>
        <li style='color: #000000;'>Margem de Lucro (30%)</li>
    </ul>
</div>
""", unsafe_allow_html=True) 