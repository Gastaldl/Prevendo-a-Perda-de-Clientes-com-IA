-- =============================================================================
-- 01_schema.sql — Definição do schema do banco de dados
-- =============================================================================
-- Este arquivo serve como REFERÊNCIA para o schema.
-- Na prática, as tabelas são criadas pelo SQLAlchemy (Base.metadata.create_all).
-- Use este arquivo para estudo e para conectar o Power BI.
-- =============================================================================

-- Tabela de Clientes
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    registration_date DATETIME NOT NULL,
    city TEXT,
    state TEXT,
    gender TEXT,
    birth_date DATE,
    is_churned BOOLEAN DEFAULT 0
);

-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT
);

-- Tabela de Pedidos
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    order_date DATETIME NOT NULL,
    total_value REAL NOT NULL,
    status TEXT NOT NULL,         -- 'delivered', 'cancelled', 'returned'
    payment_method TEXT,          -- 'credit_card', 'boleto', 'pix'
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Tabela de Itens do Pedido
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Tabela de Interações com Suporte
CREATE TABLE IF NOT EXISTS support_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    interaction_date DATETIME NOT NULL,
    type TEXT NOT NULL,           -- 'complaint', 'question', 'praise', 'exchange', 'cancellation'
    channel TEXT,                 -- 'chat', 'email', 'phone'
    resolved BOOLEAN DEFAULT 0,
    description TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Tabela de Previsões de Churn (Fase 3)
CREATE TABLE IF NOT EXISTS churn_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    churn_probability REAL NOT NULL,
    prediction BOOLEAN NOT NULL,
    prediction_date DATETIME NOT NULL,
    model_version TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Tabela de Histórico de Treinamento (Fase 3)
CREATE TABLE IF NOT EXISTS training_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    training_date DATETIME NOT NULL,
    model_version TEXT NOT NULL,
    accuracy REAL,
    precision REAL,
    recall REAL,
    f1_score REAL,
    auc_roc REAL,
    num_epochs INTEGER,
    learning_rate REAL,
    architecture TEXT,
    notes TEXT
);

-- Índices para otimização de queries
CREATE INDEX IF NOT EXISTS idx_orders_client ON orders(client_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_interactions_client ON support_interactions(client_id);
CREATE INDEX IF NOT EXISTS idx_predictions_client ON churn_predictions(client_id);
