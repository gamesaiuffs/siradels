from classes.Experimento import Experimento
from classes.classifica_estados.ClassificaEstados import ClassificaEstados
from classes.classifica_estados.ColetaEstados import ColetaEstados
from classes.Simulacao import Simulacao
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria

estrategias = []

for i in range(6):          # fixo em 6 players
    estrategias.append(EstrategiaTotalmenteAleatoria(str(i+1)))

# Estrategias fixas e especificas
'''
estrategias.append(EstrategiaDjonatan())
estrategias.append(EstrategiaAndrei())
estrategias.append(EstrategiaBernardo())
estrategias.append(EstrategiaFelipe())
estrategias.append(EstrategiaGustavo())
estrategias.append(EstrategiaJoao())
'''

# Cria simulacao
simulacao = Simulacao(estrategias)

#ColetaEstados.simula_estados(10000)

X, Y = ClassificaEstados.ler_resultados()

ClassificaEstados.treinar_modelo(X, Y)

ClassificaEstados.modelo_info()

simulacao.rodar_simulacao()