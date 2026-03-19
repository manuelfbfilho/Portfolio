import streamlit as st
import pandas as pd
from utils.data_loader import carregar_dados
from utils.recommender import gerar_recomendacao

st.title("🧠 Sistema de Recomendação")

df = carregar_dados()

sim = gerar_recomendacao(df)

# mapa produtos
mapa = df[['product_id','name']].drop_duplicates().set_index('product_id')['name']

# criar label amigável
labels = {pid: f"{pid} - {mapa.get(pid, '')}" for pid in sim.columns}

produto_label = st.selectbox(
    "Produto referência",
    options=list(labels.values())
)

# recuperar id
produto = [k for k,v in labels.items() if v == produto_label][0]

ranking = sim[produto].sort_values(ascending=False)[1:6]

# montar tabela
resultado = pd.DataFrame({
    'product_id': ranking.index,
    'similaridade': ranking.values,
    'nome_produto': ranking.index.map(mapa)
})

st.dataframe(resultado)