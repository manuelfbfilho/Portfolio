# src/main_pipeline.py
"""
Pipeline principal do Hackathon Forecast Big Data 2025
- Lê dados de /data
- Normaliza colunas
- Gera baseline e salva previsões em /docs
"""
import pandas as pd
from pathlib import Path
from src.utils import standardize_transacoes, standardize_produtos, standardize_pdvs

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
DOCS = BASE / "docs"

def load_data(trans_path, products_path=None, pdvs_path=None):
    print(f"Carregando: {trans_path}")
    df = pd.read_parquet(trans_path)
    prod = pd.read_parquet(products_path) if products_path and Path(products_path).exists() else None
    pdv = pd.read_parquet(pdvs_path) if pdvs_path and Path(pdvs_path).exists() else None

    # normaliza nomes de colunas
    df = standardize_transacoes(df)
    if prod is not None:
        prod = standardize_produtos(prod)
    if pdv is not None:
        pdv = standardize_pdvs(pdv)
    print("Colunas transacoes (após normalização):", list(df.columns))
    return df, prod, pdv

def aggregate_weekly(df, date_col='data'):
    if date_col not in df.columns:
        raise KeyError(f"Coluna de data esperada '{date_col}' não encontrada. Colunas disponíveis: {list(df.columns)}")
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    if df[date_col].isna().all():
        raise ValueError(f"A coluna {date_col} não contém datas convertíveis.")
    # criar semana (início da semana)
    df['week_start'] = df[date_col].dt.to_period('W').apply(lambda r: r.start_time)
    # nomes padrão esperados: 'pdv', 'produto', 'quantidade'
    for c in ['pdv','produto','quantidade']:
        if c not in df.columns:
            raise KeyError(f"Coluna esperada '{c}' não encontrada no DataFrame.")
    weekly = df.groupby(['pdv','produto','week_start'], as_index=False)['quantidade'].sum()
    return weekly

def baseline_predict(weekly):
    # calcula média das últimas 4 semanas e média anual
    weeks_sorted = sorted(weekly['week_start'].unique())
    if len(weeks_sorted) == 0:
        raise ValueError("Weekly DataFrame vazio.")
    last_weeks = weeks_sorted[-4:]
    recent = weekly[weekly['week_start'].isin(last_weeks)]
    mean_last4 = recent.groupby(['pdv','produto'], as_index=False)['quantidade'].mean().rename(columns={'quantidade':'mean_last4'})
    annual_mean = weekly.groupby(['pdv','produto'], as_index=False)['quantidade'].mean().rename(columns={'quantidade':'mean_annual'})
    pred_base = pd.merge(annual_mean[['pdv','produto','mean_annual']], mean_last4, on=['pdv','produto'], how='left')
    pred_base['pred'] = pred_base['mean_last4'].fillna(pred_base['mean_annual']).fillna(0).round().astype(int)

    rows = []
    for _, r in pred_base.iterrows():
        for s in range(1,6):  # semanas 1..5 de janeiro
            rows.append((s, int(r['pdv']), int(r['produto']), int(r['pred'])))
    pred_df = pd.DataFrame(rows, columns=['semana','pdv','produto','quantidade'])
    return pred_df

if __name__ == "__main__":
    trans_path = DATA / "transacoes_2022.parquet"
    prod_path  = DATA / "produtos.parquet"
    pdv_path   = DATA / "pdvs.parquet"

    df, prod, pdv = load_data(trans_path, prod_path, pdv_path)
    weekly = aggregate_weekly(df, date_col='data')
    pred_df = baseline_predict(weekly)

    # 🔹 Limite máximo de linhas permitidas
    MAX_ROWS = 1_500_000

    # 🔹 Ordena produtos por total previsto (maior -> menor)
    prod_sums = pred_df.groupby('produto')['quantidade'].sum().sort_values(ascending=False)

    # 🔹 Vai adicionando produtos até atingir o limite de linhas
    rows_acumuladas = 0
    produtos_selecionados = []
    for prod_id, _ in prod_sums.items():
        linhas_prod = len(pred_df[pred_df['produto'] == prod_id])
        if rows_acumuladas + linhas_prod > MAX_ROWS:
            break
        produtos_selecionados.append(prod_id)
        rows_acumuladas += linhas_prod

    # 🔹 Filtra DataFrame apenas com esses produtos
    pred_df_filtrado = pred_df[pred_df['produto'].isin(produtos_selecionados)]
    print(f"Selecionados {len(produtos_selecionados)} produtos ({rows_acumuladas} linhas)")

    DOCS.mkdir(exist_ok=True)
    out_path = DOCS / "predictions_hackathon_model.parquet"
    pred_df_filtrado.to_parquet(out_path, index=False)
    print(f"Arquivo gerado em {out_path} com {len(pred_df_filtrado)} linhas")

