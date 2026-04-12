"""
Exportação de previsões e métricas para o banco de dados.

Salva os resultados do modelo nas tabelas previsoes_churn
e historico_treinamento.
"""
from datetime import datetime
from src.database.connection import get_session
from src.database.models import PrevisaoChurn, HistoricoTreinamento


def salvar_previsoes(
    cliente_ids: list,
    probabilidades: list,
    threshold: float = 0.5,
    versao_modelo: str = "v1.0"
):
    """
    Salva as previsões de churn no banco de dados.

    TODO: Implementar a inserção de previsões:
        1. Criar uma session do SQLAlchemy
        2. Para cada cliente, criar um objeto PrevisaoChurn com:
            - cliente_id
            - probabilidade_churn
            - previsao (True se prob > threshold)
            - data_previsao (datetime atual)
            - versao_modelo
        3. Fazer bulk insert (session.add_all)
        4. Commit e close

    Dicas:
        - Use session.bulk_save_objects() para performance
        - Trate exceções com try/except e rollback
        - Delete previsões antigas da mesma versão antes de inserir
    """
    pass


def salvar_historico_treinamento(metricas: dict, versao_modelo: str = "v1.0"):
    """
    Salva o histórico de treinamento no banco de dados.

    TODO: Implementar a inserção do histórico:
        1. Criar um objeto HistoricoTreinamento com as métricas
        2. Inserir no banco
        3. Commit e close

    Args:
        metricas: Dicionário com as métricas do treinamento
                  (acuracia, precisao, recall, f1_score, etc.)
        versao_modelo: Identificador da versão do modelo
    """
    pass


if __name__ == "__main__":
    # TODO: Orquestrar a exportação:
    # 1. Carregar o modelo treinado
    # 2. Fazer previsões para todos os clientes
    # 3. Salvar previsões no banco
    # 4. Salvar métricas no banco
    print("Exportação de resultados para o banco de dados")
