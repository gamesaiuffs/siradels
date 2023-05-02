from Simulacao import Simulacao
from classes.strategies.EstrategiaFelipe import EstrategiaFelipe
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria
from classes.strategies.EstrategiaManual import EstrategiaManual

estrategias = (EstrategiaTotalmenteAleatoria(),
               EstrategiaFelipe(),
               EstrategiaTotalmenteAleatoria(),
               EstrategiaTotalmenteAleatoria())
simulacao = Simulacao(estrategias)
simulacao.rodar_simulacao()
