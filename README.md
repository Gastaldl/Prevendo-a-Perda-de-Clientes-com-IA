# 🔄 Previsão de Churn de Clientes de E-commerce

Projeto end-to-end de Data Science para prever o churn (cancelamento) de clientes de um e-commerce fictício, utilizando **Python**, **SQL**, **Rede Neural** e **Power BI**.

## 🎯 Objetivo

Construir um pipeline completo que vai desde a criação do banco de dados com dados sintéticos até um dashboard interativo no Power BI, passando por engenharia de features em SQL e modelagem com rede neural.

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| **Python 3.11+** | Geração de dados, pré-processamento, modelagem |
| **SQLite** | Banco de dados relacional |
| **SQLAlchemy** | ORM para interação Python ↔ SQL |
| **Faker** | Geração de dados sintéticos |
| **Pandas / NumPy** | Manipulação e análise de dados |
| **PyTorch** | Construção da rede neural |
| **scikit-learn** | Métricas de avaliação e pré-processamento |
| **Matplotlib / Seaborn** | Visualizações exploratórias |
| **Power BI** | Dashboard final |

## 📁 Estrutura do Projeto

```
├── data/                        # Banco de dados SQLite
├── notebooks/                   # Notebooks exploratórios
├── sql/                         # Scripts SQL
│   ├── 01_schema.sql
│   ├── 02_feature_engineering.sql
│   └── 03_queries_analiticas.sql
├── src/                         # Código-fonte Python
│   ├── __init__.py
│   ├── data_generation/         # Fase 1: Geração de dados sintéticos
│   ├── database/                # Conexão e modelos do banco
│   ├── features/                # Extração de features
│   ├── model/                   # Rede neural e treinamento
│   └── export/                  # Exportação de resultados
├── powerbi/                     # Arquivos do Power BI
├── tests/                       # Testes unitários
├── docs/                        # Documentação adicional
│   └── guia_projeto.md          # Guia detalhado do projeto
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Como Executar

```bash
# 1. Criar ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar as fases do projeto
python -m src.data_generation.generate    # Fase 1: Criar banco e popular dados
python -m src.features.extract            # Fase 1: Extrair features via SQL
python -m src.model.train                 # Fase 2: Treinar rede neural
python -m src.export.save_predictions     # Fase 3: Salvar previsões no banco
```

## 📊 Fases do Projeto

1. **Banco de Dados (SQL)** — Modelagem, dados sintéticos e feature engineering
2. **Preparação e Modelagem (Python + Rede Neural)** — Pré-processamento e classificação
3. **Exportação de Resultados (Python → SQL)** — Persistência de previsões e métricas
4. **Dashboard (Power BI)** — Visualização e análise interativa

## 📝 Licença

Projeto educacional para prática de habilidades em Data Science.
