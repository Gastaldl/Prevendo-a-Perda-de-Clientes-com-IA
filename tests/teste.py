from src.data_generation.generate import generate_clients

clients = generate_clients(5)  # gera só 5 para testar
for c in clients:
    print(f"{c['name']} — Churned: {c['is_churned']}")