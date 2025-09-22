# src/utils.py
"""
Utilitários para normalização de colunas e validações.
"""
from typing import Dict
import pandas as pd

# mapeamentos possíveis para encontrar as colunas nos arquivos reais
COL_MAP = {
    # transações -> padrão interno
    'data': ['transaction_date','data','Data'],
    'pdv': ['internal_store_id','pdv','PDV'],
    'produto': ['internal_product_id','produto','produto_id'],
    'quantidade': ['quantity','quantidade','qty','qtd'],
    'faturamento': ['gross_value','faturamento','valor_bruto']
}

def find_column(df: pd.DataFrame, possibles: list):
    for p in possibles:
        if p in df.columns:
            return p
    return None

def standardize_transacoes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tenta mapear colunas do DataFrame transações para os nomes padrão:
    data, pdv, produto, quantidade, faturamento (se houver).
    """
    col_renames: Dict[str,str] = {}
    for std_name, possibles in COL_MAP.items():
        found = find_column(df, possibles)
        if found:
            col_renames[found] = std_name
    if 'data' not in col_renames.values():
        raise ValueError(f"Não foi encontrada coluna de data nas colunas: {list(df.columns)}")
    if 'pdv' not in col_renames.values():
        raise ValueError("Não foi encontrada coluna de PDV.")
    if 'produto' not in col_renames.values():
        raise ValueError("Não foi encontrada coluna de Produto.")
    if 'quantidade' not in col_renames.values():
        raise ValueError("Não foi encontrada coluna de Quantidade.")
    df = df.rename(columns=col_renames)
    return df

def standardize_produtos(df: pd.DataFrame) -> pd.DataFrame:
    # renomeia apenas se necessário
    if 'produto' not in df.columns:
        for c in ['produto_id','internal_product_id']:
            if c in df.columns:
                df = df.rename(columns={c:'produto'})
    return df

def standardize_pdvs(df: pd.DataFrame) -> pd.DataFrame:
    if 'pdv' not in df.columns:
        for c in ['internal_store_id','store_id']:
            if c in df.columns:
                df = df.rename(columns={c:'pdv'})
    return df
