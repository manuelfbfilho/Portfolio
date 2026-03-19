import pandas as pd
import json
from pathlib import Path

# =========================
# 1. Configuração
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_FILE = BASE_DIR / "data/raw/custos_importacao.json"
OUTPUT_FILE = BASE_DIR / "data/processed/custos_importacao_normalizado.csv"


# =========================
# 2. Logger simples
# =========================
def log(msg):
    print(f"[INFO] {msg}")


# =========================
# 3. Extração
# =========================
def extract_json(file_path):
    log("Carregando JSON...")
    
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    log(f"Registros carregados: {len(data)} produtos")
    return data


# =========================
# 4. Transformação
# =========================
def transform_data(data):
    log("Transformando dados...")
    
    rows = []
    
    for item in data:
        product_id = item.get("product_id")
        product_name = item.get("product_name")
        category = item.get("category")
        historic = item.get("historic_data", [])
        
        if not historic:
            continue
        
        for record in historic:
            rows.append({
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "start_date": record.get("start_date"),
                "usd_price": record.get("usd_price")
            })
    
    df = pd.DataFrame(rows)
    
    log(f"Total de linhas geradas: {len(df)}")
    
    # =========================
    # 5. Limpeza e padronização
    # =========================
    
    # Datas
    df['start_date'] = pd.to_datetime(df['start_date'], dayfirst=True, errors='coerce')
    
    # Preço
    df['usd_price'] = pd.to_numeric(df['usd_price'], errors='coerce')
    
    # Ordenação temporal (importante)
    df = df.sort_values(by=['product_id', 'start_date'])
    
    # =========================
    # 6. Validação
    # =========================
    
    null_dates = df['start_date'].isnull().sum()
    null_prices = df['usd_price'].isnull().sum()
    
    log(f"Datas nulas: {null_dates}")
    log(f"Preços nulos: {null_prices}")
    
    return df


# =========================
# 7. Load
# =========================
def load_data(df, output_path):
    log("Salvando CSV...")
    
    df.to_csv(output_path, index=False)
    
    log(f"Arquivo salvo em: {output_path}")


# =========================
# 8. Pipeline
# =========================
def run():
    data = extract_json(INPUT_FILE)
    df = transform_data(data)
    load_data(df, OUTPUT_FILE)
    
    log("Processo finalizado com sucesso!")


# =========================
# Execução
# =========================
if __name__ == "__main__":
    run()