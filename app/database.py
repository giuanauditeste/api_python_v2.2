from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("Variável de ambiente DATABASE_URL não configurada.")
    raise ValueError("DATABASE_URL environment variable not set")

print(f"Using database: {DATABASE_URL}")

# Configurações robustas do pool de conexões para prevenir timeouts
engine = create_engine(
    DATABASE_URL,
    # Configurações do pool de conexões
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_recycle=1800,   # Recicla conexões a cada 30 minutos
    pool_size=10,        # Tamanho do pool
    max_overflow=20,     # Máximo de conexões extras
    pool_timeout=30,     # Timeout para obter conexão do pool
    
    # Configurações de conexão TCP para manter conexões ativas
    connect_args={
        "options": "-c statement_timeout=30000",  # Timeout de 30 segundos para statements
        "keepalives_idle": 600,      # Envia keepalive após 10 minutos de inatividade
        "keepalives_interval": 30,   # Intervalo entre keepalives (30 segundos)
        "keepalives_count": 5        # Número máximo de keepalives antes de considerar conexão morta
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def create_tables():
#     Base.metadata.create_all(bind=engine)
