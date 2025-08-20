<table width=1000 align="center" border=0>
<tr>
  <td align=center width=150><img src="images/Fernandes.png" width="120"/></td>
  <td align=center width=700><img src="images/Banner.png" width="600"/></td>
  <td align=center width=150><img src="images/ONE-Challenge-TelecomX-P2.png" width="120"></td>
</tr>
</table>

# 📊 Telecom X – Parte 2: Prevendo Churn (EDA + ML + Calibração + SHAP)
O Telecom X é um projeto de análise e modelagem preditiva voltado para compreender e prever a evasão de clientes (churn) em uma empresa de telecomunicações.
A iniciativa foi desenvolvida como parte de um projeto acadêmico/prático, abrangendo desde a análise exploratória (EDA) até a implantação de um dashboard interativo em Dash/Plotly, com explicabilidade, calibração e recomendações de negócio.

## 🎯 Objetivo
O objetivo central do projeto é prever a probabilidade de churn dos clientes e identificar fatores determinantes que influenciam a evasão, permitindo que a empresa de telecom:
* Antecipe clientes com maior risco de cancelamento;
* Crie estratégias de retenção personalizadas;
* Apoie decisões de negócio baseadas em dados (data-driven).

### **Escopo completo conforme _backlog.ipynb_ e _Sobre.ipynb_:**
- EDA estatística (correlação numérica e **Cramer's V** para categóricas);
- **LPM (OLS)** para interpretação (regressão linear com _target_ 0/1);
- Pipelines de ML (**Logistic Regression** e **Random Forest**);
- **Validação k-fold (k=5)** com **ROC-AUC**;
- **Calibração** (sigmoid vs isotonic) e seleção por **AUC** com _tie-break_ de **Brier**;
- **Importância de variáveis** (coef./importances) e ranking;
- **Dashboard Dash + Plotly** com identidade visual;
- Documentação técnica (.docx) + README.

---

## 📂 Etapas do Projeto
### 1. Análise Exploratória de Dados (EDA)
* Limpeza e tratamento dos dados de churn;
* Análise estatística de variáveis categóricas e numéricas;
* Cálculo de correlações (Pearson) e associações (Cramer's V);
* Ajuste de modelo linear de probabilidade (LPM/OLS) para interpretação.

### 2. Modelagem Preditiva
* Construção de pipelines com Logistic Regression e Random Forest;
* Validação cruzada estratificada (k=5);
* Seleção do modelo via ROC-AUC e Brier Score (calibração).

### 3. Calibração e Explicabilidade
* Avaliação de calibração via curvas reliability (sigmoid vs isotonic);
* Geração de métricas adicionais (Precision, Recall, F1, AUC);
* Análise de importância de variáveis (coeficientes/importances e SHAP).

### 4. Dashboard Interativo (Dash + Plotly)
* Visualização da distribuição de probabilidades e ajuste de limiar;
* Exibição de métricas em cards dinâmicos;
* Curvas ROC, Precision–Recall e Calibração;
* Tabela de métricas por faixa de limiar com exportação CSV;
* Recomendações de ação automáticas por segmento de clientes.

### 5. Documentação e Comunicação
* Relatório em formato .docx com conclusões e recomendações de negócio;
* README.md padronizado com instruções de uso;
* Post no LinkedIn com resumo executivo do projeto.

---

## 📂 Estrutura do Projeto

```
📁 telecom-x-churn/
│
├── artifacts/
│   └── holdout_predictions.csv
│   └── shap_summary.csv
│   └── metrics.json
│   └── model.pkl
│   └── shap_top20.png
│
├── assets/
│   └── telecomx.css
│
├── data/
│   └── dados_tratados.csv
│
├── docs/
│   ├── Relatorio_TelecomX_Parte2.pdf
│   ├── Sobre.ipynb
│   ├── backlog.ipynb
│
├── images/
│   ├── Fernandes.png
│   ├── ONE-Challenge-TelecomX-P2.png
│   ├── Banner.png
|
├── src/
│   ├── app.py
│   ├── data_prep.py
│   ├── eda.py
│   ├── train.py
│
├── setup.bat
├── README.md
└── requirements.txt
```

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas
* Linguagem: Python 3.11
* Manipulação e análise de dados: pandas, numpy
* Modelagem estatística e machine learning: scikit-learn, statsmodels
* Explicabilidade: shap
* Visualização: plotly, seaborn, matplotlib
* Dashboard interativo: Dash (com dash-table)
* Documentação: python-docx
* Ambiente: virtualenv (.venv) + requirements.txt para reprodutibilidade

---

## 📁 Artefatos gerados
- `artifacts/corr_numeric.(csv|png)` — correlação numérica
- `artifacts/cramers_v.(csv|png)` — associação categórica
- `artifacts/lpm_summary.txt` — sumário do OLS (Linear Probability Model)
- `artifacts/feature_importance.csv` — ranking de importância
- `artifacts/shap_top20.png` — top 20 (proxy)
- `artifacts/model.pkl`, `artifacts/metrics.json`, `artifacts/holdout_predictions.csv`

---

## ▶️ Como executar
Clicando 2x no arquivo "setup.bat" e acessando o endereço apresentado no final da execução do arquivo

Ou

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

### 3. Treinar modelo
```bash
python src/train.py --data data/dados_tratados.csv --out artifacts/
```

## 4. Rodar dashboard
```bash
python src/app.py --data data/dados_tratados.csv --model artifacts/model.pkl
```

Outro Arquivo:
```bash
python srv/app_2.py
```
---

## ✍️ Autor

**Manuel Fernandes**  
[LinkedIn](https://www.linkedin.com/in/manuelfbfilho) • [GitHub](https://github.com/manuelfbfilho)

---

## 🧠 Licença

Este projeto é livre para fins educacionais e profissionais, desde que citada a autoria.


