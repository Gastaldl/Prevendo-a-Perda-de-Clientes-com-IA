"""
Definição e treinamento da rede neural para previsão de churn.

Utiliza PyTorch para construir um classificador binário com
camadas densas (fully connected).
"""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


class ChurnNet(nn.Module):
    """
    Rede neural para classificação de churn.

    TODO: Implementar a arquitetura da rede neural.

    Arquitetura sugerida (comece simples e experimente):
        - Camada 1: Linear(num_features → 64) + ReLU + Dropout(0.3)
        - Camada 2: Linear(64 → 32) + ReLU + Dropout(0.2)
        - Camada 3: Linear(32 → 16) + ReLU
        - Saída:    Linear(16 → 1) + Sigmoid

    Dicas:
        - Use nn.Sequential ou defina camadas separadas
        - Dropout ajuda a evitar overfitting
        - BatchNorm1d pode ajudar na convergência
        - Sigmoid na saída para probabilidade (0 a 1)
    """

    def __init__(self, input_dim: int):
        super().__init__()
        # TODO: Definir as camadas da rede
        pass

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # TODO: Implementar o forward pass
        pass


def treinar_modelo(
    X_train, y_train, X_val, y_val,
    epochs: int = 100,
    learning_rate: float = 0.001,
    batch_size: int = 32
) -> dict:
    """
    Treina o modelo e retorna métricas.

    TODO: Implementar o loop de treinamento:
        1. Criar DataLoaders para treino e validação
        2. Definir o modelo, loss function e optimizer
            - Loss: BCELoss (Binary Cross Entropy)
            - Optimizer: Adam
        3. Loop de treinamento:
            - Forward pass
            - Calcular loss
            - Backward pass
            - Atualizar pesos
        4. A cada N épocas, avaliar no conjunto de validação
        5. Registrar métricas: loss, acurácia, precision, recall, F1

    Dicas:
        - Use torch.no_grad() para avaliação
        - Considere early stopping para evitar overfitting
        - Use class_weight ou oversampling se os dados forem desbalanceados
        - Salve o melhor modelo (menor val_loss) com torch.save()

    Returns:
        Dicionário com métricas finais e histórico de treinamento.
    """
    pass


def avaliar_modelo(model, X_test, y_test, threshold: float = 0.5) -> dict:
    """
    Avalia o modelo no conjunto de teste.

    TODO: Implementar a avaliação:
        1. Fazer previsões com o modelo treinado
        2. Calcular métricas usando sklearn.metrics:
            - accuracy_score
            - precision_score
            - recall_score
            - f1_score
            - roc_auc_score
            - confusion_matrix
            - classification_report
        3. Plotar: curva ROC, matriz de confusão

    Returns:
        Dicionário com todas as métricas.
    """
    pass


if __name__ == "__main__":
    # TODO: Orquestrar o pipeline completo:
    # 1. Carregar features (from src.features.extract import ...)
    # 2. Preparar dados (split, normalizar, converter para tensores)
    # 3. Treinar modelo
    # 4. Avaliar modelo
    # 5. Salvar modelo treinado
    print("Pipeline de treinamento do modelo de churn")
