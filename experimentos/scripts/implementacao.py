from experimentos.scripts.transformações import * 
from itertools import product

# exemplo 
# metodos_por_variavel = {
#     "ouro": [lambda x: discretizar(x, [1, 3, 5]), lambda x: escalar(x, 0, 10)],
#     "cartas_na_mao": [lambda x: binarizar(x, 3), lambda x: escalar(x, 0, 5)],
#     "mais_cara": [lambda x: discretizar(x, [3, 5]), lambda x: escalar(x, 0, 10)],
# }


metodos_por_variavel = {
    "JaQtdOuro": [lambda x: discretizar(x, [1, 3, 5]), lambda x: escalar(x, 0, 10)],
    "JaQtdCarta": [],
    "JaCartaCara": [],
    "JaCartaBarata": [],
    "JaConstruidos":[],
    "JaConstruidosMilitar": [],
    "JaConstruidosReligioso": [],
    "JaConstruidosNobre": [],
    "JaConstruidosComercial": [],
    "JaConstruidosEspecial":[],
    "JaPersonagem": [],
    "JmConstruidos": [],
    "JmQtdCarta": [],
    "MediaOuroAdversarios": [],
    "Rank1Disponivel": [],
    "Rank2Disponivel": [],
    "Rank3Disponivel": [],
    "Rank4Disponivel": [],
    "Rank5Disponivel": [],
    "Rank6Disponivel": [],
    "Rank7Disponivel": [],
    "Rank8Disponivel": [],
    "MeuTurno": [],
}


# combinacoes = list(product(*metodos_por_variavel.values()))