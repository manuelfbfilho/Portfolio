@echo off
echo ====== Telecom X - Setup ======

REM Criar ambiente virtual
python -m venv .venv

REM Ativar ambiente virtual
call .venv\Scripts\activate

REM Atualizar pip
python -m pip install --upgrade pip

REM Instalar dependências
pip install -r requirements.txt

REM Treinar modelo e gerar artefatos
python src\train.py --data data\dados_tratados.csv --out artifacts\

REM Rodar dashboard
python src\app.py --data data\dados_tratados.csv --model artifacts\model.pkl

pause

