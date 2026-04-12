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
    COUNT(DISTINCT c.id) AS total_clientes,
    COUNT(DISTINCT p.id) AS total_pedidos,
    ROUND(SUM(p.valor_total), 2) AS receita_total,
    ROUND(AVG(p.valor_total), 2) AS ticket_medio
FROM clientes c
LEFT JOIN pedidos p ON c.id = p.cliente_id;


-- Distribuição de churn
SELECT
    CASE WHEN is_churned = 1 THEN 'Churned' ELSE 'Ativo' END AS status,
    COUNT(*) AS quantidade,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clientes), 1) AS percentual
FROM clientes
GROUP BY is_churned;


-- Receita por mês (para gráfico de linha)
SELECT
    strftime('%Y-%m', data_pedido) AS mes,
    COUNT(*) AS num_pedidos,
    ROUND(SUM(valor_total), 2) AS receita_mensal
FROM pedidos
GROUP BY strftime('%Y-%m', data_pedido)
ORDER BY mes;


-- Top 10 clientes por valor gasto
SELECT
    c.id,
    c.nome,
    COUNT(p.id) AS total_pedidos,
    ROUND(SUM(p.valor_total), 2) AS total_gasto
FROM clientes c
JOIN pedidos p ON c.id = p.cliente_id
GROUP BY c.id
ORDER BY total_gasto DESC
LIMIT 10;


-- =============================================================================
-- ANÁLISE COMPARATIVA: CHURNED vs ATIVO
-- =============================================================================

-- Comparação de métricas entre clientes churned e ativos
SELECT
    CASE WHEN c.is_churned = 1 THEN 'Churned' ELSE 'Ativo' END AS status,
    COUNT(DISTINCT c.id) AS num_clientes,
    ROUND(AVG(total_por_cliente.total_gasto), 2) AS media_gasto,
    ROUND(AVG(total_por_cliente.total_pedidos), 1) AS media_pedidos,
    ROUND(AVG(total_por_cliente.ticket_medio), 2) AS media_ticket
FROM clientes c
JOIN (
    SELECT
        cliente_id,
        SUM(valor_total) AS total_gasto,
        COUNT(*) AS total_pedidos,
        AVG(valor_total) AS ticket_medio
    FROM pedidos
    GROUP BY cliente_id
) total_por_cliente ON c.id = total_por_cliente.cliente_id
GROUP BY c.is_churned;


-- Distribuição de status de pedido por tipo de cliente
SELECT
    CASE WHEN c.is_churned = 1 THEN 'Churned' ELSE 'Ativo' END AS status_cliente,
    p.status AS status_pedido,
    COUNT(*) AS quantidade,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (
        PARTITION BY c.is_churned
    ), 1) AS percentual
FROM clientes c
JOIN pedidos p ON c.id = p.cliente_id
GROUP BY c.is_churned, p.status;


-- =============================================================================
-- ANÁLISE DE SUPORTE
-- =============================================================================

-- Volume de interações por tipo e status do cliente
SELECT
    CASE WHEN c.is_churned = 1 THEN 'Churned' ELSE 'Ativo' END AS status_cliente,
    i.tipo,
    COUNT(*) AS quantidade,
    ROUND(AVG(CASE WHEN i.resolvido = 1 THEN 1.0 ELSE 0.0 END) * 100, 1) AS pct_resolvido
FROM clientes c
JOIN interacoes_suporte i ON c.id = i.cliente_id
GROUP BY c.is_churned, i.tipo
ORDER BY c.is_churned, quantidade DESC;


-- =============================================================================
-- QUERIES PARA O POWER BI (após Fase 3)
-- =============================================================================

-- Distribuição das probabilidades de churn
SELECT
    CASE
        WHEN probabilidade_churn < 0.2 THEN '0-20% (Baixo)'
        WHEN probabilidade_churn < 0.4 THEN '20-40%'
        WHEN probabilidade_churn < 0.6 THEN '40-60% (Médio)'
        WHEN probabilidade_churn < 0.8 THEN '60-80%'
        ELSE '80-100% (Alto)'
    END AS faixa_risco,
    COUNT(*) AS num_clientes
FROM previsoes_churn
WHERE versao_modelo = (
    SELECT versao_modelo FROM previsoes_churn
    ORDER BY data_previsao DESC LIMIT 1
)
GROUP BY faixa_risco
ORDER BY faixa_risco;


-- Evolução das métricas do modelo ao longo das versões
SELECT
    versao_modelo,
    data_treinamento,
    ROUND(acuracia * 100, 1) AS acuracia_pct,
    ROUND(precisao * 100, 1) AS precisao_pct,
    ROUND(recall * 100, 1) AS recall_pct,
    ROUND(f1_score * 100, 1) AS f1_pct,
    ROUND(auc_roc * 100, 1) AS auc_roc_pct
FROM historico_treinamento
ORDER BY data_treinamento;


-- Clientes com maior risco de churn (ação de retenção)
SELECT
    c.id,
    c.nome,
    c.email,
    c.cidade,
    c.estado,
    ROUND(pc.probabilidade_churn * 100, 1) AS risco_churn_pct,
    COALESCE(SUM(p.valor_total), 0) AS total_gasto
FROM clientes c
JOIN previsoes_churn pc ON c.id = pc.cliente_id
LEFT JOIN pedidos p ON c.id = p.cliente_id
WHERE pc.probabilidade_churn > 0.7
  AND pc.versao_modelo = (
      SELECT versao_modelo FROM previsoes_churn
      ORDER BY data_previsao DESC LIMIT 1
  )
GROUP BY c.id
ORDER BY pc.probabilidade_churn DESC;
