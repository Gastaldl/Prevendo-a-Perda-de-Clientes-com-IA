"""
Geração de dados sintéticos para o e-commerce.

Utiliza a biblioteca Faker para criar dados realistas de clientes,
produtos, pedidos e interações com suporte.
"""
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("pt_BR")

# Configurações de geração
NUM_CLIENTES = 2000
NUM_PRODUTOS = 100
MAX_PEDIDOS_POR_CLIENTE = 15
TAXA_CHURN = 0.25  # 25% dos clientes serão churned


def gerar_clientes(num: int = NUM_CLIENTES) -> list[dict]:
    """
    Gera uma lista de dicionários representando clientes.

    TODO: Implementar a geração de clientes usando Faker.
    Dicas:
        - Use fake.name(), fake.email(), fake.phone_number()
        - Use fake.date_between(start_date="-3y", end_date="-6m") para data_cadastro
        - Use fake.city(), fake.state_abbr()
        - Atribua is_churned=True para ~25% dos clientes
        - Clientes churned devem ter padrões diferentes:
            * Menos pedidos recentes
            * Mais interações de reclamação
            * Maior tempo desde o último pedido

    Returns:
        Lista de dicionários com dados dos clientes.
    """
    pass


def gerar_produtos(num: int = NUM_PRODUTOS) -> list[dict]:
    """
    Gera uma lista de dicionários representando produtos.

    TODO: Implementar a geração de produtos.
    Dicas:
        - Categorias sugeridas: ["Eletrônicos", "Moda", "Casa", "Esportes",
          "Livros", "Beleza", "Alimentos", "Brinquedos"]
        - Preços entre R$10 e R$2000 dependendo da categoria
        - Use fake.sentence() para descrição

    Returns:
        Lista de dicionários com dados dos produtos.
    """
    pass


def gerar_pedidos(clientes: list, produtos: list) -> tuple[list[dict], list[dict]]:
    """
    Gera pedidos e itens de pedido para os clientes.

    TODO: Implementar a geração de pedidos.
    Dicas:
        - Clientes NÃO churned: 3-15 pedidos, distribuídos ao longo do tempo
        - Clientes churned: 1-5 pedidos, concentrados no início do período
        - Status possíveis: ["entregue", "cancelado", "devolvido"]
        - Clientes churned têm mais cancelamentos/devoluções
        - Métodos de pagamento: ["cartão", "boleto", "pix"]

    Returns:
        Tupla (lista_pedidos, lista_itens_pedido)
    """
    pass


def gerar_interacoes_suporte(clientes: list) -> list[dict]:
    """
    Gera interações de suporte para os clientes.

    TODO: Implementar a geração de interações.
    Dicas:
        - Tipos: ["reclamação", "dúvida", "elogio", "troca", "cancelamento"]
        - Canais: ["chat", "email", "telefone"]
        - Clientes churned devem ter MAIS reclamações e MENOS elogios
        - Clientes churned: mais interações não resolvidas

    Returns:
        Lista de dicionários com dados das interações.
    """
    pass


def popular_banco():
    """
    Orquestra a geração de todos os dados e insere no banco.

    TODO: Implementar o pipeline completo:
        1. Chamar init_db() para criar as tabelas
        2. Gerar clientes, produtos, pedidos e interações
        3. Inserir tudo no banco usando sessions do SQLAlchemy
        4. Printar estatísticas (total de registros, taxa de churn real, etc.)
    """
    pass


if __name__ == "__main__":
    popular_banco()
