<table width=1000 align="center" border=0>
<tr>
  <td align=center width=150><img src="images/Fernandes.png" width="120"/></td>
  <td align=center width=700><img src="images/Banner.png" width="600"/></td>
  <td align=center width=150><img src="images/Big_Data.png" width="120"></td>
</tr>
</table>

# 📊 Hackathon Forecast Big Data 2025
Solução para o projeto de previsão de vendas para apoiar reposição de produtos (desafio Hackathon Forecast Big Data 2025). Com o objetivo de prever a quantidade semanal de vendas por PDV/SKU para as 5 semanas de janeiro/2023 a partir do histórico de 2022.

## 📂 Estrutura do Projeto

```
📁 Big_Data_2025/
│
├── data/
│   └── transcoes_2022.parquet
│   └── produtos.parquet
│   └── pdvs.parquet
│
├── docs/
│   ├── Hackathon Forecast Big Data 2025 - Desafio Tecnico.docx
│   ├── predictions_hackathon_baseline.csv
│
├── images/
│   ├── Fernandes.png
│   ├── Big_Data.png
│   ├── Banner.png
|
├── src/
│   ├── main_pipeline.py
│   ├── model_lightgbm.py
│   ├── dash_app.py
│   ├── utils.py
│
├── README.md
├── requirements.txt
└── .gitignore

Obs.: Os arquivos referentes aos BDs estarão disponibilizados nos links abaixo, no final do README.
```
--- 

## Requisitos
- Python 3.9+
- Pacotes (pandas, pyarrow, lightgbm, scikit-learn, dash, plotly)

Exemplo `requirements.txt`:

---

## ▶️ Instruções de Execução
### 1. Coloque os dados `.parquet` em `data/`:
- transacoes_2022.parquet
- produtos.parquet
- pdvs.parquet

### 2. Rode o pipeline baseline:
```python -m src.main_pipeline```

Saída esperada: docs/predictions_hackathon_baseline.parquet.

### 3. (Opcional) Treinar modelo LightGBM:
```python -m src.model_lightgbm```

### (Opcional) Rodar dashboard:
```python -m src.dash_app```

## Observações
* O script mapeia automaticamente as colunas reais para nomes padrão internos.
* Baseline: média das últimas 4 semanas, fallback média anual.
* Formato de submissão exigido: semana;pdv;produto;quantidade (inteiros) para 5 semanas de janeiro/2023.

---

## Recomendações

### 1. Criar e ativar ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/Mac
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Links Disponíveis
* BD Transações 2022 (PARQUET) - [Download Aqui!](https://drive.google.com/open?id=12hvE9Hxr3D02CCQ4cZ8g0vf2o508Jkbr&usp=drive_fs)

* BD Cadastro de Produtos (PARQUET) - [Download Aqui!](https://drive.google.com/open?id=189dIV8ZOnABmkGubOmWo5DqoWwKUDcNH&usp=drive_fs)

* BD Cadastro de PDVs (PARQUET) - [Download Aqui!](https://drive.google.com/open?id=1TchAV34xwJ-dfh9cLNjsANBo6mtBCmQ_&usp=drive_fs)

---

## ✍️ Autor

**Manuel Fernandes**  
[LinkedIn](https://www.linkedin.com/in/manuelfbfilho) • [GitHub](https://github.com/manuelfbfilho)

