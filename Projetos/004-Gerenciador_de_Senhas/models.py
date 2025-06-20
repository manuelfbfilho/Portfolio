from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_usuario = Column(String(40), nullable=False)
    login_usuario = Column(String(20), nullable=False, unique=True)
    data_nascimento = Column(DateTime, nullable=True)
    email_usuario = Column(String(50), unique=True, nullable=False)
    senha_mestre = Column(String(10), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    senhas_sites = relationship("SenhaSite", back_populates="usuario")
    senhas_wifi = relationship("SenhaWiFi", back_populates="usuario")

class SenhaSite(Base):
    __tablename__ = "senha_site"

    id_senha = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    senha = Column(String, nullable=False)

    usuario = relationship("Usuario", back_populates="senhas_sites")

class SenhaWiFi(Base):
    __tablename__ = "senha_wifi"

    id_senha = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    senha = Column(String, nullable=False)

    usuario = relationship("Usuario", back_populates="senhas_wifi")
