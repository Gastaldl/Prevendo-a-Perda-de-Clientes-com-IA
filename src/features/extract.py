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
        - total_pedidos: COUNT de pedidos por cliente
        - total_gasto: SUM do valor_total dos pedidos
        - ticket_medio: AVG do valor_total
        - total_gasto_90dias: SUM valor_total WHERE data_pedido >= (hoje - 90 dias)
        - dias_desde_ultimo_pedido: julianday('now') - julianday(MAX(data_pedido))
        - taxa_cancelamento: proporção de pedidos cancelados/devolvidos

    Features de Suporte:
        - total_interacoes: COUNT de interações por cliente
        - total_reclamacoes: COUNT WHERE tipo = 'reclamação'
        - taxa_resolucao: proporção de interações resolvidas
        - dias_desde_ultima_interacao: similar ao de pedidos

    Features de Perfil:
        - dias_como_cliente: julianday('now') - julianday(data_cadastro)
        - num_categorias_distintas: COUNT DISTINCT de categorias compradas

    Features Avançadas (Window Functions):
        - tendencia_gasto: comparar gasto dos últimos 30 dias vs 30-60 dias
        - ranking_gasto: RANK() do cliente por total gasto

    Label:
        - is_churned: coluna alvo (0 ou 1)

    Dicas de SQL:
        - Use JOINs entre clientes, pedidos, itens_pedido e produtos
        - Use CASE WHEN para cálculos condicionais
        - Use COALESCE para tratar NULLs
        - Use window functions: ROW_NUMBER(), RANK(), LAG()
        - Agrupe por cliente_id usando GROUP BY

    Returns:
        DataFrame com uma linha por cliente e todas as features.
    """
    engine = get_engine()

    # TODO: Escrever a query SQL principal
    # query = """
    #     SELECT
    #         c.id AS cliente_id,
    #         ...
    #     FROM clientes c
    #     LEFT JOIN pedidos p ON c.id = p.cliente_id
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
