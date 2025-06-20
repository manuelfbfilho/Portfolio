from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas, security
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.criar_usuario(db, usuario)

@app.post("/senhas/site/{id_usuario}/")
def adicionar_senha_site(id_usuario: int, senha: schemas.SenhaCreate, db: Session = Depends(get_db)):
    return crud.adicionar_senha_site(db, id_usuario, senha.senha)

@app.get("/senhas/verificar/{id_usuario}/")
def verificar_senhas(id_usuario: int, db: Session = Depends(get_db)):
    senhas_cadastradas = crud.obter_senhas_usuario(db, id_usuario)
    senhas = [s.senha for s in senhas_cadastradas]
    
    for senha in senhas:
        if security.verificar_senha_fraca(senha, senhas):
            return {"mensagem": f"A senha '{senha}' é fraca!"}
    return {"mensagem": "Todas as senhas são seguras!"}

@app.get("/senha/gerar/")
def gerar_senha():
    return {"senha_forte": security.gerar_senha_forte(16)}
