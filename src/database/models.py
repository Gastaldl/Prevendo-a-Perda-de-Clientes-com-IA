"""
Modelos ORM do banco de dados.

Define as tabelas: clientes, produtos, pedidos, itens_pedido,
interacoes_suporte, previsoes_churn e historico_treinamento.
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

class Cliente(Base):
    """Tabela de clientes do e-commerce."""
    __tablename__ = "clientes"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    #   - nome (String, not null)
    #   - email (String, unique, not null)
    #   - telefone (String)
    #   - data_cadastro (DateTime, not null)
    #   - cidade (String)
    #   - estado (String)
    #   - genero (String)
    #   - data_nascimento (Date)
    #   - is_churned (Boolean, default=False) — label para o modelo
    #
    # TODO: Definir os relationships:
    #   - pedidos = relationship("Pedido", back_populates="cliente")
    #   - interacoes = relationship("InteracaoSuporte", back_populates="cliente")
    pass


class Produto(Base):
    """Tabela de produtos do catálogo."""
    __tablename__ = "produtos"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    #   - nome (String, not null)
    #   - categoria (String, not null)  — ex: Eletrônicos, Moda, Casa, etc.
    #   - preco (Float, not null)
    #   - descricao (Text)
    pass


class Pedido(Base):
    """Tabela de pedidos realizados."""
    __tablename__ = "pedidos"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    #   - cliente_id (Integer, ForeignKey("clientes.id"), not null)
    #   - data_pedido (DateTime, not null)
    #   - valor_total (Float, not null)
    #   - status (String, not null) — ex: "entregue", "cancelado", "devolvido"
    #   - metodo_pagamento (String) — ex: "cartão", "boleto", "pix"
    #
    # TODO: Definir os relationships:
    #   - cliente = relationship("Cliente", back_populates="pedidos")
    #   - itens = relationship("ItemPedido", back_populates="pedido")
    pass


class ItemPedido(Base):
    """Tabela associativa entre pedidos e produtos."""
    __tablename__ = "itens_pedido"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    #   - pedido_id (Integer, ForeignKey("pedidos.id"), not null)
    #   - produto_id (Integer, ForeignKey("produtos.id"), not null)
    #   - quantidade (Integer, not null)
    #   - preco_unitario (Float, not null)
    #
    # TODO: Definir os relationships:
    #   - pedido = relationship("Pedido", back_populates="itens")
    #   - produto = relationship("Produto")
    pass


class InteracaoSuporte(Base):
    """Tabela de interações com o suporte ao cliente."""
    __tablename__ = "interacoes_suporte"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    #   - cliente_id (Integer, ForeignKey("clientes.id"), not null)
    #   - data_interacao (DateTime, not null)
    #   - tipo (String, not null) — ex: "reclamação", "dúvida", "elogio", "troca"
    #   - canal (String) — ex: "chat", "email", "telefone"
    #   - resolvido (Boolean, default=False)
    #   - descricao (Text)
    #
    # TODO: Definir o relationship:
    #   - cliente = relationship("Cliente", back_populates="interacoes")
    pass


# =============================================================================
# FASE 3 — Tabelas de resultados do modelo
# =============================================================================

class PrevisaoChurn(Base):
    """Tabela para armazenar as previsões do modelo."""
    __tablename__ = "previsoes_churn"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    #   - cliente_id (Integer, ForeignKey("clientes.id"), not null)
    #   - probabilidade_churn (Float, not null)
    #   - previsao (Boolean, not null) — True se prob > threshold
    #   - data_previsao (DateTime, not null)
    #   - versao_modelo (String, not null) — ex: "v1.0"
    pass


class HistoricoTreinamento(Base):
    """Tabela para registrar o histórico de treinamentos do modelo."""
    __tablename__ = "historico_treinamento"

    # TODO: Definir as colunas:
    #   - id (Integer, primary_key)
    #   - data_treinamento (DateTime, not null)
    #   - versao_modelo (String, not null)
    #   - acuracia (Float)
    #   - precisao (Float)  — precision
    #   - recall (Float)
    #   - f1_score (Float)
    #   - auc_roc (Float)
    #   - num_epocas (Integer)
    #   - learning_rate (Float)
    #   - arquitetura (Text) — descrição da arquitetura usada
    #   - observacoes (Text)
    pass
