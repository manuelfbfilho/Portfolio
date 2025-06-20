from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UsuarioBase(BaseModel):
    nome_usuario: str
    login_usuario: str
    data_nascimento: Optional[datetime] = None
    email_usuario: EmailStr
    senha_mestre: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    data_criacao: datetime

    class Config:
        orm_mode = True

class SenhaBase(BaseModel):
    senha: str

class SenhaCreate(SenhaBase):
    pass

class SenhaResponse(SenhaBase):
    id_senha: int
    id_usuario: int

    class Config:
        orm_mode = True
