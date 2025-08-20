
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict

def _cramers_v(confusion_matrix: pd.DataFrame) -> float:
    chi2 = ((confusion_matrix - confusion_matrix.mean())**2 / confusion_matrix.mean()).sum().sum()
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n if n>0 else 0.0
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1)) if n>1 else 0.0
    rcorr = r - ((r-1)**2)/(n-1) if n>1 else r
    kcorr = k - ((k-1)**2)/(n-1) if n>1 else k
    denom = min((kcorr-1), (rcorr-1))
    return np.sqrt(phi2corr / denom) if denom>0 else 0.0

def cramers_v_matrix(df: pd.DataFrame, cat_cols: List[str]) -> pd.DataFrame:
    cols = list(cat_cols)
    m = pd.DataFrame(np.eye(len(cols)), index=cols, columns=cols, dtype=float)
    for i,c1 in enumerate(cols):
        for j,c2 in enumerate(cols):
            if j<=i: 
                continue
            cm = pd.crosstab(df[c1], df[c2])
            v = _cramers_v(cm)
            m.loc[c1,c2] = v
            m.loc[c2,c1] = v
    return m

def num_corr(df: pd.DataFrame, num_cols: List[str]) -> pd.DataFrame:
    return df[num_cols].corr()

def linear_probability_model(df: pd.DataFrame, target_col: str, features: List[str]):
    """Simple OLS with binary target for interpretability (Linear Probability Model)."""
    import statsmodels.api as sm
    X = df[features].copy()
    # One-hot encode categoricals (drop first to avoid multicollinearity)
    for c in features:
        if X[c].dtype == 'object':
            dummies = pd.get_dummies(X[c], prefix=c, drop_first=True)
            X = X.drop(columns=[c]).join(dummies)
    X = sm.add_constant(X, prepend=True)
    y = (df[target_col].astype(int) if df[target_col].dtype!='int64' else df[target_col])
    model = sm.OLS(y, X).fit()
    return model, X.columns.tolist()
