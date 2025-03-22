import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from stable_baselines3 import DQN
from classes.Experimento import Experimento
import random

from classes.strategies.Estrategia import Estrategia
from classes.strategies.Agente import Agente
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria


import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats import norm 
import statistics 
import seaborn as sns
  

path = "experimentos/teste10cors"
files = "in_"
num_files = 10

data = []
pontos = []
estrategias = []

for idx in range(num_files): 
    model = DQN.load(os.path.join(path, files + str(idx), "10"))
    
    estrategias = [Agente(model=model), EstrategiaTotalmenteAleatoria("Rand 1"), EstrategiaTotalmenteAleatoria("Rand 2"), EstrategiaTotalmenteAleatoria("Rand 3"), EstrategiaTotalmenteAleatoria("Rand 4")]
    
    vitorias, pts = Experimento.testar_estrategias_analise(estrategias=estrategias, qtd_simulacao_maximo=100)
    data.append(vitorias)
    pontos.append(statistics.mean(pts))
    

sorted(pontos)

print("Pontuacoess: ", pontos)
print("Vitórias", data)

# Dados de exemplo
# data = np.random.normal(loc=0, scale=1, size=1000)

# # test = [12, 22, 7, 17, 17, 6, 13, 10, 5, 12, 18, 24, 15, 18, 18, 19, 12, 7, 13, 12, 21, 15, 22, 5, 20, 14, 23, 22, 21, 23]

# # teste = [random.randint(5, 60) for _ in range(1000)]

# Plotando histograma e curva de densidade
# sns.histplot([data, pontos], kde=True)
# sns.histplot(pts, kde=True)
# plt.xlabel("Valores")
# plt.xlim(0, 100)
# # plt.ylim(0, 15)
# plt.ylabel("Densidade")
# plt.title("Histograma com Curva de Densidade")
# plt.savefig("analise.png")

# sns.histplot(pontos, kde=True)
# plt.xlabel("Valores")
# plt.xlim(0, 25)
# plt.ylim(0, 15)
# plt.ylabel("Densidade")
# plt.title("Histograma com Curva de Densidade")
# plt.savefig("pontos.png")

# print([random.randint(5, 25) for _ in range(30)])


# Plot between -10 and 10 with .001 steps. 
# x_axis = np.arange(-20, 20, 0.01) 
# x_axis = sorted([12, 22, 7, 17, 17, 6, 13, 10, 5, 12, 18, 24, 15, 18, 18, 19, 12, 7, 13, 12, 21, 15, 22, 5, 20, 14, 23, 22, 21, 23])
# x_axis = sorted([25, 25, 25, 25, 10,10,10,10,10, 5,5,5,5,5])
# print(x_axis)
  
# Calculating mean and standard deviation 
mean = statistics.mean(pontos) 
# moda = statistics.mode(pontos)
sd = statistics.stdev(pontos) 
dp = np.std(pontos)

print("Desvio padrão: ", dp)
print("Média: ", mean)
  
# plt.plot(pontos, norm.pdf(pontos, mean, sd)) 
# sns.hist(pontos, color='lightgreen', ec='black', kde=True)
# figure = sns.displot(pontos, kde=True, bins=15)
# figure.savefig("out.png")


plt.hist(pontos)
plt.show() 