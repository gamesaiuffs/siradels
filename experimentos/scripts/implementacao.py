# from experimentos.scripts.transformações import * 
from itertools import product

def discretizar(valor, intervalos):
    """
    Recebe uma lista com valores de intervalos e um valor, 
    e então retorna o a classe (intervalo) ao qual o valor pertence. 
    """
    for i, limite in enumerate(intervalos):
        if valor <= limite:
            return limite
    return len(intervalos)

def binarizar(valor, limite):
    """
    Recebe um valor de entrada e um valor de limite.
    retorna 1 se valor > limite, senão 0.  
    """
    return 1 if valor > limite else 0

def escalar(valor, min_val, max_val):
    """
    Recebe um valor de entrada e o valor mínimo e máximo de escala. 
    Retorna o valor de entrada normalizado de acordo com o intervalo.
    """
    return (valor - min_val) / (max_val - min_val)

def codificar_one_hot(valor, categorias):
    """
    Recebe um valor e uma lista com as categorias de valores.
    Retorna a entrada codificada em one hot.
    """
    vetor = [0] * len(categorias)
    if valor in categorias:
        vetor[categorias.index(valor)] = 1
    return vetor

# Novos metodos 
def limitar_valores(valor: int, limites: list):
    """
    Recebe um valor e os limites [inferior, superior]
    Retorna o valor dentro dos limites
    """
    if valor < limites[0]: return limites[0]
    elif valor > limites[1]: return limites[1]
    else: return valor
    
def limitar_valores_vetor(valores: list, limites: list):
    """
    Recebe um vetor de valores e os limites [inferior, superior]
    Retorna um vetor com os valores dentro dos limites
    """
    lista = []
    for val in valores:
        if val < limites[0]: lista.append(limites[0])
        elif val > limites[1]: lista.append(limites[1])
        else: lista.append(val)
        
    return lista

def intervalors_em_classes(valor, limites):
    """
    Recebe um valor e as classes, com limite inferior e superior 
        [(classe, lim_inf, lim_sup), (classe, lim_inf, lim_sup)] 
        [(1, 0, 2), (2, 3, 4), (3, 5, 10000)]
    Retorna a classe ao qual o valor pertence
    """
    for classe, lim_inf, lim_sup in limites:
        if valor >= lim_inf and valor <= lim_sup: return classe
        
    raise Exception("Classe não encontrada")

# exemplo 
# metodos_por_variavel = {
#     "ouro": [lambda x: discretizar(x, [1, 3, 5]), lambda x: escalar(x, 0, 10)],
#     "cartas_na_mao": [lambda x: binarizar(x, 3), lambda x: escalar(x, 0, 5)],
#     "mais_cara": [lambda x: discretizar(x, [3, 5]), lambda x: escalar(x, 0, 10)],
# }


metodos_por_variavel = {
    "ouro_personagem_padrao": lambda x: limitar_valores(x, [0, 6]),
    "ouro_personagem_classes": lambda x: intervalors_em_classes(x, [("pouco", 0, 2), ("medio", 3, 5), ("muito", 6, 10000)]),
    "ouro_personagem_proporcao": "",
    "cartas_dist_mao_padrao": lambda x: limitar_valores(x, [0, 5]),
    "cartas_dist_mao_classes": "",
    "carta_mais_cara_padrao": lambda x: limitar_valores(x, [0, 6]),
    "carta_mais_cara_classes": "",
    "carta_mais_cara_proporcao": "",
    "carta_mais_barata_padrao": lambda x: limitar_valores(x, [0, 6]),
    "carta_mais_barata_classe": "",
    "carta_mais_barata_proporcao": "",
    "qtd_dist_const_padrao": lambda x: limitar_valores_vetor(x, [0, 3]),
    "qtd_dist_const_percent": "",
    "qtd_dist_const_proporcao": "",
    "qtd_dist_cada_tipo_padrao": lambda x: limitar_valores_vetor(x, [0, 3]),
    "qtd_dist_cada_tipo_vetor_bin": "",
    "qtd_dist_cada_tipo_bin": "",
    "dist_const_jog_mais_const_padrao": lambda x: limitar_valores(x, [0, 7]),
    "dist_const_jog_mais_const_proporcao": "",
    "jog_mais_cartas_mao_padrao": lambda x: limitar_valores(x, [0, 5]),
    "jog_mais_cartas_mao_proporcao": "",
    "ouro_oponentes_padrao": lambda x: limitar_valores(x, [0, 4]),
    "ouro_oponentes_vetor": "",
    "ouro_oponentes_media": "",
}


print(metodos_por_variavel["qtd_dist_const_padrao"]([-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))


# combinacoes = list(product(*metodos_por_variavel.values()))