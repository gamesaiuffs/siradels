from experimentos.scripts.transformações import * 
INF = 10e9

"""
    DICIONÁRIO DE DESCRIÇÃO DAS VARIÁVEIS
    tamanho: Numero de valores que a variavel adiciona ao vetor de observação
    largura: Range de cada variável (de quanto a quanto cada valor pode ir)

    padrão - originais do ambiente
    classes - variáveis divididas em 3 classes 
    classes b - variáveis divididas em duas classes - para ambiente binário
    proporcao - informações descritas em proporções a outras informações 
    original - valor sem transformação 
"""

        
# Verificar se o range das variáveis esta correto 
METODOS_POR_VARIAVEL = {
    "ouro_personagem_padrao": {"funcao": lambda x: limitar_valores(x["jogador_visao"].ouro, [0, 6]), "tamanho": 1, "largura": 7},
    "ouro_personagem_original": {"funcao": lambda x: x["jogador_visao"].ouro, "tamanho": 1, "largura": INF},
    "ouro_personagem_classes": {"funcao": lambda x: intervalos_em_classes(x["jogador_visao"].ouro, [(0, 0, 2), (1, 3, 5), (2, 6, 10000)]), "tamanho": 1, "largura": 3},
    "ouro_personagem_classes_bin": {"funcao": lambda x: intervalos_em_classes(x["jogador_visao"].ouro, [(0, 0, 3), (1, 4, 10000)]), "tamanho": 1, "largura": 2},
    "ouro_personagem_proporcao": {"funcao": lambda x: ouro_personagem_proporcao(x), "tamanho": 1, "largura": None}, 

    "cartas_dist_mao_padrao": {"funcao": lambda x: limitar_valores(len(x["jogador_visao"].cartas_distrito_mao), [0, 5]), "tamanho": 1, "largura": 6},
    "cartas_dist_mao_original": {"funcao": lambda x: len(x["jogador_visao"].cartas_distrito_mao), "tamanho": 1, "largura": INF},
    "cartas_dist_mao_classes": {"funcao": lambda x: intervalos_em_classes(len(x["jogador_visao"].cartas_distrito_mao), [(0, 0, 2), (1, 3, 5), (2, 6, 10000)]), "tamanho": 1, "largura": 3},
    "cartas_dist_mao_classes_bin": {"funcao": lambda x: intervalos_em_classes(len(x["jogador_visao"].cartas_distrito_mao), [(0, 0, 3), (1, 4, 10000)]), "tamanho": 1, "largura": 2},
    "cartas_dist_mao_proporcao": {"funcao": lambda x: cartas_dist_mao_proporcao(x), "tamanho": 1, "largura": None},

    "carta_mais_cara_padrao": {"funcao": lambda x: limitar_valores(encontra_carta_mais_cara(x), [0, 6]), "tamanho": 1, "largura": 7},
    "carta_mais_cara_original": {"funcao": lambda x: encontra_carta_mais_cara(x), "tamanho": 1, "largura": INF},
    "carta_mais_cara_classes": {"funcao": lambda x: intervalos_em_classes(encontra_carta_mais_cara(x), [(0, 0, 2), (1, 3, 5), (2, 6, 10000)]), "tamanho": 1, "largura": 3},
    "carta_mais_cara_classes_bin": {"funcao": lambda x: intervalos_em_classes(encontra_carta_mais_cara(x), [(0, 0, 3), (1, 4, 10000)]), "tamanho": 1, "largura": 2},
    "carta_mais_cara_proporcao": {"funcao": lambda x: encontra_carta_mais_cara(x), "tamanho": 1, "largura": None},

    "carta_mais_barata_padrao": {"funcao": lambda x: limitar_valores(encontra_carta_mais_barata(x), [0, 6]), "tamanho": 1, "largura": 7},
    "carta_mais_barata_original": {"funcao": lambda x: encontra_carta_mais_barata(x), "tamanho": 1, "largura": INF},
    "carta_mais_barata_classes": {"funcao": lambda x: intervalos_em_classes(encontra_carta_mais_barata(x), [(0, 0, 2), (1, 3, 5), (2, 6, 10000)]), "tamanho": 1, "largura": 3},
    "carta_mais_barata_classes_bin": {"funcao": lambda x: intervalos_em_classes(encontra_carta_mais_barata(x), [(0, 0, 3), (1, 4, 10000)]), "tamanho": 1, "largura": 2},
    "carta_mais_barata_proporcao": {"funcao": lambda x: encontra_carta_mais_barata(x), "tamanho": 1, "largura": None},

    "qtd_dist_const_padrao": {"funcao": lambda x: limitar_valores(len(x["jogador_visao"].distritos_construidos), [0, 7]), "tamanho": 1, "largura": 8},
    "qtd_dist_const_original": {"funcao": lambda x: len(x["jogador_visao"].distritos_construidos), "tamanho": 1, "largura": INF},
    "qtd_dist_const_classes": {"funcao": lambda x: intervalos_em_classes(len(x["jogador_visao"].distritos_construidos), [(0, 0, 3), (1, 4, 6), (2, 7, 10000)]), "tamanho": 1, "largura": 3},
    "qtd_dist_const_classes_bin": {"funcao": lambda x: intervalos_em_classes(len(x["jogador_visao"].distritos_construidos), [(0, 0, 6), (1, 7, 10000)]), "tamanho": 1, "largura": 2},
    "qtd_dist_const_proporcao": {"funcao": lambda x: qtd_dist_const_proporcao(x), "tamanho": 1, "largura": None},

    "qtd_dist_cada_tipo_padrao": {"funcao": lambda x: limitar_valores_vetor(conta_tipos_distritos(x["jogador_visao"]), [0, 3]), "tamanho": 5, "largura": 4},
    "qtd_dist_cada_tipo_original": {"funcao": lambda x: conta_tipos_distritos(x["jogador_visao"]), "tamanho": 5, "largura": INF},
    "qtd_dist_cada_tipo_classes": {"funcao": lambda x: intervalos_em_classes_vetor(conta_tipos_distritos(x["jogador_visao"]), [(0, 0, 2), (1, 3, 4), (2, 5, 10000)]), "tamanho": 5, "largura": 3},
    "qtd_dist_cada_tipo_classes_bin": {"funcao": lambda x: intervalos_em_classes_vetor(conta_tipos_distritos(x["jogador_visao"]), [(0, 0, 6), (1, 7, 10000)]), "tamanho": 5, "largura": 2},
    "qtd_dist_cada_tipo_proporcao": {"funcao": lambda x: qtd_dist_cada_tipo_proporcao(x), "tamanho": 5, "largura": None},

    "dist_const_jog_mais_const_padrao": {"funcao": lambda x: limitar_valores(max(conta_distritos_construidos(x)), [0, 7]), "tamanho": 1, "largura": 8},
    "dist_const_jog_mais_const_original": {"funcao": lambda x: max(conta_distritos_construidos(x)), "tamanho": 1, "largura": INF},
    "dist_const_jog_mais_const_classes": {"funcao": lambda x: intervalos_em_classes(max(conta_distritos_construidos(x)), [(0, 0, 2), (1, 3, 4), (2, 5, 10000)]), "tamanho": 1, "largura": 3},
    "dist_const_jog_mais_const_classes_bin": {"funcao": lambda x: intervalos_em_classes(max(conta_distritos_construidos(x)), [(0, 0, 6), (1, 7, 10000)]), "tamanho": 1, "largura": 2},
    "dist_const_jog_mais_const_proporcao": {"funcao": lambda x: max(conta_distritos_construidos(x)) / 7, "tamanho": 1, "largura": None},

    "jog_mais_cartas_mao_padrao": {"funcao": lambda x: limitar_valores(max(conta_cartas_mao(x)), [0, 5]), "tamanho": 1, "largura": 6},
    "jog_mais_cartas_mao_original": {"funcao": lambda x: max(conta_cartas_mao(x)), "tamanho": 1, "largura": INF},
    "jog_mais_cartas_mao_classes": {"funcao": lambda x: intervalos_em_classes(max(conta_cartas_mao(x)), [(0, 0, 2), (1, 3, 4), (2, 5, 10000)]), "tamanho": 1, "largura": 3},
    "jog_mais_cartas_mao_classes_bin": {"funcao": lambda x: intervalos_em_classes(max(conta_cartas_mao(x)), [(0, 0, 3), (1, 4, 10000)]), "tamanho": 1, "largura": 2},
    "jog_mais_cartas_mao_proporcao": {"funcao": lambda x: jog_mais_cartas_mao_proporcao(x), "tamanho": 1, "largura": None},

    "ouro_oponentes_padrao": {"funcao": lambda x: limitar_valores((sum(conta_ouros_adversarios(x)) // (len(x["jogadores"]) - 1)), [0, 4]), "tamanho": 1, "largura": 5},
    "ouro_oponentes_original": {"funcao": lambda x: conta_ouros_adversarios(x), "tamanho": 4, "largura": INF},
    "ouro_oponentes_classes": {"funcao": lambda x: intervalos_em_classes_vetor(conta_ouros_adversarios(x), [(0, 0, 2), (1, 3, 4), (2, 5, 10000)]), "tamanho": 4, "largura": 3},
    "ouro_oponentes_classes_bin": {"funcao": lambda x: intervalos_em_classes_vetor(conta_ouros_adversarios(x), [(0, 0, 3), (1, 4, 10000)]), "tamanho": 4, "largura": 2},
    "ouro_oponentes_proporcao": {"funcao": lambda x: ouro_oponentes_proporcao(x), "tamanho": 4, "largura": None},        

    "disponibilidade_personagens": {"funcao": lambda x: disponibilidade_personagens(x["tabuleiro"].baralho_personagens), "tamanho": 8, "largura": 2},
    "turno_agente": {"funcao": lambda x: 0 if x["jogador_atual"] is None or x["jogador_atual"].nome != "Agente" else 1, "tamanho": 1, "largura": 2}
}

# Experimento 1 - variação nas representações - todas as variáveis presentes
variaveis_padrao = ['ouro_personagem_padrao', 'cartas_dist_mao_padrao', 'carta_mais_cara_padrao', 'carta_mais_barata_padrao', 'qtd_dist_const_padrao', 'qtd_dist_cada_tipo_padrao', 'dist_const_jog_mais_const_padrao', 'jog_mais_cartas_mao_padrao', 'ouro_oponentes_padrao', 'disponibilidade_personagens', 'turno_agente']
variaveis_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
variaveis_classes = ["ouro_personagem_classes","cartas_dist_mao_classes","carta_mais_cara_classes","carta_mais_barata_classes","qtd_dist_const_classes","qtd_dist_cada_tipo_classes","dist_const_jog_mais_const_classes","jog_mais_cartas_mao_classes","ouro_oponentes_classes", "disponibilidade_personagens", "turno_agente" ]
variaveis_classes_bin = ["ouro_personagem_classes_bin","cartas_dist_mao_classes_bin","carta_mais_cara_classes_bin","carta_mais_barata_classes_bin","qtd_dist_const_classes_bin","qtd_dist_cada_tipo_classes_bin","dist_const_jog_mais_const_classes_bin","jog_mais_cartas_mao_classes_bin","ouro_oponentes_classes_bin", "disponibilidade_personagens", "turno_agente"]
proporcoes = ["ouro_personagem_proporcao", "cartas_dist_mao_proporcao", "carta_mais_cara_proporcao", "carta_mais_barata_proporcao", "qtd_dist_const_proporcao", "qtd_dist_cada_tipo_proporcao", "dist_const_jog_mais_const_proporcao", "jog_mais_cartas_mao_proporcao", "ouro_oponentes_proporcao", "disponibilidade_personagens", "turno_agente"]

variaveis_classes_bin_teste = ["ouro_personagem_classes_bin","cartas_dist_mao_classes_bin","carta_mais_cara_classes_bin","carta_mais_barata_classes_bin","qtd_dist_const_classes_bin","qtd_dist_cada_tipo_classes_bin","dist_const_jog_mais_const_classes_bin","jog_mais_cartas_mao_classes_bin","ouro_oponentes_classes_bin", "turno_agente"]

# Experimento 2 - remoção de variáveis uma a uma - em ordem
menos_ouro_personagem_original = [ "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
menos_cartas_dist_mao_original = ["ouro_personagem_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
menos_carta_mais_cara_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
menos_carta_mais_barata_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
menos_qtd_dist_const_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
menos_qtd_dist_cada_tipo_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original",  "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
menos_dist_const_jog_mais_const_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
menos_jog_mais_cartas_mao_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
menos_ouro_oponentes_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "disponibilidade_personagens", "turno_agente"]


menos_18_17_13 = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "disponibilidade_personagens", "turno_agente"]
menos_18_17_13_14_12 = ["ouro_personagem_original", "cartas_dist_mao_original",  "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "disponibilidade_personagens", "turno_agente"]



REPRESENT = variaveis_padrao