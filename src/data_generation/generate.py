"""
Geração de dados sintéticos para o e-commerce.

Utiliza a biblioteca Faker para criar dados realistas de clientes,
produtos, pedidos e interações com suporte.
"""
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("en_US")

# Configurações de geração
NUM_CLIENTS = 2000
NUM_PRODUCTS = 100
MAX_ORDERS_PER_CLIENT = 15
CHURN_RATE = 0.25  # 25% dos clientes serão churned


def generate_clients(num: int = NUM_CLIENTS) -> list[dict]:
    """
    Gera uma lista de dicionários representando clientes.

    TODO: Implementar a geração de clientes usando Faker.
    Dicas:
        - Use fake.name(), fake.email(), fake.phone_number()
        - Use fake.date_between(start_date="-3y", end_date="-6m") para registration_date
        - Use fake.city(), fake.state_abbr()
        - Atribua is_churned=True para ~25% dos clientes
        - Clientes churned devem ter padrões diferentes:
            * Menos pedidos recentes
            * Mais interações de complaint
            * Maior tempo desde o último pedido

    Returns:
        Lista de dicionários com dados dos clientes.
    """



def generate_products(num: int = NUM_PRODUCTS) -> list[dict]:
    """
    Gera uma lista de dicionários representando produtos.

    TODO: Implementar a geração de produtos.
    Dicas:
        - Categorias sugeridas: ["Eletrônicos", "Moda", "Casa", "Esportes",
          "Livros", "Beleza", "Alimentos", "Brinquedos"]
        - Preços entre R$10 e R$2000 dependendo da category
        - Use fake.sentence() para description

    Returns:
        Lista de dicionários com dados dos produtos.
    """
    pass


def generate_orders(clients: list, products: list) -> tuple[list[dict], list[dict]]:
    """
    Gera pedidos e itens de pedido para os clientes.

    TODO: Implementar a geração de pedidos.
    Dicas:
        - Clientes NÃO churned: 3-15 pedidos, distribuídos ao longo do tempo
        - Clientes churned: 1-5 pedidos, concentrados no início do período
        - Status possíveis: ["delivered", "cancelled", "returned"]
        - Clientes churned têm mais cancelamentos/devoluções
        - Métodos de pagamento: ["credit_card", "boleto", "pix"]

    Returns:
        Tupla (orders_list, order_items_list)
    """
    pass


def generate_support_interactions(clients: list) -> list[dict]:
    """
    Gera interações de suporte para os clientes.

    TODO: Implementar a geração de interações.
    Dicas:
        - Tipos: ["complaint", "question", "praise", "exchange", "cancellation"]
        - Canais: ["chat", "email", "phone"]
        - Clientes churned devem ter MAIS complaints e MENOS praises
        - Clientes churned: mais interações não resolvidas (resolved=False)

    Returns:
        Lista de dicionários com dados das interações.
    """
    pass


def populate_database():
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
    populate_database()
