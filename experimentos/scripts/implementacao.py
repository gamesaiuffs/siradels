# from experimentos.scripts.transformações import * 
from itertools import product
# from database.Postgres import *

import psycopg2

class Conexao(object):
    _db=None
    def __init__(self):
        self._db = psycopg2.connect(host='localhost', database='ia', user='postgres', password='admin')
    
    def executar(self, sql):
        cur=self._db.cursor()
        cur.execute(sql)
        cur.close()
        self._db.commit()
        # try:
        #     cur=self._db.cursor()
        #     cur.execute(sql)
        #     cur.close()
        #     self._db.commit()
        # except:
        #     return False
        # return True
    
    def consultar(self, sql):
        rs=None
        cur=self._db.cursor()
        cur.execute(sql)
        rs=cur.fetchall()
        # try:
        #     cur=self._db.cursor()
        #     cur.execute(sql)
        #     rs=cur.fetchall()
        # except:
        #     return None
        return rs
    
    def fechar(self):
        self._db.close()
        

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

conexao = Conexao()


def variaveis_por_permutacao(permutacao): 
    retorno = conexao.consultar(f"""
                    select vr.title from experiment_permutation ep
                    join permutation_representation pe on ep.id = pe.id_permutation
                    join variable_representation vr on pe.id_representation=vr.id
                    where ep.id = {permutacao};
                    """)
    return [item[0] for item in retorno]


def proporcao_ouros(ouros_personagem, ouros_todos):
    """
    Calcula a proporção de ouros de um personagem em relação ao total de ouros na mesa.

    recebe ouros_personagem: int, quantidade de ouros do personagem.\n
    recebe ouros_todos: list, lista contendo os ouros de todos os personagens (incluindo o do próprio personagem).\n
    retorna: float, proporção de ouros do personagem em relação ao total na mesa.
    """
    total_ouros = sum(ouros_todos)
    
    # Evitar divisão por zero caso ninguém tenha ouro
    if total_ouros == 0:
        return 0.0
    
    return ouros_personagem / total_ouros




# exemplo 
# metodos_por_variavel = {
#     "ouro": [lambda x: discretizar(x, [1, 3, 5]), lambda x: escalar(x, 0, 10)],
#     "cartas_na_mao": [lambda x: binarizar(x, 3), lambda x: escalar(x, 0, 5)],
#     "mais_cara": [lambda x: discretizar(x, [3, 5]), lambda x: escalar(x, 0, 10)],
# }


# metodos_por_variavel = {
#     "ouro_personagem_padrao": lambda x: limitar_valores(x, [0, 6]),
#     "ouro_personagem_classes": lambda x: intervalors_em_classes(x, [("pouco", 0, 2), ("medio", 3, 5), ("muito", 6, 10000)]),
#     "ouro_personagem_proporcao": "",
#     "cartas_dist_mao_padrao": lambda x: limitar_valores(x, [0, 5]),
#     "cartas_dist_mao_classes": "",
#     "carta_mais_cara_padrao": lambda x: limitar_valores(x, [0, 6]),
#     "carta_mais_cara_classes": "",
#     "carta_mais_cara_proporcao": "",
#     "carta_mais_barata_padrao": lambda x: limitar_valores(x, [0, 6]),
#     "carta_mais_barata_classe": "",
#     "carta_mais_barata_proporcao": "",
#     "qtd_dist_const_padrao": lambda x: limitar_valores_vetor(x, [0, 3]),
#     "qtd_dist_const_percent": "",
#     "qtd_dist_const_proporcao": "",
#     "qtd_dist_cada_tipo_padrao": lambda x: limitar_valores_vetor(x, [0, 3]),
#     "qtd_dist_cada_tipo_vetor_bin": "",
#     "qtd_dist_cada_tipo_bin": "",
#     "dist_const_jog_mais_const_padrao": lambda x: limitar_valores(x, [0, 7]),
#     "dist_const_jog_mais_const_proporcao": "",
#     "jog_mais_cartas_mao_padrao": lambda x: limitar_valores(x, [0, 5]),
#     "jog_mais_cartas_mao_proporcao": "",
#     "ouro_oponentes_padrao": lambda x: limitar_valores(x, [0, 4]),
#     "ouro_oponentes_vetor": "",
#     "ouro_oponentes_media": "",
# }


# permutacoes_id = [
#     [2, 3], # ouro_personagem
#     [5], # cartas_dist
#     [7, 8], # carta_mais_cara
#     [10, 11], # carta_mais_barata
#     [13, 14], # qtd_dist_const
#     [16], # qtd_dist_cada_tipo
#     [18], # dist_const_jogador_mais_construiu
#     [20], # jogador_mais_cartas_mao
#     [22]  # ouro_oponentes
# ]

# produto = list(
#     product(
#         permutacoes_id[0], 
#         permutacoes_id[1], 
#         permutacoes_id[2], 
#         permutacoes_id[3], 
#         permutacoes_id[4], 
#         permutacoes_id[5], 
#         permutacoes_id[6], 
#         permutacoes_id[7], 
#         permutacoes_id[8]  
#     ))


# for idx, item in enumerate(produto):
#     print(idx + 2, "  ", item)
#     conexao.executar(f"INSERT INTO experiment_permutation(id, id_exp, status) VALUES ({idx + 2}, 1, 'pendente');")
    
#     for var in item:
#         conexao.executar(f"INSERT INTO permutation_representation(id_permutation, id_representation) VALUES ({idx + 2}, {var});")
       
       

# Pesquisar lista de variáveis por permutação
# print(metodos_por_variavel["qtd_dist_const_padrao"]([-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))

# print(variaveis_por_permutacao(1))

# [
#     "ouro_personagem_padrao",
#     "cartas_dist_mao_padrao",
#     "carta_mais_cara_classes",vat
#     "..."
# ]

# resposta = variaveis_por_permutacao(31)
# print(resposta)


# # combinacoes = list(product(*metodos_por_variavel.values()))


if __name__ == "__main__":
    print(proporcao_ouros(4, [1, 3, 6, 3]))