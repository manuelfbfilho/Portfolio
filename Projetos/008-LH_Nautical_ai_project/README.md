<p align="center">
  <img src="https://img.shields.io/badge/Python-Data%20Platform-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Machine%20Learning-Forecasting-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Recommender-AI-purple?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit"/>
  <img src="https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge"/>
</p>
<table width="1000" align="center" cellpadding="0" cellspacing="0" style="border:none;">
  <tr>
    <td align="center" width="150">
      <img src="images/Fernandes.png" width="100"/></td>
    <td align="center" width="700"><h1 align="center"><b>🚤 LH Nautical<br>Data, Analytics & AI Platform</b></h1></td>
    <td align="center" width="150"><img src="images/Indicium_Academy.png" width="140"/></td>
  </tr>
</table>

<p align="center">
  <b>End-to-End Data Project: Engineering + Analytics + Machine Learning + AI</b>
</p>

---

# 🎥 Demo do Projeto

<p align="center">
  <img src="images/dashboard_gif.gif" width="800"/>
</p>

---

# 📌 Overview

Este projeto implementa uma plataforma completa de dados e inteligência artificial, cobrindo:

- Engenharia de Dados (ETL)
- Análise de Negócio
- Machine Learning
- Sistema de Recomendação
- Dashboard interativo

---

# 🎯 Problema de Negócio

A empresa enfrentava:

- Ruptura de estoque
- Excesso de produtos
- Falta de previsibilidade
- Ausência de inteligência de cliente
- Nenhum sistema de recomendação

---

# 🚀 Solução

* ✔ Pipeline de dados estruturado
* ✔ Análise de rentabilidade
* ✔ Segmentação de clientes
* ✔ Previsão de demanda
* ✔ Sistema de recomendação
* ✔ Dashboard interativo

---

# 🏗️ Arquitetura
```sql
Raw Data → ETL → Processed Data → ML Models → Dashboard
```
---

# 📊 Dashboard

## 🔹 Funcionalidades

- KPIs em tempo real  
- Filtros dinâmicos  
- Análise por produto, cliente e tempo  
- Previsão de demanda  
- Sistema de recomendação  

---

# 🤖 Machine Learning

## 📈 Forecasting
- Média móvel (baseline)
- MAE: 2.59

## 🧠 Recomendação
- Similaridade de cosseno
- Matriz usuário-item

## 📊 Clustering
- KMeans para segmentação de clientes

---

# 📁 Estrutura
```pgsql
lh_nautical_ai_project/
├── dashboard/
|      ├── pages/
│      └── utils/
├── data/
|     ├── processed/
│     └── raw/
├── docs/
├── images/
├── notebooks/
├── src/
│     └── data_engineering/
├── README.md
├── .gitignore
└── requirements.txt
```
---

# ⚙️ Tecnologias

- Python
- Pandas
- Scikit-learn
- Streamlit
- Plotly
- Power BI

---

# 🚀 Como Rodar Localmente

```bash
git clone https://github.com/SEU_USUARIO/lh_nautical_ai_project.git
cd lh_nautical_ai_project

pip install -r requirements.txt
streamlit run dashboard/app.py
```
---
# ☁️ Deploy (Streamlit Cloud)
1. Suba o projeto no GitHub
2. Acesse: https://streamlit.io/cloud
3. Clique em New App
4. Conecte seu repositório
5. Configure:
```
Main file: dashboard/app.py
```
6. Deploy 🚀

Link de acesso: https://lhnautical.streamlit.app/
---
# 📈 Insights

* Domingo = pior dia de vendas
* Produtos com prejuízo identificado
* Clientes premium compram múltiplas categorias
* Forte oportunidade de cross-sell

---
# 🔮 Próximos Passos

* Modelos avançados (XGBoost / LSTM)
* Deploy em AWS
* Pipeline automatizado (Airflow)
* MLOps

---
# 👨‍💻 Autor

<p>
<img src="https://avatars.githubusercontent.com/u/151965418?s=400&u=6c7f9f47152b9680683a3d090c4016d1acfdb6ee&v=4" width="100"/><br>
<b>Manuel Fernandes</b>
</p>

---
# 📜 Licença

MIT