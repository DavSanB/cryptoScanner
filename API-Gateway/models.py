from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    config = relationship("Config", back_populates="usuario", uselist=False)

class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    idUsuario = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="config")
