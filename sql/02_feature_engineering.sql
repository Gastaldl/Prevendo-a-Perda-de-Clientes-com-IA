-- =============================================================================
-- 02_feature_engineering.sql — Queries de Feature Engineering
-- =============================================================================
-- Pratique estas queries para extrair features relevantes para o modelo.
-- Depois, integre-as no módulo src/features/extract.py
-- =============================================================================


-- =============================================================================
-- 1. FEATURES BÁSICAS DE COMPRAS (JOINs + Agregações)
-- =============================================================================

-- TODO: Total de pedidos e valor gasto por cliente
-- Dica: LEFT JOIN clients com orders, GROUP BY cliente
-- SELECT
--     c.id AS client_id,
--     c.name,
--     COUNT(o.id) AS total_orders,
--     COALESCE(SUM(o.total_value), 0) AS total_spent,
--     COALESCE(AVG(o.total_value), 0) AS avg_ticket,
--     c.is_churned
-- FROM clients c
-- LEFT JOIN orders o ON c.id = o.client_id
-- GROUP BY c.id;


-- =============================================================================
-- 2. FEATURES TEMPORAIS (Funções de Data)
-- =============================================================================

-- TODO: Dias desde o último pedido e dias como cliente
-- Dica: Use julianday() para calcular diferenças de datas no SQLite
-- SELECT
--     c.id,
--     CAST(julianday('now') - julianday(c.registration_date) AS INTEGER) AS days_as_client,
--     CAST(julianday('now') - julianday(MAX(o.order_date)) AS INTEGER) AS days_since_last_order
-- FROM clients c
-- LEFT JOIN orders o ON c.id = o.client_id
-- GROUP BY c.id;


-- =============================================================================
-- 3. FEATURES DE SUPORTE (Subqueries)
-- =============================================================================

-- TODO: Métricas de interações com suporte por cliente
-- Dica: Use subqueries ou LEFT JOIN com agregação
-- SELECT
--     c.id,
--     COUNT(i.id) AS total_interactions,
--     SUM(CASE WHEN i.type = 'complaint' THEN 1 ELSE 0 END) AS total_complaints,
--     AVG(CASE WHEN i.resolved = 1 THEN 1.0 ELSE 0.0 END) AS resolution_rate
-- FROM clients c
-- LEFT JOIN support_interactions i ON c.id = i.client_id
-- GROUP BY c.id;


-- =============================================================================
-- 4. FEATURES COM JANELA DE TEMPO (Filtros Condicionais)
-- =============================================================================

-- TODO: Gasto nos últimos 90 dias vs gasto total
-- Dica: Use CASE WHEN com filtro de data
-- SELECT
--     c.id,
--     COALESCE(SUM(CASE
--         WHEN o.order_date >= date('now', '-90 days') THEN o.total_value
--         ELSE 0
--     END), 0) AS spent_last_90_days,
--     COALESCE(SUM(CASE
--         WHEN o.order_date >= date('now', '-30 days') THEN o.total_value
--         ELSE 0
--     END), 0) AS spent_last_30_days
-- FROM clients c
-- LEFT JOIN orders o ON c.id = o.client_id
-- GROUP BY c.id;


-- =============================================================================
-- 5. FEATURES COM WINDOW FUNCTIONS (Avançado)
-- =============================================================================

-- TODO: Ranking de clientes por gasto e tendência de consumo
-- Dica: Use RANK(), ROW_NUMBER() e LAG()

-- Ranking de clientes por total gasto:
-- SELECT
--     c.id,
--     SUM(o.total_value) AS total_spent,
--     RANK() OVER (ORDER BY SUM(o.total_value) DESC) AS spending_rank,
--     NTILE(4) OVER (ORDER BY SUM(o.total_value) DESC) AS spending_quartile
-- FROM clients c
-- JOIN orders o ON c.id = o.client_id
-- GROUP BY c.id;

-- Evolução mensal de gastos por cliente (para detectar tendência):
-- SELECT
--     client_id,
--     strftime('%Y-%m', order_date) AS month,
--     SUM(total_value) AS monthly_spent,
--     LAG(SUM(total_value)) OVER (
--         PARTITION BY client_id ORDER BY strftime('%Y-%m', order_date)
--     ) AS previous_month_spent
-- FROM orders
-- GROUP BY client_id, strftime('%Y-%m', order_date);


-- =============================================================================
-- 6. FEATURES DE DIVERSIDADE DE CONSUMO
-- =============================================================================

-- TODO: Quantas categorias distintas o cliente comprou
-- Dica: JOIN com order_items e products
-- SELECT
--     c.id,
--     COUNT(DISTINCT pr.category) AS distinct_categories_count,
--     COUNT(DISTINCT pr.id) AS distinct_products_count
-- FROM clients c
-- LEFT JOIN orders o ON c.id = o.client_id
-- LEFT JOIN order_items oi ON o.id = oi.order_id
-- LEFT JOIN products pr ON oi.product_id = pr.id
-- GROUP BY c.id;


-- =============================================================================
-- 7. TAXA DE CANCELAMENTO / DEVOLUÇÃO
-- =============================================================================

-- TODO: Proporção de pedidos com problemas
-- SELECT
--     c.id,
--     COUNT(o.id) AS total_orders,
--     SUM(CASE WHEN o.status IN ('cancelled', 'returned') THEN 1 ELSE 0 END) AS problematic_orders,
--     ROUND(
--         CAST(SUM(CASE WHEN o.status IN ('cancelled', 'returned') THEN 1 ELSE 0 END) AS REAL)
--         / NULLIF(COUNT(o.id), 0), 2
--     ) AS cancellation_rate
-- FROM clients c
-- LEFT JOIN orders o ON c.id = o.client_id
-- GROUP BY c.id;


-- =============================================================================
-- 8. QUERY FINAL CONSOLIDADA (use esta como base no Python)
-- =============================================================================

-- TODO: Juntar tudo em uma única query grande!
-- Esta será a query principal do seu módulo src/features/extract.py
-- Combine todas as features acima usando CTEs (WITH) ou subqueries
-- Exemplo com CTE:
--
-- WITH purchase_features AS (
--     SELECT ... FROM ... GROUP BY c.id
-- ),
-- support_features AS (
--     SELECT ... FROM ... GROUP BY c.id
-- ),
-- diversity_features AS (
--     SELECT ... FROM ... GROUP BY c.id
-- )
-- SELECT
--     pf.*,
--     sf.total_interactions,
--     sf.total_complaints,
--     df.distinct_categories_count,
--     c.is_churned
-- FROM clients c
-- LEFT JOIN purchase_features pf ON c.id = pf.client_id
-- LEFT JOIN support_features sf ON c.id = sf.client_id
-- LEFT JOIN diversity_features df ON c.id = df.client_id;
