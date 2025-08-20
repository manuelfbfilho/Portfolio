from __future__ import annotations
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

TARGET_COL = "Churn"

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna(subset=[TARGET_COL]).copy()
    df["target"] = (df[TARGET_COL] == "Evasão").astype(int)
    return df

def build_preprocess(df: pd.DataFrame, drop_cols=("Churn","target","customerID")):
    X = df.drop(columns=list(drop_cols))
    cat_cols = [c for c in X.columns if X[c].dtype == "object"]
    num_cols = [c for c in X.columns if c not in cat_cols]

    numeric = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    categoric = Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))])

    preprocess = ColumnTransformer(
        transformers=[
            ("num", numeric, num_cols),
            ("cat", categoric, cat_cols),
        ]
    )
    return preprocess, cat_cols, num_cols