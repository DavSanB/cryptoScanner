# IMPORTS

from datetime import datetime, timedelta

## Imports de FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status

## Imports de Seguridad
from security import Security
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

## Imports de Base de Datos
import crud, models, schemas
from sqlalchemy.orm import Session
from database import SessionLocal, engine

## Configuracion TOKEN de seguridad

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
sec = Security()

# Configuración de CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/usuarios", response_model=schemas.Token)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_nombre(db=db, nombre=usuario.nombre)

    if db_usuario:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail      = "Usuario existente!"
        )

    usuario.password = sec.get_password_hash(usuario.password)
    usuario = crud.create_usuario(db, usuario=usuario)

    access_token = sec.create_access_token(nombre = usuario.nombre)

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=schemas.Token)
def login(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = sec.authenticate_usuario(db, usuario.nombre, usuario.password)

    if db_usuario is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail      = "Contraseña o Usuario incorrectos",
            headers     = {"WWW-Authenticate": "Bearer"},
        )

    access_token = sec.create_access_token(nombre = usuario.nombre)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/usuarios", response_model=schemas.Usuario)
def get_config(db: Session = Depends(get_db), token:str = Depends(oauth2_scheme)):
    current_usuario: schemas.Usuario = sec.get_current_usuario(db=db, token = token)
    return current_usuario

@app.get("/usuarios/config", response_model=schemas.Config)
def get_config(db: Session = Depends(get_db), token:str = Depends(oauth2_scheme)):
    current_usuario: schemas.Usuario = sec.get_current_usuario(db=db, token = token)
    return current_usuario.config

@app.put("/usuarios/config" , response_model=schemas.Config)
def update_config(config:schemas.ConfigUpdate, db: Session = Depends(get_db), token:str = Depends(oauth2_scheme)):
    current_usuario: schemas.Usuario = sec.get_current_usuario(db=db, token = token)
    config = crud.update_config(db=db, usuario=current_usuario.id, config = config)
    return config