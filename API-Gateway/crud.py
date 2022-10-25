from sqlalchemy.orm import Session
import models, schemas

def get_usuario(db:Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuario_by_nombre(db:Session, nombre: str):
    return db.query(models.Usuario).filter(models.Usuario.nombre == nombre).first()

def get_usuarios(db:Session, skip: int=0, limit: int=100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def create_usuario(db:Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(nombre = usuario.nombre, hashed_password=usuario.password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    db_config = models.Config(idUsuario = db_usuario.id, monedas = 10, orden = "Cambio")
    db.add(db_config)
    db.commit()
    return db_usuario

def update_config(db:Session, usuario: int, config: schemas.ConfigUpdate):
    db_config = db.query(models.Config).filter(models.Config.idUsuario == usuario).first()
    db_config.monedas = config.monedas
    db_config.orden = config.orden
    db.commit()
    return db_config
