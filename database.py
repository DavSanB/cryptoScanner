from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user    = "cryptoscanner"
passw   = "cryptoScanner"
host    = "localhost"
port    = "5432"
dbname  = "cryptoscanner"

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://" + user + ":" + passw + "@" + host + ":" + port + "/" + dbname

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False)
SessionLocal.configure(bind=engine)
Base = declarative_base()