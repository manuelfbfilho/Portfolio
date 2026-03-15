<p align="center">
  <img src="https://img.shields.io/static/v1?label=Python&message=Data%20Pipeline&color=blue&style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/static/v1?label=Apache%20Airflow&message=Orchestration&color=red&style=for-the-badge&logo=apacheairflow"/>
  <img src="https://img.shields.io/static/v1?label=PostgreSQL&message=Database&color=green&style=for-the-badge&logo=postgresql"/><br>
  <img src="https://img.shields.io/static/v1?label=Docker&message=Containerization&color=blue&style=for-the-badge&logo=docker"/>
  <img src="https://img.shields.io/static/v1?label=Pandas&message=Data%20Processing&color=red&style=for-the-badge&logo=pandas"/>
  <img src="https://img.shields.io/static/v1?label=License&message=MIT&color=green&style=for-the-badge"/>
</p>
<table width="1000" cellpadding="0" cellspacing="0" style="border:none;>
  <tr style="border:none;">
    <td align="center" width="150" style="border:none;">
      <img src="https://github.com/manuelfbfilho/Portfolio/raw/master/Projetos/006-TelecomX-P2/images/Fernandes.png" width="100"/></td>
    <td align="center" width="700" style="border:none;"><font size=7><b>Pipeline ELT com Apache Airflow</b></font></td>
    <td align="center" width="150" style="border:none;"><img src="images/Indicium_Academy.png" width="140"/></td>
  </tr>
</table>

# 📌 Visão Geral do Projeto

Este projeto implementa um pipeline **ELT (Extract, Load, Transform)** utilizando **Apache Airflow** para orquestração, **PostgreSQL** como banco de origem e destino, e **Docker** para containerização do ambiente.

O objetivo do projeto é demonstrar na prática como construir um pipeline de dados completo, passando por todas as etapas essenciais:
  * Extração de dados de uma base operacional
  * Persistência intermediária em arquivo local
  * Carga em um banco de dados de destino
  * Validação da integridade dos dados carregados

A base de dados utilizada é a Northwind, uma base clássica usada para aprendizado de SQL e engenharia de dados.

<hr>

# 🎯 Objetivo

Este projeto tem como objetivo demonstrar na prática:
  ✔ construção de pipelines ELT
  ✔ orquestração com Apache Airflow
  ✔ manipulação de dados com Python e Pandas
  ✔ integração com bancos PostgreSQL
  ✔ uso de Docker para ambientes de dados
  ✔ organização de projetos de engenharia de dados

<hr>

# 🏗️ Arquitetura do Pipeline

```pgsql
                +---------------------+
                |   Source Database   |
                |    PostgreSQL       |
                |   (Northwind DB)    |
                |   Port: 5433        |
                +----------+----------+
                           |
                           |
                           v
                 +-------------------+
                 |   Apache Airflow  |
                 |   DAG Orchestrator|
                 |                   |
                 |  extract_task     |
                 |  load_task        |
                 |  validate_task    |
                 +---------+---------+
                           |
                           |
                           v
                +---------------------+
                |   Local Storage     |
                |  customers.csv      |
                |  (include folder)   |
                +----------+----------+
                           |
                           |
                           v
                +---------------------+
                |  Target Database    |
                |    PostgreSQL       |
                |     Port: 5434      |
                +----------+----------+
                           |
                           v
                 +------------------+
                 |   Validation     |
                 | SELECT COUNT(*)  |
                 | Expected = 91    |
                 +------------------+

```

### Fluxo de Dados
```pgsql
Extract → Persist → Load → Validate
```

<hr>

# ⚙️ Tecnologias Utilizadas
| **Tecnologia** | **Função no Projeto** |
|-|-|
| Python | Linguagem principal |
| Apache Airflow | Orquestração do pipeline |
| PostgreSQL | Banco de dados de origem e destino |
| Docker | Containerização do ambiente |
| Pandas | Manipulação e processamento de dados |
| Astronomer CLI | Execução local do Airflow |

<hr>

# 📁 Estrutura do Projeto
```pgsql
007-ELT-Airflow
│
├── dags
│   └── elt_customers_pipeline.py
│
├── scripts
│   ├── extract_customers.py
│   ├── load_customers.py
│   └── validate_customers.py
│
├── docker
│   └── docker-compose.yml
│
├── sql
│   └── northwind.sql
│
├── include
│
├── images
│   └── pipeline_execution.gif
│
├── requirements.txt
├── .gitignore
└── README.md
```

<hr>

