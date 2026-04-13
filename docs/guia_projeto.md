# 📘 Guia Completo — Previsão de Churn de Clientes de E-commerce

Este guia vai te acompanhar em cada fase do projeto. Cada seção tem **o que fazer**, **como fazer**, **conceitos-chave** e **critérios de conclusão** para que você saiba exatamente quando avançar para a próxima fase.

---

## 🔀 Estratégia de Dados: Faker primeiro, Kaggle depois

Este projeto usa uma abordagem em **duas rodadas**:

| Rodada | Fonte de Dados | Objetivo |
|---|---|---|
| **1ª Rodada** (Fases 1-4) | 🏭 **Faker** (dados sintéticos) | Construir e validar todo o pipeline. Você controla os dados, então se algo der errado, o problema está no código — não nos dados. Além disso, a geração com Faker é ótima prática de Python. |
| **2ª Rodada** (Fase 5) | 📊 **Kaggle** (dados reais) | Trocar a fonte de dados por um dataset real, sem mudar o restante do pipeline. O modelo enfrenta um desafio real, e o portfólio fica muito mais forte. |

**Por que essa ordem?**
- Com Faker você pratica **mais Python** (lógica de geração, seed, distribuições)
- Você tem **controle total** sobre os padrões de churn
- Quando trocar para dados reais, o pipeline já está validado — só muda a entrada
- No portfólio, você mostra que trabalhou **com dados reais**

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.11+** → [python.org](https://www.python.org/downloads/)
- **Power BI Desktop** → [powerbi.microsoft.com](https://powerbi.microsoft.com/desktop/)
- **Git** → [git-scm.com](https://git-scm.com/)
- Um editor de código (VS Code recomendado)

### Setup Inicial

```bash
# 1. Navegue até o projeto
cd "Previsão de Churn de Clientes de E-commerce"

# 2. Crie o ambiente virtual
python -m venv .venv

# 3. Ative o ambiente virtual (Windows)
.venv\Scripts\activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Inicialize o repositório Git
git init
git add .
git commit -m "chore: setup inicial do projeto"
```

---

## 🗂️ Mapa de Arquivos do Projeto

```
├── data/
│   ├── ecommerce_churn.db           ← Banco SQLite (gerado na Fase 1)
│   └── raw/                         ← Datasets Kaggle baixados (Fase 5)
├── sql/
│   ├── 01_schema.sql                ← Referência do schema
│   ├── 02_feature_engineering.sql   ← Queries de features (praticar aqui)
│   └── 03_queries_analiticas.sql    ← Queries para Power BI
├── src/
│   ├── database/
│   │   ├── connection.py            ← Conexão SQLAlchemy (Fase 1)
│   │   └── models.py               ← Modelos ORM (Fase 1)
│   ├── data_generation/
│   │   ├── generate.py              ← 🏭 Dados sintéticos com Faker (Fase 1)
│   │   └── import_kaggle.py         ← 📊 Importação de dados reais (Fase 5)
│   ├── features/
│   │   └── extract.py               ← Extração de features (Fase 1→2)
│   ├── model/
│   │   └── train.py                 ← Rede neural PyTorch (Fase 2)
│   └── export/
│       └── save_predictions.py      ← Exportação para o banco (Fase 3)
├── notebooks/                       ← Jupyter notebooks exploratórios
├── powerbi/                         ← Arquivos .pbix (Fase 4)
└── tests/                           ← Testes unitários
```

> Todos os arquivos `.py` já contêm **esqueletos com TODOs** — sua tarefa é implementar cada `TODO`.

---

# 🔷 FASE 1 — Banco de Dados com Dados Sintéticos (SQL + Faker)

**Objetivo:** Criar o banco de dados relacional, popular com dados sintéticos via Faker e praticar queries SQL. Os dados sintéticos servem para **construir e validar o pipeline** antes de usar dados reais.

**Tecnologias:** SQLite, SQLAlchemy, Faker, SQL puro

**Tempo estimado:** 3-5 dias

---

### Etapa 1.1 — Conexão com o Banco (`src/database/connection.py`)

**O que fazer:**
Implementar as funções `get_engine()`, `get_session()` e `init_db()`.

**Conceitos-chave:**
- **Engine:** Ponto central de conexão do SQLAlchemy com o banco
- **Session:** Gerencia transações (insert, update, delete)
- **`echo=True`:** Mostra as queries SQL geradas no console (útil para aprender)

**Exemplo de referência:**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///data/ecommerce_churn.db", echo=True)
Session = sessionmaker(bind=engine)
```

**Critério de conclusão:** ✅ Conseguir criar uma engine e uma session sem erros.

---

### Etapa 1.2 — Modelos ORM (`src/database/models.py`)

**O que fazer:**
Transformar cada `TODO` em colunas SQLAlchemy reais. O arquivo já tem todos os campos documentados.

**Conceitos-chave:**
- **ORM (Object Relational Mapping):** Cada classe Python = uma tabela SQL
- **`Column()`:** Define uma coluna com tipo, constraints, e default
- **`relationship()`:** Define relações entre tabelas (1:N, N:M)
- **`ForeignKey()`:** Referência entre tabelas

**Exemplo de referência (para a tabela Client):**
```python
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    # ... demais colunas

    orders = relationship("Order", back_populates="client")
```

**Dica:** Consulte o arquivo `sql/01_schema.sql` para ver o schema completo como referência.

**Critério de conclusão:** ✅ Rodar `init_db()` sem erros e verificar que as tabelas foram criadas no banco.

**Verificação:**
```python
import sqlite3
conn = sqlite3.connect("data/ecommerce_churn.db")
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
print([row[0] for row in cursor.fetchall()])
# Deve mostrar: ['clients', 'products', 'orders', 'order_items', 'support_interactions', ...]
```

---

### Etapa 1.3 — Dados Sintéticos (`src/data_generation/generate.py`)

**O que fazer:**
Implementar as funções de geração usando Faker e inserir no banco.

**Conceitos-chave:**
- **Faker:** Biblioteca que gera dados falsos realistas (nomes, emails, datas...)
- **Seed:** Use `Faker.seed(42)` e `random.seed(42)` para dados reproduzíveis
- **Distribuição de Churn:** Clientes churned devem ter padrões notavelmente diferentes

**⚠️ Regra de ouro para os dados sintéticos:**
Os dados precisam **refletir padrões reais de churn**. Sem isso, o modelo não vai aprender nada. Garanta que clientes churned tenham:
- Menos pedidos recentes (últimos 90 dias)
- Mais tempo desde o último pedido
- Mais interações de reclamação e menos de elogio
- Mais cancelamentos/devoluções
- Menor ticket médio recente

**Volumes recomendados:**
| Tabela | Quantidade |
|---|---|
| Clientes | 2.000 |
| Produtos | 100 |
| Pedidos | ~10.000-15.000 |
| Itens de Pedido | ~20.000-30.000 |
| Interações Suporte | ~3.000-5.000 |

**Critério de conclusão:** ✅ Banco populado com dados, e uma verificação rápida mostra que ~25% dos clientes são churned.

---

### Etapa 1.4 — Queries SQL (`sql/02_feature_engineering.sql`)

**O que fazer:**
Praticar as queries SQL diretamente no banco. O arquivo tem queries progressivas do básico ao avançado.

**Ordem recomendada de estudo:**
1. **JOINs + GROUP BY** — Agregar pedidos por cliente
2. **Funções de data** — `julianday()`, `strftime()`
3. **CASE WHEN** — Cálculos condicionais
4. **Subqueries** — Queries dentro de queries
5. **CTEs (WITH)** — Queries nomeadas reutilizáveis
6. **Window Functions** — `RANK()`, `ROW_NUMBER()`, `LAG()`, `NTILE()`

**Dica prática:** Use uma ferramenta SQL como **DB Browser for SQLite** (grátis) para testar queries visualmente antes de levá-las ao Python.

**Critério de conclusão:** ✅ Conseguir executar a query consolidada final (seção 8 do arquivo) e obter um resultado com 1 linha por cliente e todas as features.

---

# 🔷 FASE 2 — Preparação e Modelagem (Python + Rede Neural)

**Objetivo:** Extrair features do banco, pré-processar os dados e treinar uma rede neural.

**Tecnologias:** Pandas, scikit-learn, PyTorch

**Tempo estimado:** 4-7 dias

---

### Etapa 2.1 — Extração de Features (`src/features/extract.py`)

**O que fazer:**
Implementar `extrair_features()` que executa a query SQL consolidada da Fase 1 e retorna um DataFrame.

**Conceitos-chave:**
- **`pd.read_sql()`:** Executa SQL e retorna DataFrame diretamente
- **Features devem ser numéricas:** O modelo só aceita números

**Exemplo:**
```python
import pandas as pd
from src.database.connection import get_engine

engine = get_engine()
df = pd.read_sql("SELECT * FROM clients LIMIT 5", engine)
print(df.head())
```

**Critério de conclusão:** ✅ DataFrame com ~2000 linhas, ~12-15 colunas de features, e sem colunas de texto (exceto identificadores).

---

### Etapa 2.2 — Pré-processamento (`src/features/extract.py` → `preparar_dados()`)

**O que fazer:**
Limpar, normalizar e dividir os dados para treinamento.

**Pipeline de pré-processamento:**
```
DataFrame bruto
    ↓
1. Tratar nulos (fillna com 0 ou mediana)
    ↓
2. Remover colunas desnecessárias (id, nome, email)
    ↓
3. Separar X (features) e y (is_churned)
    ↓
4. Normalizar com StandardScaler
    ↓
5. Train/Test split (80/20)
    ↓
6. Converter para tensores PyTorch
```

**Conceitos-chave:**
- **StandardScaler:** Normaliza cada feature para média=0 e std=1
- **Train/Test Split:** Nunca treinar e avaliar no mesmo dado
- **Desbalanceamento:** Se 75% dos dados são "não churn", o modelo pode simplesmente prever "não churn" sempre e ter 75% de acurácia. Soluções: class_weight, oversampling (SMOTE), ou undersampling.

**Critério de conclusão:** ✅ X_train, X_test, y_train, y_test criados como tensores PyTorch com shapes corretos.

---

### Etapa 2.3 — Rede Neural (`src/model/train.py`)

**O que fazer:**
Implementar a classe `ChurnNet` e a função `treinar_modelo()`.

**Arquitetura sugerida (comece aqui):**
```
Input (N features)
    ↓
Linear(N → 64) → ReLU → Dropout(0.3)
    ↓
Linear(64 → 32) → ReLU → Dropout(0.2)
    ↓
Linear(32 → 16) → ReLU
    ↓
Linear(16 → 1) → Sigmoid
    ↓
Output (probabilidade de churn: 0 a 1)
```

**Loop de treinamento — estrutura base:**
```python
model = ChurnNet(input_dim=num_features)
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    model.train()
    for X_batch, y_batch in train_loader:
        # Forward
        y_pred = model(X_batch)
        loss = criterion(y_pred.squeeze(), y_batch)

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Avaliação periódica
    if epoch % 10 == 0:
        model.eval()
        with torch.no_grad():
            val_pred = model(X_val)
            val_loss = criterion(val_pred.squeeze(), y_val)
        print(f"Epoch {epoch}: Train Loss={loss:.4f}, Val Loss={val_loss:.4f}")
```

**Conceitos-chave:**
- **BCELoss:** Binary Cross Entropy, ideal para classificação binária
- **Adam:** Optimizer adaptativo, bom default
- **Dropout:** Desliga neurônios aleatoriamente durante treino (regularização)
- **Overfitting:** Quando o modelo decora os dados de treino mas não generaliza

**Métricas para acompanhar:**
| Métrica | O que mede | Ideal |
|---|---|---|
| Acurácia | % de acertos totais | > 80% |
| Precision | Dos que o modelo disse "churn", quantos realmente eram | > 70% |
| Recall | Dos que realmente eram churn, quantos o modelo pegou | > 70% |
| F1-Score | Harmonia entre precision e recall | > 70% |
| AUC-ROC | Capacidade de separar as classes | > 0.80 |

**⚠️ Atenção:** Para churn, **Recall é mais importante que Precision**. É pior perder um cliente churned (falso negativo) do que enviar uma promoção de retenção para um cliente ativo (falso positivo).

**Critério de conclusão:** ✅ Modelo treinado com F1-Score > 0.65 no conjunto de teste. Métricas registradas.

---

### Etapa 2.4 — Experimentação (Opcional mas recomendado)

**O que fazer:**
Testar variações e comparar resultados.

**Experimentos sugeridos:**
1. Variar o número de camadas (2 vs 3 vs 4)
2. Variar learning rate (0.01, 0.001, 0.0001)
3. Adicionar BatchNormalization
4. Testar com/sem Dropout
5. Aumentar/reduzir neurônios por camada
6. Usar class_weight para lidar com desbalanceamento

**Dica:** Crie um notebook em `notebooks/` para exploração visual dos experimentos.

---

# 🔷 FASE 3 — Exportação de Resultados (Python → SQL)

**Objetivo:** Salvar previsões e métricas de volta no banco de dados.

**Tecnologias:** SQLAlchemy, Python

**Tempo estimado:** 1-2 dias

---

### Etapa 3.1 — Salvar Previsões (`src/export/save_predictions.py`)

**O que fazer:**
Implementar `salvar_previsoes()` para inserir as probabilidades de churn de cada cliente no banco.

**Conceitos-chave:**
- **Versionamento:** Cada rodada de previsões tem uma `versao_modelo`
- **Threshold:** Probabilidade acima de 0.5 (ou outro valor) = previsão de churn
- **Idempotência:** Se rodar 2 vezes, delete os resultados antigos antes

**Exemplo de fluxo:**
```python
Session = get_session()
session = Session()

# Deletar previsões antigas desta versão
session.query(ChurnPrediction).filter_by(model_version="v1.0").delete()

# Inserir novas previsões
previsoes = []
for cid, prob in zip(cliente_ids, probabilidades):
    previsoes.append(ChurnPrediction(
        client_id=cid,
        churn_probability=prob,
        prediction=prob > 0.5,
        prediction_date=datetime.now(),
        model_version="v1.0"
    ))

session.add_all(previsoes)
session.commit()
session.close()
```

**Critério de conclusão:** ✅ Tabela `churn_predictions` populada com 2000 registros (1 por cliente).

---

### Etapa 3.2 — Salvar Histórico de Treinamento

**O que fazer:**
Implementar `salvar_historico_treinamento()` para registrar as métricas de cada treinamento.

**Critério de conclusão:** ✅ Tabela `training_history` com pelo menos 1 registro contendo todas as métricas.

---

# 🔷 FASE 4 — Dashboard (Power BI)

**Objetivo:** Criar um dashboard interativo conectado ao banco de dados.

**Tecnologias:** Power BI Desktop, DAX

**Tempo estimado:** 3-5 dias

---

### Etapa 4.1 — Conectar ao Banco

**Como conectar Power BI ao SQLite:**

O Power BI não tem conector nativo para SQLite. Existem duas opções:

**Opção A — Conector ODBC (recomendado):**
1. Instale o driver ODBC para SQLite: [sqliteodbc.org](http://www.ch-werner.de/sqliteodbc/)
2. No Power BI: Obter Dados → ODBC → Configurar DSN apontando para o `.db`

**Opção B — Exportar para CSV (mais simples):**
1. No Python, exporte os DataFrames relevantes para CSV:
```python
import pandas as pd
from src.database.connection import get_engine

engine = get_engine()

# Exportar tabelas
pd.read_sql("SELECT * FROM clients", engine).to_csv("data/clients.csv", index=False)
pd.read_sql("SELECT * FROM churn_predictions", engine).to_csv("data/predictions.csv", index=False)
# ... etc
```
2. No Power BI: Obter Dados → CSV

**Opção C — Converter para Excel:**
```python
with pd.ExcelWriter("data/dados_ecommerce.xlsx") as writer:
    pd.read_sql("SELECT * FROM clients", engine).to_excel(writer, sheet_name="Clients")
    pd.read_sql("SELECT * FROM orders", engine).to_excel(writer, sheet_name="Orders")
    # ... etc
```

---

### Etapa 4.2 — Modelagem de Dados no Power BI

**Relacionamentos a configurar:**
```
clients  (1) ──→ (N) orders                [via client_id]
clients  (1) ──→ (N) support_interactions   [via client_id]
clients  (1) ──→ (N) churn_predictions     [via client_id]
orders   (1) ──→ (N) order_items           [via order_id]
products (1) ──→ (N) order_items           [via product_id]
```

---

### Etapa 4.3 — Medidas DAX

**Medidas sugeridas para praticar:**

```dax
// Total de Clientes
Total Clientes = COUNTROWS(clients)

// Taxa de Churn
Taxa Churn = 
DIVIDE(
    COUNTROWS(FILTER(clients, clients[is_churned] = TRUE())),
    COUNTROWS(clients)
)

// Receita Total
Receita Total = SUM(orders[total_value])

// Ticket Médio
Ticket Médio = AVERAGE(orders[total_value])

// Clientes em Risco (prob > 70%)
Clientes Alto Risco = 
COUNTROWS(
    FILTER(churn_predictions, churn_predictions[churn_probability] > 0.7)
)

// Receita em Risco
Receita em Risco = 
CALCULATE(
    SUM(orders[total_value]),
    FILTER(
        clients,
        RELATED(churn_predictions[churn_probability]) > 0.7
    )
)

// Média de Interações
Media Interacoes = 
DIVIDE(
    COUNTROWS(support_interactions),
    COUNTROWS(clients)
)
```

---

### Etapa 4.4 — Páginas do Dashboard

Crie **4 páginas** no seu dashboard:

#### Página 1: 📊 Visão Geral do E-commerce
- **Cards:** Total de clientes, Receita total, Ticket médio, Pedidos totais
- **Gráfico de linha:** Receita mensal ao longo do tempo
- **Gráfico de barras:** Top categorias por receita
- **Mapa:** Distribuição geográfica de clientes por estado
- **Filtros:** Período, Estado, Categoria

#### Página 2: 🔴 Análise de Churn
- **Gauge:** Taxa de churn atual
- **Gráfico de barras empilhadas:** Churned vs Ativo por segmento
- **Gráfico de dispersão:** Ticket médio vs Dias desde último pedido (cor = churn)
- **Tabela:** Comparativo de métricas (ativo vs churned)
- **Filtros:** Gênero, Estado, Período de cadastro

#### Página 3: 🤖 Previsões do Modelo
- **Histograma:** Distribuição das probabilidades de churn
- **Cards:** Total alto risco, médio risco, baixo risco
- **Gráfico de barras:** Receita em risco por faixa de probabilidade
- **Tabela detalhada:** Top 20 clientes com maior risco (nome, email, prob, gasto)
- **Filtros:** Versão do modelo, Faixa de risco

#### Página 4: 📈 Performance do Modelo
- **Gráfico de linhas:** Evolução de Acurácia, Precision, Recall e F1 ao longo das versões
- **Card:** AUC-ROC atual
- **Tabela:** Detalhes de cada treinamento (arquitetura, hiperparâmetros, métricas)

---

### Etapa 4.5 — Formatação e Polish

**Dicas de design:**
- Use um tema escuro ou corporativo consistente
- Mantenha uma paleta de cores limitada (3-4 cores)
- Use ícones nos cards para destaque visual
- Adicione tooltips personalizados
- Configure a navegação entre páginas com botões
- Use bookmarks para cenários pré-configurados

**Critério de conclusão:** ✅ Dashboard funcional com 4 páginas, filtros interativos e medidas DAX customizadas.

---

# 🔷 FASE 5 — Migração para Dados Reais (Kaggle)

**Objetivo:** Substituir os dados sintéticos por um dataset real do Kaggle, re-treinar o modelo e atualizar o dashboard. Isso valida que seu pipeline é robusto e deixa seu portfólio mais forte.

**Tecnologias:** Pandas, SQLAlchemy, Kaggle

**Tempo estimado:** 2-3 dias

---

### Etapa 5.1 — Escolher e Baixar o Dataset

**Datasets recomendados:**

| Dataset | Link | Observações |
|---|---|---|
| **E-Commerce Customer Churn** | [Kaggle](https://www.kaggle.com/datasets/ankitverma2010/ecommerce-customer-churn-analysis-and-prediction) | Encaixa perfeitamente no tema do projeto |
| **Telco Customer Churn** | [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) | Clássico, muito usado em portfólios |

**O que fazer:**
1. Baixe o CSV do Kaggle
2. Salve em `data/raw/` (esta pasta está no `.gitignore`)
3. Explore o dataset em um notebook (`notebooks/exploracao_kaggle.ipynb`)

**Critério de conclusão:** ✅ Dataset baixado e explorado. Você entende as colunas, os tipos de dados e a distribuição de churn.

---

### Etapa 5.2 — Mapear e Importar (`src/data_generation/import_kaggle.py`)

**O que fazer:**
Implementar o script que lê o CSV do Kaggle e insere os dados nas suas tabelas SQL existentes.

**Conceitos-chave:**
- **Mapeamento de colunas:** O dataset do Kaggle terá colunas com nomes e formatos diferentes das suas tabelas. Você precisa fazer o "de-para"
- **Limpeza:** Dados reais vêm sujos — valores faltantes, formatos inconsistentes, outliers
- **Adaptação do schema:** Pode ser que o Kaggle tenha colunas extras ou faltem algumas. Adapte os modelos ORM se necessário

**Pipeline de importação:**
```
CSV Kaggle (data/raw/)
    ↓
1. Ler com pd.read_csv()
    ↓
2. Explorar: df.info(), df.describe(), df.isnull().sum()
    ↓
3. Mapear colunas do Kaggle → suas tabelas
    ↓
4. Limpar: tratar nulos, converter tipos, remover duplicatas
    ↓
5. Resetar banco: drop_all() + create_all()
    ↓
6. Inserir via SQLAlchemy (session.add_all)
    ↓
7. Verificar: SELECT COUNT(*) de cada tabela
```

**Dica importante:** Nem todo dataset do Kaggle terá o mesmo nível de detalhe das suas tabelas Faker. Por exemplo, o dataset pode não ter tabela de `produtos` separada. Nesse caso, simplifique seus modelos ou preencha o que faltar com dados derivados.

**Critério de conclusão:** ✅ Banco populado com dados reais. Queries da Fase 1 funcionam sem alteração (ou com ajustes mínimos).

---

### Etapa 5.3 — Re-treinar o Modelo

**O que fazer:**
1. Rodar o pipeline de extração de features (`src/features/extract.py`) — a query SQL deve funcionar sem mudanças
2. Rodar o pré-processamento — atenção a features que possam não existir mais
3. Re-treinar a rede neural — salve como `v2.0`
4. Comparar métricas: Faker (v1.0) vs Kaggle (v2.0)

**⚠️ Expectativa realista:**
O modelo treinado com dados reais provavelmente terá **métricas inferiores** às do Faker. Isso é normal! Dados sintéticos têm padrões perfeitos e fáceis de aprender. Dados reais são ruidosos e desafiadores — e é exatamente por isso que são mais valiosos para aprendizado.

**O que comparar:**
| Métrica | Faker (v1.0) | Kaggle (v2.0) |
|---|---|---|
| Acurácia | ~ | ~ |
| Precision | ~ | ~ |
| Recall | ~ | ~ |
| F1-Score | ~ | ~ |
| AUC-ROC | ~ | ~ |

**Critério de conclusão:** ✅ Modelo v2.0 treinado com dados reais. Métricas registradas no `historico_treinamento`.

---

### Etapa 5.4 — Atualizar o Dashboard

**O que fazer:**
1. Refresh dos dados no Power BI
2. Verificar se os visuais ainda fazem sentido com os dados reais
3. Na página de Performance do Modelo, agora você terá **duas versões** para comparar (v1.0 Faker vs v2.0 Kaggle)
4. Ajustar filtros e medidas DAX se necessário

**Critério de conclusão:** ✅ Dashboard atualizado com dados reais e comparação entre versões do modelo.

---

# 🎯 Checklist Final

Use este checklist para garantir que você praticou tudo:

### SQL
- [ ] Criou o banco de dados com schema correto
- [ ] Escreveu queries com JOINs (INNER, LEFT)
- [ ] Usou GROUP BY com funções de agregação (COUNT, SUM, AVG)
- [ ] Usou CASE WHEN para cálculos condicionais
- [ ] Usou subqueries e CTEs (WITH)
- [ ] Usou Window Functions (RANK, ROW_NUMBER, LAG)
- [ ] Fez INSERT/UPDATE via Python

### Python
- [ ] Gerou dados sintéticos com Faker
- [ ] Importou e limpou dados reais do Kaggle
- [ ] Conectou ao banco via SQLAlchemy
- [ ] Manipulou DataFrames com Pandas
- [ ] Fez pré-processamento (nulos, normalização, encoding)
- [ ] Fez train/test split
- [ ] Usou scikit-learn para métricas

### Rede Neural
- [ ] Definiu a arquitetura com `nn.Module`
- [ ] Implementou o loop de treinamento
- [ ] Usou BCELoss e Adam optimizer
- [ ] Aplicou Dropout para regularização
- [ ] Avaliou com múltiplas métricas (Acc, Precision, Recall, F1, AUC)
- [ ] Experimentou diferentes hiperparâmetros
- [ ] Comparou performance entre dados sintéticos e reais

### Power BI
- [ ] Conectou ao banco de dados / importou dados
- [ ] Configurou relacionamentos entre tabelas
- [ ] Criou medidas DAX customizadas
- [ ] Construiu 4 páginas de dashboard
- [ ] Aplicou filtros interativos
- [ ] Formatou com design profissional
- [ ] Atualizou dashboard com dados reais do Kaggle

---

# 💡 Dicas Gerais

1. **Commite frequentemente** — Faça commits no Git ao final de cada etapa
2. **Documente suas decisões** — Adicione comentários explicando o "porquê" do código
3. **Notebook para exploração** — Use `notebooks/` para testes rápidos e visualizações
4. **Não busque perfeição** — Faça funcionar primeiro, depois otimize
5. **Debug com prints** — Use `print()` e `df.head()` liberalmente
6. **Consulte a documentação:**
   - [SQLAlchemy docs](https://docs.sqlalchemy.org/)
   - [PyTorch tutorials](https://pytorch.org/tutorials/)
   - [Faker docs](https://faker.readthedocs.io/)
   - [Power BI docs](https://learn.microsoft.com/power-bi/)

---

> **Boa sorte e bom aprendizado!** 🚀
> Cada fase desse projeto vai te dar experiência prática real. Quando terminar, você vai ter um projeto completo para colocar no portfólio.
