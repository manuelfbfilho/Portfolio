"""
Dash App – Telecom X (Versão Final)
-----------------------------------
Funcionalidades:
1) Distribuição de probabilidades + limiar ajustável;
2) Métricas no limiar escolhido (Precision, Recall, F1, AUC);
3) Curva ROC e Curva Precision–Recall (PR);
4) Curva de calibração (Reliability);
5) Tabela de métricas por faixa de limiar (0.1 → 0.9) com exportação CSV;
6) Recomendações automáticas segmentadas (storytelling prático com regras específicas).
"""

import argparse, pickle
import pandas as pd
import numpy as np

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    roc_curve, precision_recall_curve
)
from sklearn.calibration import calibration_curve

# ----------------------
# Funções auxiliares
# ----------------------
def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def compute_threshold_metrics(y_true, prob, thr):
    y_pred = (prob >= thr).astype(int)
    return {
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "auc": roc_auc_score(y_true, prob)
    }

def compute_threshold_table(y_true, prob):
    """Gera tabela de métricas de 0.1 a 0.9"""
    rows = []
    for thr in np.arange(0.1, 1.0, 0.1):
        m = compute_threshold_metrics(y_true, prob, thr)
        rows.append({
            "Limiar": round(thr,2),
            "Precision": round(m["precision"],3),
            "Recall": round(m["recall"],3),
            "F1": round(m["f1"],3),
            "AUC": round(m["auc"],3)
        })
    return pd.DataFrame(rows)

def reliability_curve_data(y_true, prob):
    frac_true, frac_pred = calibration_curve(y_true, prob, n_bins=10, strategy="uniform")
    return frac_pred, frac_true

def segment_recommendations(df, cat_col, thr, top_k=5):
    if not cat_col or cat_col not in df.columns:
        return ["Selecione uma variável categórica."]

    df = df.copy()
    df["pred_bin"] = (df["prob"] >= thr).astype(int)
    global_rate = df["pred_bin"].mean()

    agg = (df.groupby(cat_col)["pred_bin"]
             .agg(rate="mean", n="count")
             .reset_index()
             .sort_values("rate", ascending=False))

    recs = []
    for _, row in agg.head(top_k).iterrows():
        categoria = row[cat_col]
        rate = row["rate"]; n = int(row["n"])
        gap_pp = (rate - global_rate) * 100

        # Regras específicas
        if cat_col == "Contract" and categoria == "Month-to-month":
            acao = "Oferecer planos anuais/trimestrais com desconto para aumentar retenção."
        elif cat_col == "PaymentMethod" and categoria == "Electronic check":
            acao = "Incentivar migração para débito automático ou cartão (maior fidelização)."
        elif cat_col == "InternetService" and categoria == "Fiber optic":
            acao = "Reforçar suporte técnico e atendimento prioritário (clientes exigentes)."
        else:
            acao = "Aplicar comunicação proativa de retenção e revisão de benefícios."

        recs.append(
            f"Segmento '{cat_col} = {categoria}' (n={n}): risco {rate:.1%} "
            f"({gap_pp:+.1f} pp vs global). Ações: {acao}"
        )
    return recs

