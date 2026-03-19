def calcular_kpis(df):
    receita = df['total'].sum()
    vendas = len(df)
    ticket = receita / vendas if vendas > 0 else 0

    return receita, vendas, ticket