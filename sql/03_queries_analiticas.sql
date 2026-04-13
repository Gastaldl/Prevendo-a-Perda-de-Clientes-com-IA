-- =============================================================================
-- 03_queries_analiticas.sql — Queries para análise exploratória e Power BI
-- =============================================================================
-- Use estas queries para explorar os dados e como base para
-- as visualizações no Power BI.
-- =============================================================================


-- =============================================================================
-- ANÁLISE GERAL DO E-COMMERCE
-- =============================================================================

-- Visão geral: total de clientes, pedidos e receita
SELECT
    COUNT(DISTINCT c.id) AS total_clients,
    COUNT(DISTINCT o.id) AS total_orders,
    ROUND(SUM(o.total_value), 2) AS total_revenue,
    ROUND(AVG(o.total_value), 2) AS avg_ticket
FROM clients c
LEFT JOIN orders o ON c.id = o.client_id;


-- Distribuição de churn
SELECT
    CASE WHEN is_churned = 1 THEN 'Churned' ELSE 'Active' END AS status,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clients), 1) AS percentage
FROM clients
GROUP BY is_churned;


-- Receita por mês (para gráfico de linha)
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS num_orders,
    ROUND(SUM(total_value), 2) AS monthly_revenue
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;


-- Top 10 clientes por valor gasto
SELECT
    c.id,
    c.name,
    COUNT(o.id) AS total_orders,
    ROUND(SUM(o.total_value), 2) AS total_spent
FROM clients c
JOIN orders o ON c.id = o.client_id
GROUP BY c.id
ORDER BY total_spent DESC
LIMIT 10;


-- =============================================================================
-- ANÁLISE COMPARATIVA: CHURNED vs ATIVO
-- =============================================================================

-- Comparação de métricas entre clientes churned e ativos
SELECT
    CASE WHEN c.is_churned = 1 THEN 'Churned' ELSE 'Active' END AS status,
    COUNT(DISTINCT c.id) AS num_clients,
    ROUND(AVG(client_totals.total_spent), 2) AS avg_spent,
    ROUND(AVG(client_totals.total_orders), 1) AS avg_orders,
    ROUND(AVG(client_totals.avg_ticket), 2) AS avg_ticket
FROM clients c
JOIN (
    SELECT
        client_id,
        SUM(total_value) AS total_spent,
        COUNT(*) AS total_orders,
        AVG(total_value) AS avg_ticket
    FROM orders
    GROUP BY client_id
) client_totals ON c.id = client_totals.client_id
GROUP BY c.is_churned;


-- Distribuição de status de pedido por tipo de cliente
SELECT
    CASE WHEN c.is_churned = 1 THEN 'Churned' ELSE 'Active' END AS client_status,
    o.status AS order_status,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (
        PARTITION BY c.is_churned
    ), 1) AS percentage
FROM clients c
JOIN orders o ON c.id = o.client_id
GROUP BY c.is_churned, o.status;


-- =============================================================================
-- ANÁLISE DE SUPORTE
-- =============================================================================

-- Volume de interações por tipo e status do cliente
SELECT
    CASE WHEN c.is_churned = 1 THEN 'Churned' ELSE 'Active' END AS client_status,
    i.type,
    COUNT(*) AS count,
    ROUND(AVG(CASE WHEN i.resolved = 1 THEN 1.0 ELSE 0.0 END) * 100, 1) AS pct_resolved
FROM clients c
JOIN support_interactions i ON c.id = i.client_id
GROUP BY c.is_churned, i.type
ORDER BY c.is_churned, count DESC;


-- =============================================================================
-- QUERIES PARA O POWER BI (após Fase 3)
-- =============================================================================

-- Distribuição das probabilidades de churn
SELECT
    CASE
        WHEN churn_probability < 0.2 THEN '0-20% (Low)'
        WHEN churn_probability < 0.4 THEN '20-40%'
        WHEN churn_probability < 0.6 THEN '40-60% (Medium)'
        WHEN churn_probability < 0.8 THEN '60-80%'
        ELSE '80-100% (High)'
    END AS risk_tier,
    COUNT(*) AS num_clients
FROM churn_predictions
WHERE model_version = (
    SELECT model_version FROM churn_predictions
    ORDER BY prediction_date DESC LIMIT 1
)
GROUP BY risk_tier
ORDER BY risk_tier;


-- Evolução das métricas do modelo ao longo das versões
SELECT
    model_version,
    training_date,
    ROUND(accuracy * 100, 1) AS accuracy_pct,
    ROUND(precision * 100, 1) AS precision_pct,
    ROUND(recall * 100, 1) AS recall_pct,
    ROUND(f1_score * 100, 1) AS f1_pct,
    ROUND(auc_roc * 100, 1) AS auc_roc_pct
FROM training_history
ORDER BY training_date;


-- Clientes com maior risco de churn (ação de retenção)
SELECT
    c.id,
    c.name,
    c.email,
    c.city,
    c.state,
    ROUND(cp.churn_probability * 100, 1) AS churn_risk_pct,
    COALESCE(SUM(o.total_value), 0) AS total_spent
FROM clients c
JOIN churn_predictions cp ON c.id = cp.client_id
LEFT JOIN orders o ON c.id = o.client_id
WHERE cp.churn_probability > 0.7
  AND cp.model_version = (
      SELECT model_version FROM churn_predictions
      ORDER BY prediction_date DESC LIMIT 1
  )
GROUP BY c.id
ORDER BY cp.churn_probability DESC;
