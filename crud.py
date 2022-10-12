from sqlalchemy.orm import Session
import models, schemas

def get_usuario(db:Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_by_email(db:Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_usuarios(db:Session, skip: int=0, limit: int=100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db:Session, usuario: schemas.UsuarioCreate):
    fake_hashed_password = usuario.password + 'notreallyhashed'
    db_usuario = models.Usuario(email = usuario.email, hashed_password= fake_hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario