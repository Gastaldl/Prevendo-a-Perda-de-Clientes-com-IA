"""
Importação de datasets reais do Kaggle para o banco de dados.

Este módulo é usado na Fase 5, após o pipeline estar validado
com dados sintéticos (Faker). Ele lê CSVs do Kaggle, mapeia
as colunas para o schema existente e insere no banco.
"""
import pandas as pd
import os
from src.database.connection import get_engine, get_session, init_db, Base

# Caminho para os datasets baixados do Kaggle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")


def explorar_dataset(filepath: str):
    """
    Explora um dataset CSV do Kaggle e exibe informações úteis.

    TODO: Implementar a exploração:
        1. Ler o CSV com pd.read_csv()
        2. Exibir: df.shape, df.columns, df.dtypes
        3. Exibir: df.head(), df.describe()
        4. Exibir: df.isnull().sum()  (valores faltantes)
        5. Exibir: distribuição da coluna alvo (churn)

    Dica: Use esta função em um notebook para explorar visualmente.
    """
    pass


def mapear_colunas(df: pd.DataFrame) -> dict:
    """
    Mapeia as colunas do dataset Kaggle para o schema do projeto.

    TODO: Implementar o mapeamento de colunas.
    Cada dataset terá colunas diferentes — adapte conforme necessário.

    Exemplo para o dataset 'E-Commerce Customer Churn':
        mapeamento = {
            'CustomerID': 'id',
            'Churn': 'is_churned',
            'Tenure': 'days_as_client',
            'CityTier': 'city',
            'Gender': 'gender',
            ...
        }

    Returns:
        Dicionário com o mapeamento {coluna_kaggle: coluna_projeto}
    """
    pass


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e pré-processa os dados do Kaggle.

    TODO: Implementar a limpeza:
        1. Renomear colunas conforme mapeamento
        2. Tratar valores nulos (preencher ou remover)
        3. Converter tipos de dados (ex: string → float)
        4. Remover duplicatas
        5. Tratar outliers se necessário
        6. Garantir que is_churned é booleano (0/1)

    Returns:
        DataFrame limpo e pronto para inserção.
    """
    pass


def resetar_banco():
    """
    Reseta o banco de dados (drop all + create all).

    TODO: Implementar o reset:
        1. Obter a engine
        2. Base.metadata.drop_all(engine)  — apaga todas as tabelas
        3. Base.metadata.create_all(engine) — recria as tabelas vazias
        4. Printar confirmação

    ⚠️ CUIDADO: Isso apaga TODOS os dados existentes!
    """
    pass


def importar_clientes(df: pd.DataFrame):
    """
    Insere os dados de clientes do Kaggle no banco.

    TODO: Implementar a inserção:
        1. Criar objetos Client a partir das linhas do DataFrame
        2. Inserir via session.add_all()
        3. Commit e close

    Dica: Nem todo dataset terá todos os campos da tabela Client.
    Preencha os campos faltantes com valores default ou derivados.
    """
    pass


def importar_dataset(filepath: str):
    """
    Pipeline completo de importação de um dataset Kaggle.

    TODO: Orquestrar o pipeline:
        1. explorar_dataset(filepath)
        2. df = pd.read_csv(filepath)
        3. df = limpar_dados(df)
        4. resetar_banco()
        5. importar_clientes(df)
        6. (Opcional) importar dados em outras tabelas se disponíveis
        7. Verificar contagens finais no banco

    Exemplo de uso:
        python -m src.data_generation.import_kaggle
    """
    pass


if __name__ == "__main__":
    # Ajuste o nome do arquivo conforme o dataset que você baixou
    csv_path = os.path.join(RAW_DATA_DIR, "E Commerce Dataset.csv")

    if not os.path.exists(csv_path):
        print(f"❌ Arquivo não encontrado: {csv_path}")
        print(f"   Baixe o dataset do Kaggle e salve em: {RAW_DATA_DIR}")
    else:
        print(f"📊 Importando dataset: {csv_path}")
        importar_dataset(csv_path)
