from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    nombre: str | None = None

class UsuarioBase(BaseModel):
    nombre: str

class UsuarioCreate(UsuarioBase):
    password: str

class Config (BaseModel):
    id: int
    title: str
    class Config:
        orm_mode = True

class Usuario (UsuarioBase):
    id: int
    config: Config
    class Config:
        orm_mode = True