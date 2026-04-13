"""
Synthetic data generation for the e-commerce platform.

Uses the Faker library to create realistic data for clients,
products, orders and support interactions.
"""
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("en_US")
Faker.seed(42)
random.seed(42)

# Generation settings
NUM_CLIENTS = 2000
NUM_PRODUCTS = 100
MAX_ORDERS_PER_CLIENT = 15
CHURN_RATE = 0.25  # 25% of clients will be churned


def generate_clients(num: int = NUM_CLIENTS) -> list[dict]:
    """
    Generates a list of dictionaries representing clients.

    TODO: Implement client generation using Faker.
    Tips:
        - Use fake.name(), fake.email(), fake.phone_number()
        - Use fake.date_between(start_date="-3y", end_date="-6m") for registration_date
        - Use fake.city(), fake.state_abbr()
        - Set is_churned=True for ~25% of clients
        - Churned clients should have different patterns:
            * Fewer recent orders
            * More complaint interactions
            * Longer time since last order

    Returns:
        List of dictionaries with client data.
    """
    clients = []
        
    for i in range(num):
        is_churned = random.random() < CHURN_RATE

        client = {
            "name": fake.name(),
            "email": f"client_{i}_{fake.user_name()}@{fake.free_email_domain()}",
            "phone": fake.phone_number(),
            "registration_date": fake.date_time_between(start_date="-3y", end_date="-6m"),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "gender": random.choice(["Male", "Female"]),
            "birth_date": fake.date_of_birth(minimum_age=18,maximum_age=70),
            "is_churned": is_churned
            
        }
        clients.append(client)

    return clients


def generate_products(num: int = NUM_PRODUCTS) -> list[dict]:
    """
    Generates a list of dictionaries representing products.

    TODO: Implement product generation.
    Tips:
        - Suggested categories: ["Electronics", "Fashion", "Home", "Sports",
          "Books", "Beauty", "Food", "Toys"]
        - Prices between $10 and $2000 depending on the category
        - Use fake.sentence() for description

    Returns:
        List of dictionaries with product data.
    """
    category_prices = {
    "Electronics": (100, 2000),
    "Fashion":     (20,  300),
    "Home":        (30,  500),
    "Sports":      (15,  400),
    "Books":       (10,  80),
    "Beauty":      (10,  150),
    "Food":        (10,  100),
    "Toys":        (10,  200),
    }

    products = []

    for i in range(num):
        category = random.choice(list(category_prices.keys()))
        min_price, max_price = category_prices[category]

        product = {
            "name": fake.catch_phrase(),
            "category": category,
            "price": round(random.uniform(min_price, max_price), 2),
            "description": fake.sentence(),
            "stock": random.randint(0, 200),
        }
        products.append(product)

    return products


def generate_orders(clients: list, products: list) -> tuple[list[dict], list[dict]]:
    """
    Generates orders and order_items for clients.

    TODO: Implement order generation.
    Tips:
        - Non-churned clients: 3-15 orders, distributed over time
        - Churned clients: 1-5 orders, concentrated at the beginning of the period
        - Possible statuses: ["delivered", "cancelled", "returned"]
        - Churned clients have more cancellations/returns
        - Payment methods: ["credit_card", "boleto", "pix"]

    Returns:
        Tuple (orders_list, order_items_list)
    """
    orders = []
    order_items = []
    order_id = 1

    for client_index, client in enumerate(clients):
        is_churned = client["is_churned"]
        reg_date = client["registration_date"]
        if is_churned:
            num_orders = random.randint(1, 5)
            end_date = reg_date + timedelta(days=180)
            status_weights = [0.50, 0.30, 0.20]
        else:
            num_orders = random.randint(3, 15)
            end_date = datetime.now()
            status_weights = [0.85, 0.10, 0.05]

        statuses = ["delivered", "cancelled", "returned"]

        for i in range(num_orders):
            num_items = random.randint(1, 5)
            chosen_products = random.sample(products, min(num_items, len(products)))

            total_value = 0.0
            for product in chosen_products:
                quantity = random.randint(1, 3)
                unit_price = product["price"]
                total_value += round(unit_price * quantity, 2)

                order_items.append({
                    "order_id": order_id,
                    "product_id": products.index(product) + 1,
                    "quantity": quantity,
                    "unit_price": unit_price,
                })
            orders.append({
                "id": order_id,
                "client_id": client_index + 1,
                "order_date": fake.date_time_between(start_date=reg_date, end_date=end_date),
                "total_value": round(total_value, 2),
                "status": random.choices(statuses, weights=status_weights)[0],
                "payment_method": random.choice(["credit_card", "boleto", "pix"]),
            })
            order_id += 1

    return orders, order_items


