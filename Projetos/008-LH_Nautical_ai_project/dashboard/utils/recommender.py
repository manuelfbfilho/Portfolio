import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def gerar_recomendacao(df):
    df['comprou'] = 1

    matriz = df.groupby(['id_client','product_id'])['comprou'].max().unstack(fill_value=0)

    sim = cosine_similarity(matriz.T)

    return pd.DataFrame(sim, index=matriz.columns, columns=matriz.columns)