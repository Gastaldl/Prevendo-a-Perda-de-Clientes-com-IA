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
-- Dica: LEFT JOIN clientes com pedidos, GROUP BY cliente
-- SELECT
--     c.id AS cliente_id,
--     c.nome,
--     COUNT(p.id) AS total_pedidos,
--     COALESCE(SUM(p.valor_total), 0) AS total_gasto,
--     COALESCE(AVG(p.valor_total), 0) AS ticket_medio,
--     c.is_churned
-- FROM clientes c
-- LEFT JOIN pedidos p ON c.id = p.cliente_id
-- GROUP BY c.id;


-- =============================================================================
-- 2. FEATURES TEMPORAIS (Funções de Data)
-- =============================================================================

-- TODO: Dias desde o último pedido e dias como cliente
-- Dica: Use julianday() para calcular diferenças de datas no SQLite
-- SELECT
--     c.id,
--     CAST(julianday('now') - julianday(c.data_cadastro) AS INTEGER) AS dias_como_cliente,
--     CAST(julianday('now') - julianday(MAX(p.data_pedido)) AS INTEGER) AS dias_desde_ultimo_pedido
-- FROM clientes c
-- LEFT JOIN pedidos p ON c.id = p.cliente_id
-- GROUP BY c.id;


-- =============================================================================
-- 3. FEATURES DE SUPORTE (Subqueries)
-- =============================================================================

-- TODO: Métricas de interações com suporte por cliente
-- Dica: Use subqueries ou LEFT JOIN com agregação
-- SELECT
--     c.id,
--     COUNT(i.id) AS total_interacoes,
--     SUM(CASE WHEN i.tipo = 'reclamação' THEN 1 ELSE 0 END) AS total_reclamacoes,
--     AVG(CASE WHEN i.resolvido = 1 THEN 1.0 ELSE 0.0 END) AS taxa_resolucao
-- FROM clientes c
-- LEFT JOIN interacoes_suporte i ON c.id = i.cliente_id
-- GROUP BY c.id;


-- =============================================================================
-- 4. FEATURES COM JANELA DE TEMPO (Filtros Condicionais)
-- =============================================================================

-- TODO: Gasto nos últimos 90 dias vs gasto total
-- Dica: Use CASE WHEN com filtro de data
-- SELECT
--     c.id,
--     COALESCE(SUM(CASE
--         WHEN p.data_pedido >= date('now', '-90 days') THEN p.valor_total
--         ELSE 0
--     END), 0) AS gasto_ultimos_90_dias,
--     COALESCE(SUM(CASE
--         WHEN p.data_pedido >= date('now', '-30 days') THEN p.valor_total
--         ELSE 0
--     END), 0) AS gasto_ultimos_30_dias
-- FROM clientes c
-- LEFT JOIN pedidos p ON c.id = p.cliente_id
-- GROUP BY c.id;


-- =============================================================================
-- 5. FEATURES COM WINDOW FUNCTIONS (Avançado)
-- =============================================================================

-- TODO: Ranking de clientes por gasto e tendência de consumo
-- Dica: Use RANK(), ROW_NUMBER() e LAG()

-- Ranking de clientes por total gasto:
-- SELECT
--     c.id,
--     SUM(p.valor_total) AS total_gasto,
--     RANK() OVER (ORDER BY SUM(p.valor_total) DESC) AS ranking_gasto,
--     NTILE(4) OVER (ORDER BY SUM(p.valor_total) DESC) AS quartil_gasto
-- FROM clientes c
-- JOIN pedidos p ON c.id = p.cliente_id
-- GROUP BY c.id;

-- Evolução mensal de gastos por cliente (para detectar tendência):
-- SELECT
--     cliente_id,
--     strftime('%Y-%m', data_pedido) AS mes,
--     SUM(valor_total) AS gasto_mensal,
--     LAG(SUM(valor_total)) OVER (
--         PARTITION BY cliente_id ORDER BY strftime('%Y-%m', data_pedido)
--     ) AS gasto_mes_anterior
-- FROM pedidos
-- GROUP BY cliente_id, strftime('%Y-%m', data_pedido);


-- =============================================================================
-- 6. FEATURES DE DIVERSIDADE DE CONSUMO
-- =============================================================================

-- TODO: Quantas categorias distintas o cliente comprou
-- Dica: JOIN com itens_pedido e produtos
-- SELECT
--     c.id,
--     COUNT(DISTINCT pr.categoria) AS num_categorias_distintas,
--     COUNT(DISTINCT pr.id) AS num_produtos_distintos
-- FROM clientes c
-- LEFT JOIN pedidos p ON c.id = p.cliente_id
-- LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
-- LEFT JOIN produtos pr ON ip.produto_id = pr.id
-- GROUP BY c.id;


-- =============================================================================
-- 7. TAXA DE CANCELAMENTO / DEVOLUÇÃO
-- =============================================================================

-- TODO: Proporção de pedidos com problemas
-- SELECT
--     c.id,
--     COUNT(p.id) AS total_pedidos,
--     SUM(CASE WHEN p.status IN ('cancelado', 'devolvido') THEN 1 ELSE 0 END) AS pedidos_problematicos,
--     ROUND(
--         CAST(SUM(CASE WHEN p.status IN ('cancelado', 'devolvido') THEN 1 ELSE 0 END) AS REAL)
--         / NULLIF(COUNT(p.id), 0), 2
--     ) AS taxa_cancelamento
-- FROM clientes c
-- LEFT JOIN pedidos p ON c.id = p.cliente_id
-- GROUP BY c.id;


-- =============================================================================
-- 8. QUERY FINAL CONSOLIDADA (use esta como base no Python)
-- =============================================================================

-- TODO: Juntar tudo em uma única query grande!
-- Esta será a query principal do seu módulo src/features/extract.py
-- Combine todas as features acima usando CTEs (WITH) ou subqueries
-- Exemplo com CTE:
--
-- WITH features_compras AS (
--     SELECT ... FROM ... GROUP BY c.id
-- ),
-- features_suporte AS (
--     SELECT ... FROM ... GROUP BY c.id
-- ),
-- features_diversidade AS (
--     SELECT ... FROM ... GROUP BY c.id
-- )
-- SELECT
--     fc.*,
--     fs.total_interacoes,
--     fs.total_reclamacoes,
--     fd.num_categorias_distintas,
--     c.is_churned
-- FROM clientes c
-- LEFT JOIN features_compras fc ON c.id = fc.cliente_id
-- LEFT JOIN features_suporte fs ON c.id = fs.cliente_id
-- LEFT JOIN features_diversidade fd ON c.id = fd.cliente_id;
