from classes.Experimento import Experimento
from classes.ClassificaEstados import ClassificaEstados

salvaEstados = ClassificaEstados()

#salvaEstados.salvar_modelo(salvaEstados.inicializar_estados())

salvaEstados.simula_estados(1)

# Testar treino
# experimento.testar_modelo_mcts(1000, 4)
