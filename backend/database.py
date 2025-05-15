from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ajuste sua string de conexão conforme necessário:
# SQLALCHEMY_DATABASE_URL = "postgresql://seu_usuario:sua_senha@localhost:5432/receitas_culinarias"
SQLALCHEMY_DATABASE_URL = "postgresql://collage:collage1@localhost:5432/receitas_culinarias"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/receitas"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
