def calcular_margem(df):
    df['custo'] = df.get('cost_usd', 0) * 5
    df['lucro'] = df['total'] - df['custo']
    return df