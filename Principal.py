from classes.Experimento import Experimento
from classes.ClassificaEstados import ClassificaEstados

salvaEstados = ClassificaEstados()

#salvaEstados.salvar_modelo(salvaEstados.inicializar_estados())


# Cria um arquivo com dados e um com rotulos a partir da quantidade de partidas dos parametros
salvaEstados.coleta_estados_finais_publicos(50)

#salvaEstados.calcula_porcentagem(0)
