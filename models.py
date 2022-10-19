from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
#from sqlalchemy.orm import relationship

from database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    hashed_password = Column(String)