def generate_support_interactions(clients: list) -> list[dict]:
    """
    Generates support_interactions for clients.

    TODO: Implement interaction generation.
    Tips:
        - Types: ["complaint", "question", "praise", "exchange", "cancellation"]
        - Channels: ["chat", "email", "phone"]
        - Churned clients should have MORE complaints and FEWER praises
        - Churned clients: more unresolved interactions (resolved=False)

    Returns:
        List of dictionaries with interaction data.
    """
    interactions = []

    types = ["complaint", "question", "praise", "exchange", "cancellation"]
    channels = ["chat", "email", "phone"]

    for client_index, client in enumerate(clients):
        is_churned = client["is_churned"]
        reg_date = client["registration_date"]

        if is_churned:
            num_interactions = random.randint(3, 8)
            type_weights = [0.40, 0.20, 0.05, 0.20, 0.15]  # mais complaint
            resolve_chance = 0.40                            # mais não resolvidos
        else:
            num_interactions = random.randint(0, 3)
            type_weights = [0.10, 0.35, 0.30, 0.15, 0.10]  # mais praise/question
            resolve_chance = 0.80

        for _ in range(num_interactions):
            interactions.append({
                "client_id": client_index + 1,
                "interaction_date": fake.date_time_between(
                    start_date=reg_date,
                    end_date=datetime.now()
                ),
                "type": random.choices(types, weights=type_weights)[0],
                "channel": random.choice(channels),
                "resolved": random.random() < resolve_chance,
                "description": fake.sentence(),
            })

    return interactions


def populate_database():
    """
    Orchestrates the generation of all data and inserts it into the database.

    TODO: Implement the full pipeline:
        1. Call init_db() to create the tables
        2. Generate clients, products, orders and interactions
        3. Insert everything into the database using SQLAlchemy sessions
        4. Print statistics (total records, actual churn_rate, etc.)
    """
    from src.database.connection import init_db, get_session
    from src.database.models import Client, Product, Order, OrderItem, SupportInteraction

    init_db()

    clients = generate_clients()
    products = generate_products()
    orders, order_items = generate_orders(clients, products)
    interactions = generate_support_interactions(clients)

    Session = get_session()
    session = Session()

    try:
        session.bulk_insert_mappings(Client.__mapper__, clients)
        session.bulk_insert_mappings(Product.__mapper__, products)
        session.bulk_insert_mappings(Order.__mapper__, orders)
        session.bulk_insert_mappings(OrderItem.__mapper__, order_items)
        session.bulk_insert_mappings(SupportInteraction.__mapper__, interactions)

        session.commit()

        churned_count = sum(1 for c in clients if c["is_churned"])
        print("\n=== Statistics ===")
        print(f"Clients:              {len(clients):>6}  (churned: {churned_count} — {churned_count/len(clients)*100:.1f}%)")
        print(f"Products:             {len(products):>6}")
        print(f"Orders:               {len(orders):>6}")
        print(f"Order items:          {len(order_items):>6}")
        print(f"Support interactions: {len(interactions):>6}")
        print("\nDatabase populated successfully!")

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    populate_database()
