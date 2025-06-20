from sqlalchemy.orm import Session
import models, schemas

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    novo_usuario = models.Usuario(**usuario.dict())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def obter_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()

def adicionar_senha_site(db: Session, id_usuario: int, senha: str):
    nova_senha = models.SenhaSite(id_usuario=id_usuario, senha=senha)
    db.add(nova_senha)
    db.commit()
    db.refresh(nova_senha)
    return nova_senha

def adicionar_senha_wifi(db: Session, id_usuario: int, senha: str):
    nova_senha = models.SenhaWiFi(id_usuario=id_usuario, senha=senha)
    db.add(nova_senha)
    db.commit()
    db.refresh(nova_senha)
    return nova_senha

def obter_senhas_usuario(db: Session, id_usuario: int):
    senhas_sites = db.query(models.SenhaSite).filter(models.SenhaSite.id_usuario == id_usuario).all()
    senhas_wifi = db.query(models.SenhaWiFi).filter(models.SenhaWiFi.id_usuario == id_usuario).all()
    return senhas_sites + senhas_wifi
