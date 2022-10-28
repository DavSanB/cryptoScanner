# IMPORTS

from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String

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
    monedas = Column(Integer, index=True)
    orden =  Column(String, index=True)

    idUsuario = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="config")