# 🔧 Pré-requisitos

Antes de executar o projeto é necessário instalar:

1️⃣ **Git**
https://git-scm.com/

2️⃣ **Docker Desktop**
https://www.docker.com/products/docker-desktop/

Docker será utilizado para executar os bancos PostgreSQL.

3️⃣ **Python (3.10+)**
https://www.python.org/

4️⃣ **Astronomer CLI**
Ferramenta utilizada para executar o Apache Airflow localmente.

Documentação:
https://docs.astronomer.io/astro/cli/install-cli

5️⃣ **Cliente SQL (Opcional)**
Para visualizar os dados carregados.

Sugestões:
  * DBeaver
  * pgAdmin

<hr>

# 🚀 Instalação do Projeto
1️⃣ **Clonar o repositório**
```bash
git clone https://github.com/SEU_USUARIO/007-ELT-Airflow.git
```
No terminal, entrar na pasta do projeto (localmente)
```bash
cd 007-ELT-Airflow
```

<hr>

# 🐳 Subir os bancos PostgreSQL

**Entre na pasta docker:**
```bash
cd docker
```

**Execute:**
```bash
docker compose up -d
```

**Este comando irá criar dois bancos:**
| Banco | Porta | Função |
|-|-|
| source_db | 5433 | banco de origem |
| target_db | 5434 | banco de destino |

<hr>

# 🔌 Conexão com os bancos
**Banco de Origem**
```yaml
Host: localhost
Port: 5433
Database: source_db
User: postgres
Password: postgres
```

**Banco de Destino**
```yaml
Host: localhost
Port: 5434
Database: target_db
User: postgres
Password: postgres
```

<hr>

# 🌬️ Iniciando o Apache Airflow

Volte para a pasta principal do projeto.

Execute:
```powershell
astro dev start
```

Após iniciar, o Airflow estará disponível em:
```arduino
http://localhost:8080
```

Login padrão:
```pgsql
admin
admin
```

<hr>

# 🔗 Configuração das Conexões no Airflow

No menu:
```nginx
Admin → Connections
```

Criar duas conexões.

### **postgres_source**
```yaml
Connection Type: Postgres
Host: localhost
Port: 5433
Database: source_db
Login: postgres
Password: postgres
```

### **postgres_target**
```yaml
Connection Type: Postgres
Host: localhost
Port: 5434
Database: target_db
Login: postgres
Password: postgres
```

<hr>

# ▶️ Executando o Pipeline

No Airflow:
```nginx
DAGs → elt_customers_pipeline
```

Clique em:
```sql
Trigger DAG
```

<hr>

# 📊 Execução Esperada

Na interface do Airflow as tasks deverão aparecer como:
```bash
extract_task   success
load_task      success
validate_task  success
```

<hr>

# 🔍 Validação dos Dados

Conecte ao banco target_db utilizando DBeaver ou outro cliente SQL.

**Execute:**
```sql
SELECT COUNT(*) FROM customers;
```

**Resultado esperado:**
```
91
```

Isso confirma que o pipeline carregou corretamente os dados.

<hr>

# 📷 Demonstração da Execução

Adicione um GIF demonstrando a execução da DAG.
```bash
images/pipeline_execution.gif <criar imagem ou vídeo da execução>
```

**Exemplo:**
```bash
Trigger DAG → execução das tasks → consulta no banco destino
```

<hr>

# 📚 Conceitos Demonstrados

Este projeto demonstra conceitos importantes de engenharia de dados:
  * construção de pipelines ELT
  * orquestração de workflows
  * persistência intermediária de dados
  * integração com bancos relacionais
  * containerização de ambientes de dados
  * organização profissional de projetos de dados

<hr>

# 🧠 Aprendizados do Projeto

Durante o desenvolvimento deste projeto foram explorados conceitos como:
  * arquitetura de pipelines de dados
  * gerenciamento de dependências entre tarefas
  * tratamento de dados com Python e Pandas
  * execução de pipelines em ambientes containerizados
  * validação de dados em pipelines

<hr>

# 👨‍💻 Autor

<p>
<img src="https://avatars.githubusercontent.com/u/151965418?s=400&u=6c7f9f47152b9680683a3d090c4016d1acfdb6ee&v=4" width="100"/><br>
<b>Manuel Fernandes</b>
</p>

<hr>

Projeto desenvolvido como parte de estudos em Engenharia de Dados e Data Pipelines.

# 📜 Licença

Este projeto está licenciado sob a licença MIT.

<p><br><br></p>