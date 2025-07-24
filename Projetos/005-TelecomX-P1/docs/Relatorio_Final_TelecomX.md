
# 4. Relatório Final

## 4.1. Introdução

Este projeto tem como objetivo realizar uma análise exploratória dos dados da empresa **Telecom X**, que enfrenta uma alta taxa de **evasão de clientes (Churn)**. A análise tem o propósito de identificar padrões e comportamentos que possam estar associados ao desligamento dos clientes, auxiliando assim a equipe de Data Science no desenvolvimento de estratégias e modelos preditivos que contribuam para a **retenção de clientes**.

---

## 4.2. Limpeza e Tratamento de Dados

O processo de ETL foi iniciado com a **extração dos dados** em formato JSON de uma API hospedada no GitHub. Após a importação, os dados passaram por uma etapa de normalização para que as colunas aninhadas fossem transformadas em um formato tabular adequado.

As principais etapas do tratamento incluíram:
- **Renomeação e tradução** dos nomes das colunas para o idioma português (Brasil);
- Conversão de colunas binárias para valores categóricos "Sim"/"Não";
- Conversão de campos numéricos;
- Criação da coluna `Contas_Diarias` com base na divisão do valor mensal por 30 dias;
- Criação da coluna `Qtd_Servicos` com a contagem dos serviços contratados por cliente.

---

## 4.3. Análise Exploratória de Dados (EDA)

A análise foi dividida em três grandes sessões:

### Sessão 1: Variáveis Categóricas
Foram exploradas variáveis como:
- Sexo, tipo de contrato, método de pagamento;
- Serviços de telefone, internet e streaming;
- Estado civil, dependentes e se é idoso.

Cada gráfico apresentou os percentuais de evasão por categoria, com **cores distintas e explicações visuais**.

### Sessão 2: Variáveis Numéricas
Foram analisadas:
- Gasto Mensal
- Gasto Total
- Tempo de Contrato

Essas variáveis foram visualizadas por meio de boxplots, segmentando clientes que evadiram ou não.

### Sessão 3: Correlação
Foi utilizada uma **matriz de correlação (heatmap)** para variáveis numéricas:
- Tempo de contrato, gasto mensal, gasto total e contas diárias.

---

## 4.4. Conclusões e Insights

Com base nas análises realizadas, os seguintes padrões foram identificados:
- Clientes com **contratos mensais** têm maior propensão à evasão;
- **Pagamentos eletrônicos automáticos** estão entre os métodos com maior churn;
- Clientes com **menor tempo de contrato**, **gasto total mais baixo** e **poucos serviços contratados** são mais propensos a sair;
- Serviços como **segurança online, suporte técnico e múltiplas linhas** estão associados a uma **menor taxa de evasão**;
- Pessoas **sem dependentes ou não casadas** tendem a evadir mais.

---

## 4.5. Recomendações

Com base nos insights encontrados, recomendamos:

- Oferecer **benefícios para contratos anuais ou bienais**, com descontos ou bônus;
- Reforçar **programas de fidelidade** para novos clientes;
- Criar **alertas internos de churn** para clientes com perfis de alto risco (baixo gasto, pouco tempo de contrato, poucos serviços);
- Investir na **divulgação de serviços adicionais** como backup, segurança e suporte técnico;
- Promover ações específicas para **clientes solteiros ou sem dependentes**, como planos familiares ou personalizados.

---

Essas ações poderão ser complementadas com o uso de modelos preditivos de churn e dashboards interativos em futuras etapas do projeto.
