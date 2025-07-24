<table width=1000 align="center" border=0>
<tr>
  <td align=center width=150><img src="images/Fernandes.png" width="120"/></td>
  <td align=center width=700><img src="images/Banner.png" width="600"/></td>
  <td align=center width=150><img src="images/one.png" width="120"></td>
</tr>
</table>

# 📊 Telecom X - Análise de Evasão de Clientes (Churn)

Projeto de Análise de Dados com foco em identificar padrões de evasão de clientes da empresa fictícia **Telecom X**, como parte da formação do curso **ONE - Oracle Next Education - Especialização em Data Science** utilizando o processo completo de **ETL (Extração, Transformação e Carga)**, aliado à **Análise Exploratória de Dados (EDA)** e visualizações estratégicas.

---

## 🎯 Objetivo

A Telecom X enfrenta uma alta taxa de evasão de clientes (churn), o que prejudica sua sustentabilidade financeira. Este projeto tem como objetivo:

- Extrair os dados de clientes a partir de uma API em JSON;
- Realizar a transformação e limpeza dos dados;
- Explorar os dados para identificar padrões e fatores associados à evasão;
- Fornecer recomendações estratégicas à empresa com base em dados.

---

## 🧰 Tecnologias e Bibliotecas Utilizadas

- **Python 3.x**
- **Pandas** – Manipulação de dados
- **NumPy** – Suporte matemático
- **Matplotlib & Seaborn** – Visualizações gráficas
- **Jupyter Notebook** – Ambiente interativo de análise
- **JSON** – Estrutura dos dados de entrada

---

## 📂 Estrutura do Projeto

```
📁 telecom-x-churn/
│
├── data/
│   └── TelecomX_Data.json
│
├── images/
│   ├── Fernandes.png
│   ├── one.png
│   ├── Banner.png
│
├── docs/
│   ├── Relatorio_ETL_TelecomX.pdf
│   ├── Relatorio_Final_TelecomX.md
│
├── TelecomX_ETL_EDA.ipynb
├── README.md
└── requirements.txt
```

---

## 📌 Etapas do Projeto

1. **Extração** dos dados via arquivo JSON oriundo de uma API.
2. **Transformação** com tratamento de dados ausentes, conversão de variáveis, criação de coluna `Contas_Diarias`, padronização de formatos.
3. **Carga e Análise (EDA)** com:
   - Distribuições por gênero, tipo de contrato, método de pagamento.
   - Relação entre tempo de permanência, valor gasto e evasão.
   - Análise temporal e sazonal da evasão.

---

## 📈 Exemplos de Visualizações de Análises Exploratórias de Dados (EDA)

### 🔹 Variáveis Categóricas

Foram exploradas variáveis como:
- Sexo, tipo de contrato, método de pagamento;
- Serviços de telefone, internet e streaming;
- Estado civil, dependentes e se é idoso.

### 🔹 Variáveis Numéricas

Foram analisadas:
- Gasto Mensal
- Gasto Total
- Tempo de Contrato

### 🔹 Correlação

Foi utilizada uma **matriz de correlação (heatmap)** para variáveis numéricas:
- Tempo de contrato, gasto mensal, gasto total e contas diárias.

---

## 💡 Principais Insights
Com base nas análises realizadas, os seguintes padrões foram identificados:

- Clientes com **contratos mensais** têm maior propensão à evasão;
- **Pagamentos eletrônicos automáticos** estão entre os métodos com maior churn;
- Clientes com **menor tempo de contrato**, **gasto total mais baixo** e **poucos serviços contratados** são mais propensos a sair;
- Serviços como **segurança online, suporte técnico e múltiplas linhas** estão associados a uma **menor taxa de evasão**;
- Pessoas **sem dependentes ou não casadas** tendem a evadir mais.

---

## ✅ Recomendações Estratégicas
Com base nos insights encontrados, recomendamos:

- Oferecer **benefícios para contratos anuais ou bienais**, com descontos ou bônus;
- Reforçar **programas de fidelidade** para novos clientes;
- Criar **alertas internos de churn** para clientes com perfis de alto risco (baixo gasto, pouco tempo de contrato, poucos serviços);
- Investir na **divulgação de serviços adicionais** como backup, segurança e suporte técnico;
- Promover ações específicas para **clientes solteiros ou sem dependentes**, como planos familiares ou personalizados.

---

## ▶️ Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/manuelfbfilho/portfolio/Projetos/005-TelecomX-P1.git
```

2. Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

3. Execute o notebook:

```bash
jupyter notebook notebooks/TelecomX_ETL_EDA.ipynb
```

---

## 📘 Relatório Completo

Você pode acessar o relatório completo com todas as análises e conclusões no diretório `/docs`.

---

## ✍️ Autor

**Manuel Fernandes**  
[LinkedIn](https://www.linkedin.com/in/manuelfbfilho) • [GitHub](https://github.com/manuelfbfilho)

---

## 🧠 Licença

Este projeto é livre para fins educacionais e profissionais, desde que citada a autoria.


