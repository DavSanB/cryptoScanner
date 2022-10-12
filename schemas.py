from pydantic import BaseModel

class UsuarioBase(BaseModel):
    email: str
    nombre: str

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario (UsuarioBase):
    id: int

    class Config:
        orm_mode = True