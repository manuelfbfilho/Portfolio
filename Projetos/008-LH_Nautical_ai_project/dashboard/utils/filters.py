import streamlit as st

def aplicar_filtros(df):
    st.sidebar.header("🔎 Filtros Globais")

    df_f = df.copy()

    # =========================
    # 1. DATA
    # =========================
    data_min = df_f['sale_date'].min()
    data_max = df_f['sale_date'].max()

    data_inicio = st.sidebar.date_input("Data início", data_min)
    data_fim = st.sidebar.date_input("Data fim", data_max)

    if data_inicio and data_fim:
        df_f = df_f[
            (df_f['sale_date'] >= str(data_inicio)) &
            (df_f['sale_date'] <= str(data_fim))
        ]

    # =========================
    # 2. PRODUTOS
    # =========================
    produtos_unicos = df_f[['product_id', 'name']].drop_duplicates()

    produtos_dict = {
        f"{row['product_id']} - {row['name']}": row['name']
        for _, row in produtos_unicos.iterrows()
    }

    produtos_label = st.sidebar.multiselect(
        "Produtos",
        options=sorted(produtos_dict.keys())
    )

    if produtos_label:
        produtos_selecionados = [produtos_dict[p] for p in produtos_label]
        df_f = df_f[df_f['name'].isin(produtos_selecionados)]

    # =========================
    # 3. CLIENTES
    # =========================
    if 'nome' in df_f.columns:
        clientes_unicos = df_f[['id_client', 'nome']].drop_duplicates()

        clientes_dict = {
            f"{row['id_client']} - {row['nome']}": row['id_client']
            for _, row in clientes_unicos.iterrows()
        }

        clientes_label = st.sidebar.multiselect(
            "Clientes",
            options=sorted(clientes_dict.keys())
        )

        if clientes_label:
            clientes_selecionados = [clientes_dict[c] for c in clientes_label]
            df_f = df_f[df_f['id_client'].isin(clientes_selecionados)]

    else:
        clientes = st.sidebar.multiselect(
            "Clientes",
            options=sorted(df_f['id_client'].unique())
        )

        if clientes:
            df_f = df_f[df_f['id_client'].isin(clientes)]

    return df_f