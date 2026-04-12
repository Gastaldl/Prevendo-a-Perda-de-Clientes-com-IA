-- =============================================================================
-- 01_schema.sql — Definição do schema do banco de dados
-- =============================================================================
-- Este arquivo serve como REFERÊNCIA para o schema.
-- Na prática, as tabelas são criadas pelo SQLAlchemy (Base.metadata.create_all).
-- Use este arquivo para estudo e para conectar o Power BI.
-- =============================================================================

-- Tabela de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefone TEXT,
    data_cadastro DATETIME NOT NULL,
    cidade TEXT,
    estado TEXT,
    genero TEXT,
    data_nascimento DATE,
    is_churned BOOLEAN DEFAULT 0
);

-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL,
    descricao TEXT
);

-- Tabela de Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_pedido DATETIME NOT NULL,
    valor_total REAL NOT NULL,
    status TEXT NOT NULL,         -- 'entregue', 'cancelado', 'devolvido'
    metodo_pagamento TEXT,        -- 'cartão', 'boleto', 'pix'
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela de Itens do Pedido
CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Tabela de Interações com Suporte
CREATE TABLE IF NOT EXISTS interacoes_suporte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_interacao DATETIME NOT NULL,
    tipo TEXT NOT NULL,           -- 'reclamação', 'dúvida', 'elogio', 'troca', 'cancelamento'
    canal TEXT,                   -- 'chat', 'email', 'telefone'
    resolvido BOOLEAN DEFAULT 0,
    descricao TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela de Previsões de Churn (Fase 3)
CREATE TABLE IF NOT EXISTS previsoes_churn (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    probabilidade_churn REAL NOT NULL,
    previsao BOOLEAN NOT NULL,
    data_previsao DATETIME NOT NULL,
    versao_modelo TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela de Histórico de Treinamento (Fase 3)
CREATE TABLE IF NOT EXISTS historico_treinamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_treinamento DATETIME NOT NULL,
    versao_modelo TEXT NOT NULL,
    acuracia REAL,
    precisao REAL,
    recall REAL,
    f1_score REAL,
    auc_roc REAL,
    num_epocas INTEGER,
    learning_rate REAL,
    arquitetura TEXT,
    observacoes TEXT
);

-- Índices para otimização de queries
CREATE INDEX IF NOT EXISTS idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_pedidos_data ON pedidos(data_pedido);
CREATE INDEX IF NOT EXISTS idx_itens_pedido ON itens_pedido(pedido_id);
CREATE INDEX IF NOT EXISTS idx_interacoes_cliente ON interacoes_suporte(cliente_id);
CREATE INDEX IF NOT EXISTS idx_previsoes_cliente ON previsoes_churn(cliente_id);
