"""
Extração de features a partir do banco de dados.

Executa queries SQL para criar features relevantes para
a previsão de churn e retorna um DataFrame pronto para modelagem.
"""
import pandas as pd
from src.database.connection import get_engine


def extrair_features() -> pd.DataFrame:
    """
    Extrai features do banco usando queries SQL e retorna um DataFrame.

    TODO: Implementar as queries SQL para extrair as seguintes features:

    Features de Compras:
        - total_orders: COUNT de pedidos por cliente
        - total_spent: SUM do total_value dos pedidos
        - avg_ticket: AVG do total_value
        - spent_last_90_days: SUM total_value WHERE order_date >= (hoje - 90 dias)
        - days_since_last_order: julianday('now') - julianday(MAX(order_date))
        - cancellation_rate: proporção de pedidos cancelled/returned

    Features de Suporte:
        - total_interactions: COUNT de interações por cliente
        - total_complaints: COUNT WHERE type = 'complaint'
        - resolution_rate: proporção de interações resolvidas (resolved)
        - days_since_last_interaction: similar ao de pedidos

    Features de Perfil:
        - days_as_client: julianday('now') - julianday(registration_date)
        - distinct_categories_count: COUNT DISTINCT de categorias compradas

    Features Avançadas (Window Functions):
        - spending_trend: comparar gasto dos últimos 30 dias vs 30-60 dias
        - spending_rank: RANK() do cliente por total gasto

    Label:
        - is_churned: coluna alvo (0 ou 1)

    Dicas de SQL:
        - Use JOINs entre clients, orders, order_items e products
        - Use CASE WHEN para cálculos condicionais
        - Use COALESCE para tratar NULLs
        - Use window functions: ROW_NUMBER(), RANK(), LAG()
        - Agrupe por client_id usando GROUP BY

    Returns:
        DataFrame com uma linha por cliente e todas as features.
    """
    engine = get_engine()

    # TODO: Escrever a query SQL principal
    # query = """
    #     SELECT
    #         c.id AS client_id,
    #         ...
    #     FROM clients c
    #     LEFT JOIN orders o ON c.id = o.client_id
    #     ...
    #     GROUP BY c.id
    # """

    # TODO: Executar a query e retornar o DataFrame
    # df = pd.read_sql(query, engine)
    # return df
    pass


def preparar_dados(df: pd.DataFrame) -> tuple:
    """
    Pré-processa o DataFrame para alimentar o modelo.

    TODO: Implementar o pré-processamento:
        1. Tratar valores nulos (fillna ou drop)
        2. Separar features (X) e label (y)
        3. Normalizar features numéricas (StandardScaler ou MinMaxScaler)
        4. Fazer train/test split (80/20 ou 70/30)
        5. Converter para tensores PyTorch

    Returns:
        Tupla (X_train, X_test, y_train, y_test)
    """
    pass


if __name__ == "__main__":
    df = extrair_features()
    if df is not None:
        print(f"Features extraídas: {df.shape}")
        print(f"Colunas: {df.columns.tolist()}")
        print(f"\nDistribuição de churn:")
        print(df["is_churned"].value_counts())
