# src/dash_app.py
"""
Dash App para explorar previsões (lê CSV gerado em docs/)
"""
import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DOCS = BASE / "docs"

app = Dash(__name__)

PARQUET_PATH = DOCS / "predictions_hackathon_baseline.parquet"
try:
    df = pd.read_parquet(PARQUET_PATH)
    # garantir tipos
    if not df.empty:
        df['pdv'] = df['pdv'].astype(int)
        df['produto'] = df['produto'].astype(int)
        df['semana'] = df['semana'].astype(int)
except FileNotFoundError:
    df = pd.DataFrame(columns=['semana','pdv','produto','quantidade'])
    print(f"Aviso: arquivo {PARQUET_PATH} não encontrado. Rode o pipeline primeiro.")

app.layout = html.Div([
    html.H2("Forecast Hackathon - Previsões"),
    html.Div([
        html.Label("Selecione PDV:"),
        dcc.Dropdown(
            id="select-pdv",
            options=[{"label": str(x), "value": x} for x in sorted(df['pdv'].unique())],
            placeholder="Selecione PDV",
            multi=False
        )
    ]),
    html.Div([
        html.Label("Selecione Produto:"),
        dcc.Dropdown(
            id="select-prod",
            options=[{"label": str(x), "value": x} for x in sorted(df['produto'].unique())],
            placeholder="Selecione Produto",
            multi=False
        )
    ]),
    dcc.Graph(id="forecast-graph")
])

@app.callback(
    Output("forecast-graph","figure"),
    [Input("select-pdv","value"), Input("select-prod","value")]
)
def update_graph(pdv, produto):
    dff = df.copy()
    if pdv is not None:
        dff = dff[dff['pdv']==pdv]
    if produto is not None:
        dff = dff[dff['produto']==produto]
    if dff.empty:
        fig = px.bar(title="Sem dados para os filtros selecionados")
    else:
        fig = px.bar(dff.sort_values('semana'), x='semana', y='quantidade',
                     title=f"Previsão Jan/2023 - PDV={pdv or '-'}, PROD={produto or '-'}")
    return fig

if __name__ == "__main__":
    app.run(debug=True, port=8050)
