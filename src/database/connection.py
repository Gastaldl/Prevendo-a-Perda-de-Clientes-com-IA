"""
Configuração da conexão com o banco de dados SQLite.

Módulo responsável por criar a engine, a session factory e a Base
do SQLAlchemy para uso em todo o projeto.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# Caminho do banco de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "ecommerce_churn.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    """Classe base para todos os modelos ORM."""
    pass


def get_engine():
    """Cria e retorna a engine do SQLAlchemy."""
    # TODO: Criar a engine usando create_engine()
    # Dica: use echo=True durante desenvolvimento para ver as queries SQL
    engine = create_engine("sqlite:///data/ecommerce_churn.db", echo=True)
    return engine


def get_session():
    """Cria e retorna uma session factory."""
    # TODO: Criar a session factory usando sessionmaker()
    # Dica: bind=get_engine()
    session = sessionmaker(bind=get_engine())
    return session


def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    # TODO: Usar Base.metadata.create_all() para criar as tabelas
    # Dica: importe os modelos antes de chamar create_all()
    from src.database.models import (
    Client, Product, Order, OrderItem,
    SupportInteraction, ChurnPrediction, TrainingHistory
    )
    Base.metadata.create_all(bind=get_engine())
