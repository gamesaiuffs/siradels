import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Exemplo: Ouro do personagem variando de 0 a 10
ouro_personagem = np.arange(0, 11)

acoes = ["Ação 1", "Ação 2", "Ação 3", "Ação 4", "Ação 5", "Ação 6", "Ação 7", "Ação 8"]

# Simulando probabilidades de escolha (de um modelo hipotético)
probabilidades = np.random.rand(len(ouro_personagem), len(acoes))
probabilidades /= probabilidades.sum(axis=1, keepdims=True)  # Normaliza para somar 1
print(probabilidades)
# Criando o heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(probabilidades, annot=True, cmap="coolwarm", xticklabels=acoes, yticklabels=ouro_personagem)
plt.xlabel("Ações")
plt.ylabel("Ouro do Personagem")
plt.title("Heatmap de Probabilidades de Ação")
plt.show()


# acoes_discretas = ["Atacar", "Defender", "Comprar Carta", "Construir"]
# ouro_vals = np.arange(0, 11)
# cartas_vals = np.arange(0, 6)

# # Simulando decisões do modelo (cada número representa uma ação)
# decisoes = np.random.randint(0, len(acoes_discretas), size=(len(ouro_vals), len(cartas_vals)))

# plt.figure(figsize=(8, 6))
# sns.heatmap(decisoes, cmap="tab10", xticklabels=cartas_vals, yticklabels=ouro_vals)
# plt.xlabel("Cartas na Mão")
# plt.ylabel("Ouro do Personagem")
# plt.title("Heatmap de Mudança de Política")
# plt.show()