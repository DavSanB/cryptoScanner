## IMPORTS 

from fastapi import Depends

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import models, schemas

class Security:

    def __init__(self, credentials_exception):
        # Token
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.SECRET_KEY = "31406a7b32e499dd919096b267a92233f8373b1b7fa1c4485a5c0ae1ee8adedd"

        #Encripción
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def get_password_hash(password):
        return pwd_context.hash(password)
    
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta:timedelta | None = None):

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, key = self.SECRET_KEY, algorithm = self.ALGORITHM)
        
        return encoded_jwt

    def authenticate_usuario(self, db: Session, nombre:str, password:str):
        db_usuario = crud.get_usuario_by_nombre(db=db, nombre=nombre)
        if not verify_password(password, db_usuario.hashed_password):
            return None

        return db_usuario

    def get_current_usuario(self, db: Session, token:str = Depends(self.oauth2_scheme)):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms = [self.ALGORITHM])
            db_usuario = crud.get_usuario_by_nombre(db, nombre = payload.get("sub"))
            return db_usuario
        except JWTError:
            return None


