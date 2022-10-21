from datetime import datetime, timedelta
## Imports de FastAPI 
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
## Imports de Seguridad
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
## Imports de Base de Datos
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

## Configuracion TOKEN de seguridad
SECRET_KEY = "31406a7b32e499dd919096b267a92233f8373b1b7fa1c4485a5c0ae1ee8adedd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

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
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_usuario(db: Session, nombre:str, password:str):
    db_usuario = crud.get_usuario_by_nombre(db=db, nombre=nombre)
    if db_usuario is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña o Usuario incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, db_usuario.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña o Usuario incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_usuario

def create_access_token(data: dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_usuario(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se validaron las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nombre: str = payload.get("sub")
        if nombre is None:
            raise credentials_exception
        token_data= schemas.TokenData(nombre=nombre)
    except JWTError:
        raise credentials_exception

    db_usuario = crud.get_usuario_by_nombre(db, nombre=token_data.nombre)
    if db_usuario is None:
        raise credentials_exception
    return db_usuario

def get_current_usuario_activo(current_usuario: models.Usuario = Depends(get_current_usuario)):
    return current_usuario

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario = authenticate_usuario(db, usuario.nombre, usuario.password)
    db_usuario = crud.get_usuario_by_nombre(db, nombre=usuario.nombre)
    if db_usuario is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña o Usuario incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    acces_token = create_access_token(
        data = {"sub": db_usuario.nombre}, expires_delta=access_token_expires
    )
    return {"access_token": acces_token, "token_type": "bearer"}

@app.post("/usuarios", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_nombre(db=db, nombre=usuario.nombre)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Usuario existente!")
    usuario.password = get_password_hash(usuario.password)
    return crud.create_usuario(db, usuario=usuario)

@app.get("/usuarios", response_model=schemas.Usuario)
def get_config(current_usuario: schemas.Usuario = Depends(get_current_usuario_activo)):
    return current_usuario

@app.get("/usuarios/config", response_model=schemas.Config)
def get_config(current_usuario: schemas.Usuario = Depends(get_current_usuario_activo)):
    return current_usuario.config
