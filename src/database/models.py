"""
Modelos ORM do banco de dados.

Define as tabelas: clients, products, orders, order_items,
support_interactions, churn_predictions e training_history.
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    ForeignKey, Text, Date
)
from sqlalchemy.orm import relationship
from src.database.connection import Base


# =============================================================================
# FASE 1 — Tabelas principais do E-commerce
# =============================================================================

class Client(Base):
    """Tabela de clientes do e-commerce."""
    __tablename__ = "clients"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    id = Column(Integer, primary_key=True, autoincrement=True)
    #   - name (String, not null)
    name = Column(String, nullable=False)
    #   - email (String, unique, not null)
    email = Column(String, nullable=False)    
    #   - phone (String)
    phone = Column(String)
    #   - registration_date (DateTime, not null)
    registration_date = Column(DateTime, nullable=False)
    #   - city (String)
    city = Column(String)
    #   - state (String)
    state = Column(String)
    #   - gender (String)
    gender = Column(String)
    #   - birth_date (Date)
    birth_date = Column(Date)
    #   - is_churned (Boolean, default=False) — label para o modelo
    is_churned = Column(Boolean, default=False)
    #
    # TODO: Definir os relationships:
    #   - orders = relationship("Order", back_populates="client")
    orders = relationship("Order", back_populates="client")
    #   - interactions = relationship("SupportInteraction", back_populates="client")
    interactions = relationship("SupportInteraction", back_populates="client")


class Product(Base):
    """Tabela de produtos do catálogo."""
    __tablename__ = "products"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    id = Column(Integer, primary_key=True, autoincrement=True)
    #   - name (String, not null)
    name = Column(String, nullable=False)
    #   - category (String, not null)  — ex: Eletrônicos, Moda, Casa, etc.
    category = Column(String, nullable=False)
    #   - price (Float, not null)
    price = Column(Float, nullable=False)
    #   - description (Text)
    description = Column(Text)


class Order(Base):
    """Tabela de pedidos realizados."""
    __tablename__ = "orders"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    id = Column(Integer, primary_key=True, autoincrement=True)
    #   - client_id (Integer, ForeignKey("clients.id"), not null)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    #   - order_date (DateTime, not null)
    order_date = Column(DateTime, nullable=False)
    #   - total_value (Float, not null)
    total_value = Column(Float, nullable=False)
    #   - status (String, not null) — ex: "delivered", "cancelled", "returned"
    status = Column(String, nullable=False)
    #   - payment_method (String) — ex: "credit_card", "boleto", "pix"
    payment_method = Column(String)
    #
    # TODO: Definir os relationships:
    #   - client = relationship("Client", back_populates="orders")
    client = relationship("Client", back_populates="orders")
    #   - items = relationship("OrderItem", back_populates="order")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """Tabela associativa entre pedidos e produtos."""
    __tablename__ = "order_items"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    id = Column(Integer, primary_key=True, autoincrement=True)
    #   - order_id (Integer, ForeignKey("orders.id"), not null)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    #   - product_id (Integer, ForeignKey("products.id"), not null)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    #   - quantity (Integer, not null)
    quantity = Column(Integer, nullable=False)
    #   - unit_price (Float, not null)
    unit_price = Column(Float, nullable=False)
    #
    # TODO: Definir os relationships:
    #   - order = relationship("Order", back_populates="items")
    order = relationship("Order", back_populates="items")
    #   - product = relationship("Product")
    product = relationship("Product")


class SupportInteraction(Base):
    """Tabela de interações com o suporte ao cliente."""
    __tablename__ = "support_interactions"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    id = Column(Integer, primary_key=True, autoincrement=True)
    #   - client_id (Integer, ForeignKey("clients.id"), not null)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    #   - interaction_date (DateTime, not null)
    interaction_date = Column(DateTime, nullable=False)
    #   - type (String, not null) — ex: "complaint", "question", "praise", "exchange", "cancellation"
    type = Column(String, nullable=False)
    #   - channel (String) — ex: "chat", "email", "phone"
    channel = Column(String)
    #   - resolved (Boolean, default=False)
    resolved = Column(Boolean, default=False)
    #   - description (Text)
    description = Column(Text)
    #
    # TODO: Definir o relationship:
    #   - client = relationship("Client", back_populates="interactions")
    client = relationship("Client", back_populates="interactions")


# =============================================================================
# FASE 3 — Tabelas de resultados do modelo
# =============================================================================

class ChurnPrediction(Base):
    """Tabela para armazenar as previsões do modelo."""
    __tablename__ = "churn_predictions"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    id = Column(Integer, primary_key=True, autoincrement=True)
    #   - client_id (Integer, ForeignKey("clients.id"), not null)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    #   - churn_probability (Float, not null)
    churn_probability = Column(Float, nullable=False)
    #   - prediction (Boolean, not null) — True se prob > threshold
    prediction = Column(Boolean, nullable=False)
    #   - prediction_date (DateTime, not null)
    prediction_date = Column(DateTime, nullable=False)
    #   - model_version (String, not null) — ex: "v1.0"
    model_version = Column(String, nullable=False)


class TrainingHistory(Base):
    """Tabela para registrar o histórico de treinamentos do modelo."""
    __tablename__ = "training_history"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    id = Column(Integer, primary_key=True, autoincrement=True)
    #   - training_date (DateTime, not null)
    training_date = Column(DateTime, nullable=False)
    #   - model_version (String, not null)
    model_version = Column(String, nullable=False)
    #   - accuracy (Float)
    accuracy = Column(Float)
    #   - precision (Float)
    precision = Column(Float)
    #   - recall (Float)
    recall = Column(Float)
    #   - f1_score (Float)
    f1_score = Column(Float)
    #   - auc_roc (Float)
    auc_roc = Column(Float)
    #   - num_epochs (Integer)
    num_epochs = Column(Integer)
    #   - learning_rate (Float)
    learning_rate = Column(Float)
    #   - architecture (Text) — descrição da arquitetura usada
    architecture = Column(Text)
    #   - notes (Text)
    notes = Column(Text)
