from Simulacao import Simulacao
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.strategies.EstrategiaManual import EstrategiaManual

estrategias = (EstrategiaTotalmenteAleatoria(),
               EstrategiaTotalmenteAleatoria(),
               EstrategiaTotalmenteAleatoria(),
               EstrategiaTotalmenteAleatoria())
simulacao = Simulacao(estrategias)
simulacao.rodar_simulacao()