# ----------------------
# App principal
# ----------------------
def main(data_path, model_path):
    df = pd.read_csv(data_path).dropna(subset=["Churn"]).copy()
    df["target"] = (df["Churn"] == "Evasão").astype(int)

    X = df.drop(columns=[c for c in ["Churn","target","customerID"] if c in df.columns])
    model = load_model(model_path)
    prob = model.predict_proba(X)[:,1]
    df["prob"] = prob

    categorical_options = [{"label":c,"value":c} for c in X.columns if X[c].dtype=="object"]

    app = dash.Dash(__name__, external_stylesheets=["/assets/telecomx.css"])
    app.title = "Telecom X – Dashboard"

    app.layout = html.Div([
        html.H1("📊 Telecom X – Previsão de Churn"),

        html.Div(className="controls", children=[
            html.Div(className="control", children=[
                html.Label("Limiar de classificação"),
                dcc.Slider(0,1,0.05,value=0.5,id="threshold")
            ]),
            html.Div(className="control", children=[
                html.Label("Variável categórica"),
                dcc.Dropdown(options=categorical_options, id="cat_col", placeholder="Selecione...")
            ])
        ]),

        html.Div(id="metric-cards", className="metric-cards"),

        dcc.Tabs(value="tab-model", children=[
            dcc.Tab(label="Modelagem", value="tab-model", children=[
                dcc.Graph(id="hist"),
                dcc.Graph(id="rate"),
                dcc.Graph(id="roc-curve")
            ]),
            dcc.Tab(label="Calibração", value="tab-calib", children=[
                dcc.Graph(id="calibration-curve"),
                dcc.Graph(id="pr-curve")
            ]),
            dcc.Tab(label="Métricas por Limiar", value="tab-thr", children=[
                html.Button("⬇️ Baixar CSV", id="btn-download"),
                dcc.Download(id="download-metrics"),
                dash_table.DataTable(id="thr-table", page_size=10,
                    style_table={"overflowX":"auto"})
            ]),
            dcc.Tab(label="Recomendações", value="tab-recs", children=[
                html.Div(id="recommendations", className="recommendations")
            ])
        ])
    ])

    # ---- Callbacks ----
    @app.callback(
        [Output("metric-cards","children"),
         Output("hist","figure"),
         Output("rate","figure"),
         Output("roc-curve","figure"),
         Output("calibration-curve","figure"),
         Output("pr-curve","figure"),
         Output("thr-table","data"),
         Output("thr-table","columns"),
         Output("recommendations","children")],
        [Input("threshold","value"),
         Input("cat_col","value")]
    )
    def update_all(threshold, cat_col):
        y_true, prob_vals = df["target"].values, df["prob"].values
        m = compute_threshold_metrics(y_true, prob_vals, threshold)

        cards = [
            html.Div(className="metric-card", children=[html.Div("Precision"), html.H3(f"{m['precision']:.3f}")]),
            html.Div(className="metric-card", children=[html.Div("Recall"), html.H3(f"{m['recall']:.3f}")]),
            html.Div(className="metric-card", children=[html.Div("F1"), html.H3(f"{m['f1']:.3f}")]),
            html.Div(className="metric-card", children=[html.Div("AUC"), html.H3(f"{m['auc']:.3f}")]),
            html.Div(className="metric-card", children=[html.Div("Limiar"), html.H3(f"{threshold:.2f}")]),
        ]

        # Histograma
        hist = px.histogram(df, x="prob", nbins=20,
            color=df["target"].map({0:"Ativo",1:"Evasão"}), barmode="overlay")
        hist.add_vline(x=threshold, line_dash="dash")

        # Taxa por categoria
        df_tmp = df.copy()
        df_tmp["pred"] = (df_tmp["prob"]>=threshold).astype(int)
        if cat_col:
            agg = df_tmp.groupby(cat_col)["pred"].mean().reset_index().sort_values("pred",ascending=False)
            rate = px.bar(agg,x=cat_col,y="pred",title=f"Taxa prevista por {cat_col}")
        else:
            rate = px.bar(x=["Global"],y=[df_tmp["pred"].mean()],labels={"y":"Taxa"})

        # ROC
        fpr,tpr,_ = roc_curve(y_true, prob_vals)
        roc_fig = go.Figure()
        roc_fig.add_trace(go.Scatter(x=fpr,y=tpr,mode="lines",name=f"ROC AUC={m['auc']:.3f}"))
        roc_fig.add_trace(go.Scatter(x=[0,1],y=[0,1],mode="lines",line=dict(dash="dash"),name="Aleatório"))
        roc_fig.update_layout(title="Curva ROC",xaxis_title="FPR",yaxis_title="TPR")

        # Calibração
        frac_pred, frac_true = reliability_curve_data(y_true, prob_vals)
        calib_fig = go.Figure()
        calib_fig.add_trace(go.Scatter(x=frac_pred,y=frac_true,mode="lines+markers",name="Modelo"))
        calib_fig.add_trace(go.Scatter(x=[0,1],y=[0,1],mode="lines",name="Ideal",line=dict(dash="dash")))
        calib_fig.update_layout(title="Curva de Calibração")

        # Precision–Recall
        prec, rec, _ = precision_recall_curve(y_true, prob_vals)
        pr_fig = go.Figure()
        pr_fig.add_trace(go.Scatter(x=rec,y=prec,mode="lines",name="PR Curve"))
        pr_fig.update_layout(title="Curva Precision–Recall",xaxis_title="Recall",yaxis_title="Precision")

        # Tabela de métricas por limiar
        table = compute_threshold_table(y_true, prob_vals)
        data = table.to_dict("records")
        columns = [{"name":i,"id":i} for i in table.columns]

        # Recomendações
        recs = segment_recommendations(df, cat_col, threshold)
        rec_div = html.Div([html.H3("Sugestões de ação"), html.Ul([html.Li(r) for r in recs])])

        return cards, hist, rate, roc_fig, calib_fig, pr_fig, data, columns, rec_div

    # Download CSV
    @app.callback(
        Output("download-metrics","data"),
        Input("btn-download","n_clicks"),
        prevent_initial_call=True
    )
    def download_thr_table(n_clicks):
        table = compute_threshold_table(df["target"].values, df["prob"].values)
        return dcc.send_data_frame(table.to_csv,"metrics_thresholds.csv",index=False)

    try:
        app.run(debug=True)
    except TypeError:
        app.run_server(debug=True)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",required=True)
    parser.add_argument("--model",required=True)
    args = parser.parse_args()
    main(args.data,args.model)
