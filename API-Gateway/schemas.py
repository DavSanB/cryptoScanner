# IMPORTS

from pydantic import BaseModel

# TOKEN

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    nombre: str | None = None

# Usuario
class UsuarioBase(BaseModel):
    nombre: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario (UsuarioBase):
    id: int
    config: Config
    class Config:
        orm_mode = True
        
# Config 
class ConfigUpdate (BaseModel):
    monedas: int
    orden: str
    
class Config (ConfigUpdate):
    id: int
    class Config:
        orm_mode = True
