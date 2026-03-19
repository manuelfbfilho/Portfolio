import pandas as pd
import unicodedata

# =========================
# 1. Carregamento dos dados
# =========================
df = pd.read_csv('../../data/raw/produtos_raw.csv')

print("Colunas disponíveis:", df.columns.tolist())


# =========================
# 2. Funções auxiliares
# =========================

# 🔹 Normalização de texto (robusta)
def normalize_text(text):
    if pd.isna(text):
        return text
    
    text = text.lower().strip()
    
    # remover acentos
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    # remover espaços entre letras
    text = text.replace(" ", "")
    
    return text


# 🔹 Mapeamento de categorias
def map_category(text):
    if pd.isna(text):
        return text
    
    if "eletron" in text:
        return "eletrônicos"
    
    elif "prop" in text:
        return "propulsão"
    
    elif "ancor" in text or "encor" in text:
        return "ancoragem"
    
    else:
        return "ancoragem"  # fallback seguro


# 🔹 Limpeza de valores numéricos
def clean_numeric_column(series):
    return (
        series.astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )


# =========================
# 3. Padronização de categorias
# =========================
if 'actual_category' not in df.columns:
    raise ValueError("Coluna 'actual_category' não encontrada.")

df['actual_category'] = (
    df['actual_category']
    .apply(normalize_text)
    .apply(map_category)
)

print("\nCategorias após padronização:")
print(df['actual_category'].value_counts())


# =========================
# 4. Conversão de tipos numéricos
# =========================

# 🔹 price → float
if 'price' in df.columns:
    df['price'] = clean_numeric_column(df['price'])
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

# 🔹 code → inteiro
if 'code' in df.columns:
    df['code'] = pd.to_numeric(df['code'], errors='coerce', downcast='integer')


# =========================
# 5. Remoção de duplicatas
# =========================
before = len(df)

df = df.drop_duplicates()

after = len(df)

print(f"\nTotal antes: {before}")
print(f"Total depois: {after}")
print(f"Duplicatas removidas: {before - after}")


# =========================
# 6. Validação final
# =========================
print("\nTipos de dados:")
print(df.dtypes)

print("\nAmostra de preços:")
print(df['price'].head())


# =========================
# 7. Salvando dataset tratado
# =========================
df.to_csv('../../data/processed/produtos_clean.csv', index=False)

print("\nArquivo salvo com sucesso em data/processed/produtos_clean.csv")