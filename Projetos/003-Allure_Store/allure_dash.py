import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import datetime
import folium # Importe o folium aqui
from folium.plugins import HeatMap

# Carregando os dados
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

# Inicializando o aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Allure Store - Análise de Desempenho"

# Layout do Dashboard
app.layout = html.Div(children=[
    html.H1(children='📊 Allure Store - Análise de Desempenho', style={'textAlign': 'center', 'color': '#1e88e5'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2("🔍 Filtros", className="card-title"),
                    html.Div([
                        html.Label("Período de Análise", style={'font-weight': 'bold'}),
                        html.Div([
                            html.Label("Ano Inicial"),
                            dcc.Dropdown(
                                id='ano-inicio',
                                options=[{'label': str(ano), 'value': ano} for ano in range(dados_completos['Data da Compra'].min().year, dados_completos['Data da Compra'].max().year + 1)],
                                value=dados_completos['Data da Compra'].min().year
                            ),
                            html.Label("Ano Final"),
                            dcc.Dropdown(
                                id='ano-fim',
                                options=[{'label': str(ano), 'value': ano} for ano in range(dados_completos['Data da Compra'].min().year, dados_completos['Data da Compra'].max().year + 1)],
                                value=dados_completos['Data da Compra'].max().year
                            ),
                        ]),
                    ]),
                    html.Div([
                        html.Label("Lojas", style={'font-weight': 'bold'}),
                        dcc.Checklist(
                            id='lojas-checklist',
                            options=[{'label': loja, 'value': loja} for loja in dados_completos['Loja'].unique()],
                            value=dados_completos['Loja'].unique()
                        ),
                    ]),
                ]),
            ], className="mb-4"),
        ], width=3),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("Faturamento Total", className="card-title", style={'color': '#1e88e5'}),
                            html.Div(id='faturamento-total', style={'color': '#424242', 'font-size': '1.5rem'}),
                        ]),
                    ], className="mb-4"),
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("Média de Avaliações", className="card-title", style={'color': '#1e88e5'}),
                            html.Div(id='media-avaliacoes', style={'color': '#424242', 'font-size': '1.5rem'}),
                        ]),
                    ], className="mb-4"),
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("Frete Médio", className="card-title", style={'color': '#1e88e5'}),
                            html.Div(id='frete-medio', style={'color': '#424242', 'font-size': '1.5rem'}),
                        ]),
                    ], className="mb-4"),
                ], width=3),
                 dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("Margem Média", className="card-title", style={'color': '#1e88e5'}),
                            html.Div(id='margem-media', style={'color': '#424242', 'font-size': '1.5rem'}),
                        ]),
                    ], className="mb-4"),
                ], width=3),
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H2("📊 Análise de Desempenho", className="card-title"),
                            html.H3("💰 Faturamento por Loja",  style={'color': '#424242', 'font-size': '1.2rem'}),
                            dcc.Graph(id='faturamento-por-loja'),
                        ]),
                    ], className="mb-4"),
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("⭐ Média de Avaliações",  style={'color': '#424242', 'font-size': '1.2rem'}),
                            dcc.Graph(id='media-avaliacoes-loja'),
                        ]),
                    ], className="mb-4"),
                ], width=6),
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("📦 Vendas por Categoria",  style={'color': '#424242', 'font-size': '1.2rem'}),
                            dcc.Graph(id='vendas-por-categoria'),
                        ]),
                    ], className="mb-4"),
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("💳 Métodos de Pagamento",  style={'color': '#424242', 'font-size': '1.2rem'}),
                            dcc.Graph(id='metodos-pagamento'),
                        ]),
                    ], className="mb-4"),
                ], width=6),
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("📈 Storytelling de Vendas",  style={'color': '#424242', 'font-size': '1.2rem'}),
                            dcc.Graph(id='storytelling-vendas'),
                        ]),
                    ], className="mb-4"),
                ], width=12),
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("🌍 Análise Geográfica",  style={'color': '#424242', 'font-size': '1.2rem'}),
                            html.H4("Mapa de Calor das Vendas",  style={'color': '#424242', 'font-size': '1rem'}),
                            html.Div(id='mapa-calor-vendas'),
                        ]),
                    ], className="mb-4"),
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Distribuição Geográfica por Loja",  style={'color': '#424242', 'font-size': '1rem'}),
                            dcc.Graph(id='distribuicao-geografica'),
                        ]),
                    ], className="mb-4"),
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("📈 Score de Desempenho por Loja",  style={'color': '#424242', 'font-size': '1.2rem'}),
                            dcc.Graph(id='score-desempenho'),
                        ]),
                    ], className="mb-4"),
                ], width=12),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3("🎯 Recomendação",  style={'color': '#424242', 'font-size': '1.2rem'}),
                            html.Div(id='recomendacao')
                        ])
                    ])
                ])
            ])
        ], width=9),
    ]),
])

