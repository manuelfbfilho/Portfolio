import pandas as pd
import streamlit as st

@st.cache_data
def carregar_dados():
    # =========================
    # 1. Carregar dados
    # =========================
    vendas = pd.read_csv("data/raw/vendas_2023_2024.csv")
    produtos = pd.read_csv("data/processed/produtos_clean.csv")

    # =========================
    # 2. Padronizar colunas
    # =========================
    vendas = vendas.rename(columns={'id_product': 'product_id'})
    produtos = produtos.rename(columns={'code': 'product_id'})

    vendas['product_id'] = vendas['product_id'].astype(str).str.strip()
    produtos['product_id'] = produtos['product_id'].astype(str).str.strip()

    # =========================
    # 3. Merge vendas + produtos
    # =========================
    df = vendas.merge(produtos, on='product_id', how='left')

    # =========================
    # 4. Datas
    # =========================
    df['sale_date'] = pd.to_datetime(
        df['sale_date'],
        format='mixed',
        dayfirst=True,
        errors='coerce'
    )

    df = df.dropna(subset=['sale_date'])

    # =========================
    # 5. Clientes (CORRETO AGORA)
    # =========================
    try:
        clientes = pd.read_json("data/raw/clientes_crm.json")

        # Renomear corretamente
        clientes = clientes.rename(columns={
            'code': 'id_client',
            'full_name': 'nome'
        })

        # Garantir mesmo tipo
        clientes['id_client'] = clientes['id_client'].astype(str)
        df['id_client'] = df['id_client'].astype(str)

        # Merge
        df = df.merge(clientes[['id_client', 'nome']], on='id_client', how='left')

    except Exception as e:
        print("Erro ao carregar clientes:", e)

    # =========================
    # 6. Limpeza final
    # =========================
    df['name'] = df['name'].fillna("Produto desconhecido")
    df['nome'] = df['nome'].fillna("Cliente desconhecido")

    return df