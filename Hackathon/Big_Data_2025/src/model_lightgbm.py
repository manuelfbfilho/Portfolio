# src/model_lightgbm.py
"""
Treina um LightGBM simples usando as séries agregadas por semana.
- Entrada: weekly dataframe (pdv, produto, week_start, quantidade)
- Saída: modelo treinado (retornado) e avaliação MAE
"""
import pandas as pd
from pathlib import Path
import lightgbm as lgb
from lightgbm import early_stopping
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from src.utils import standardize_transacoes

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
DOCS = BASE / "docs"

def create_lag_features(df, lags=[1,2,3,4]):
    """Cria variáveis de lag da quantidade semanal."""
    df = df.sort_values(['pdv','produto','week_start']).copy()
    for lag in lags:
        df[f"lag_{lag}"] = df.groupby(["pdv","produto"])["quantidade"].shift(lag)
    return df

def prepare_training(weekly):
    """Cria features de lag e prepara X e y."""
    df = create_lag_features(weekly)
    df = df.dropna().reset_index(drop=True)
    # features
    X = df[['pdv','produto'] + [c for c in df.columns if c.startswith('lag_')]].copy()
    X['pdv'] = X['pdv'].astype('category')
    X['produto'] = X['produto'].astype('category')
    y = df['quantidade']
    return X, y

def train_lightgbm(weekly):
    """Treina modelo LightGBM e retorna (modelo, MAE de validação)."""
    X, y = prepare_training(weekly)
    X_train, X_val, y_train, y_val = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = lgb.LGBMRegressor(n_estimators=1000, learning_rate=0.05)

    # Treina usando callback para early stopping (compatível com LightGBM 4.x)
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        callbacks=[early_stopping(stopping_rounds=50, verbose=False)]
    )

    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    print("MAE:", mae)
    return model, mae

if __name__ == "__main__":
    # Lê transações, normaliza colunas, agrega semanalmente e treina LightGBM
    trans_path = DATA / "transacoes_2022.parquet"
    if not trans_path.exists():
        raise FileNotFoundError("Arquivo de transações não encontrado em data/")
    
    df = pd.read_parquet(trans_path)
    df = standardize_transacoes(df)
    df['data'] = pd.to_datetime(df['data'])
    df['week_start'] = df['data'].dt.to_period('W').apply(lambda r: r.start_time)
    weekly = df.groupby(['pdv','produto','week_start'], as_index=False)['quantidade'].sum()
    
    model, mae = train_lightgbm(weekly)
    print("Treinamento concluído. MAE:", mae)