# Funções de callback para atualizar os gráficos e métricas
@app.callback(
    [
        Output('faturamento-total', 'children'),
        Output('media-avaliacoes', 'children'),
        Output('frete-medio', 'children'),
        Output('margem-media', 'children'),
        Output('faturamento-por-loja', 'figure'),
        Output('media-avaliacoes-loja', 'figure'),
        Output('vendas-por-categoria', 'figure'),
        Output('metodos-pagamento', 'figure'),
        Output('storytelling-vendas', 'figure'),
        Output('mapa-calor-vendas', 'children'),
        Output('distribuicao-geografica', 'figure'),
        Output('score-desempenho', 'figure'),
        Output('recomendacao', 'children')
    ],
    [
        Input('ano-inicio', 'value'),
        Input('ano-fim', 'value'),
        Input('lojas-checklist', 'value')
    ]
)
def update_dashboard(ano_inicio, ano_fim, lojas_selecionadas):
    dados_filtrados = dados_completos[
        (dados_completos['Loja'].isin(lojas_selecionadas)) &
        (dados_completos['Data da Compra'].dt.year >= ano_inicio) &
        (dados_completos['Data da Compra'].dt.year <= ano_fim)
    ]

    faturamento_total = f"R$ {dados_filtrados['Preço'].sum():,.2f}"
    media_avaliacoes = f"{dados_filtrados['Avaliação da compra'].mean():.2f}"
    frete_medio = f"R$ {dados_filtrados['Frete'].mean():.2f}"
    margem_media = f"R$ {dados_filtrados['Margem'].mean():.2f}"
    
    # Gráfico de faturamento por loja
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

    # Gráfico de média de avaliações por loja
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

    # Gráfico de vendas por categoria
    fig_categoria = px.bar(
        dados_filtrados.groupby(['Loja', 'Categoria do Produto']).size().reset_index(name='Quantidade'),
        x='Loja',
        y='Quantidade',
        color='Categoria do Produto',
        title='Quantidade de Vendas por Categoria',
        barmode='stack'
    )
    fig_categoria.update_layout(height=400)

    # Gráfico de métodos de pagamento
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

    # Gráfico de storytelling de vendas
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
    
    # Mapa de calor
    mapa = folium.Map(location=[-15.77972, -47.92972], zoom_start=4)
    heat_data = [[row['lat'], row['lon'], row['Preço']] for index, row in dados_filtrados.iterrows()]
    HeatMap(heat_data).add_to(mapa)
    mapa_html = folium.Figure().add_child(mapa)
    mapa_div = html.Iframe(srcDoc=mapa_html.render(), width='100%', height='400')

    # Gráfico de distribuição geográfica
    fig_geo = px.scatter_geo(
        dados_filtrados,
        lat='lat',
        lon='lon',
        color='Loja',
        size='Preço',
        title='Distribuição Geográfica das Vendas'
    )

    # Gráfico de score de desempenho
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
    
    # Recomendação de Loja para Fechar
    loja_para_fechar = scores_series.idxmin()
    recomendacao_texto = html.Div(children=[
        html.H3("Recomendação de Fechamento", style={'color': '#dc3545'}),
        html.P(f"Baseado na análise de múltiplos indicadores, a loja {loja_para_fechar} apresenta o pior desempenho e deve ser considerada para fechamento.", style={'color': '#000000'}),
        html.H4("Fatores Considerados:", style={'color': '#000000'}),
        html.Ul([
            html.Li("Faturamento Total (40%)", style={'color': '#000000'}),
            html.Li("Média de Avaliações (30%)", style={'color': '#000000'}),
            html.Li("Margem de Lucro (30%)", style={'color': '#000000'}),
        ])
    ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px'})

    return (
        faturamento_total,
        media_avaliacoes,
        frete_medio,
        margem_media,
        fig_faturamento,
        fig_avaliacoes,
        fig_categoria,
        fig_pagamento,
        fig_storytelling,
        mapa_div,
        fig_geo,
        fig_score,
        recomendacao_texto
    )

if __name__ == '__main__':
    app.run(debug=True)
