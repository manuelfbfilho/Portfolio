from sklearn.cluster import KMeans
import pandas as pd

def segmentar_clientes(df):
    base = df.groupby('id_client').agg({
        'total': 'sum',
        'qtd': 'sum'
    }).reset_index()

    kmeans = KMeans(n_clusters=3, random_state=42)
    base['cluster'] = kmeans.fit_predict(base[['total','qtd']])

    return base