# Imports
from more_itertools import sort_together
from classes.enum.TipoDistrito import TipoDistrito
from classes.model.Tabuleiro import Tabuleiro
from classes.model.Jogador import Jogador
from experimentos.scripts.transformações import * 
INF = 10e9


class Estado:
    # Construtor
    def __init__(self, tabuleiro: Tabuleiro, jogadores: list[Jogador]):
        self.tabuleiro: Tabuleiro = tabuleiro
        self.jogadores: list[Jogador] = jogadores
        self.turno: int = 0
        self.rodada: int = 0
        self.jogador_atual: Jogador | None = None
        
        # self.metodos_por_variavel = {
        #     "ouro_personagem_padrao": {"funcao": lambda x: limitar_valores(x["jogador_visao"].ouro, [0, 6]), "tamanho": 1},
        #     "ouro_personagem_classes": lambda x: intervalos_em_classes(x["jogador_visao"].ouro, [(1, 0, 2), (2, 3, 5), (3, 6, 10000)]),
        #     "ouro_personagem_proporcao": "",
            
        #     "cartas_dist_mao_padrao": lambda x: limitar_valores(len(x["jogador_visao"].cartas_distrito_mao), [0, 5]),
        #     "cartas_dist_mao_classes": lambda x: intervalos_em_classes(len(x["jogador_visao"].cartas_distrito_mao), [(1, 0, 2), (2, 3, 5), (3, 6, 10000)]),
            
        #     "carta_mais_cara_padrao": lambda x: limitar_valores(encontra_carta_mais_cara(x), [0, 6]),
        #     "carta_mais_cara_classes": lambda x: intervalos_em_classes(encontra_carta_mais_cara(x), [(1, 0, 2), (2, 3, 5), (3, 6, 10000)]),
        #     "carta_mais_cara_proporcao": "",
            
        #     "carta_mais_barata_padrao": lambda x: limitar_valores(encontra_carta_mais_barata(x), [0, 6]),
        #     "carta_mais_barata_classe": lambda x: intervalos_em_classes(encontra_carta_mais_barata(x), [(1, 0, 2), (2, 3, 5), (3, 6, 10000)]),
        #     "carta_mais_barata_proporcao": "",
            
        #     "qtd_dist_const_padrao": lambda x: limitar_valores(len(x["jogador_visao"].distritos_construidos), [0, 7]),
        #     "qtd_dist_const_percent": "",
        #     "qtd_dist_const_proporcao": "",
            
        #     "qtd_dist_cada_tipo_padrao": lambda x: limitar_valores_vetor(conta_tipos_distritos(x), [0, 3]),
        #     "qtd_dist_cada_tipo_vetor_bin": "",
        #     "qtd_dist_cada_tipo_bin": "",
            
        #     "dist_const_jog_mais_const_padrao": lambda x: limitar_valores(max(conta_distritos_construidos(x)), [0, 7]),
        #     "dist_const_jog_mais_const_proporcao": "",
            
        #     "jog_mais_cartas_mao_padrao": lambda x: limitar_valores(max(conta_cartas_mao(x)), [0, 5]),
        #     "jog_mais_cartas_mao_proporcao": "",
            
        #     "ouro_oponentes_padrao": lambda x: limitar_valores((sum(conta_ouros_adversarios(x)) // (len(x["jogadores"]) - 1)), [0, 4]),
        #     "ouro_oponentes_vetor": ""
        # }
        
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
        self.metodos_por_variavel = {
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

        
        self.variaveis_padrao = ['ouro_personagem_padrao', 'cartas_dist_mao_padrao', 'carta_mais_cara_padrao', 'carta_mais_barata_padrao', 'qtd_dist_const_padrao', 'qtd_dist_cada_tipo_padrao', 'dist_const_jog_mais_const_padrao', 'jog_mais_cartas_mao_padrao', 'ouro_oponentes_padrao', 'disponibilidade_personagens', 'turno_agente']
        self.variaveis_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
        self.variaveis_classes = ["ouro_personagem_classes","cartas_dist_mao_classes","carta_mais_cara_classes","carta_mais_barata_classes","qtd_dist_const_classes","qtd_dist_cada_tipo_classes","dist_const_jog_mais_const_classes","jog_mais_cartas_mao_classes","ouro_oponentes_classes", "disponibilidade_personagens", "turno_agente" ]
        self.variaveis_classes_bin = ["ouro_personagem_classes_bin","cartas_dist_mao_classes_bin","carta_mais_cara_classes_bin","carta_mais_barata_classes_bin","qtd_dist_const_classes_bin","qtd_dist_cada_tipo_classes_bin","dist_const_jog_mais_const_classes_bin","jog_mais_cartas_mao_classes_bin","ouro_oponentes_classes_bin", "disponibilidade_personagens", "turno_agente"]
        self.variaveis_classes_bin_teste = ["ouro_personagem_classes_bin","cartas_dist_mao_classes_bin","carta_mais_cara_classes_bin","carta_mais_barata_classes_bin","qtd_dist_const_classes_bin","qtd_dist_cada_tipo_classes_bin","dist_const_jog_mais_const_classes_bin","jog_mais_cartas_mao_classes_bin","ouro_oponentes_classes_bin", "turno_agente"]
        self.proporcoes = ["ouro_personagem_proporcao", "cartas_dist_mao_proporcao", "carta_mais_cara_proporcao", "carta_mais_barata_proporcao", "qtd_dist_const_proporcao", "qtd_dist_cada_tipo_proporcao", "dist_const_jog_mais_const_proporcao", "jog_mais_cartas_mao_proporcao", "ouro_oponentes_proporcao", "disponibilidade_personagens", "turno_agente"]

        
        # Experimento 2 - remoção de variáveis uma a uma - em ordem
        self.menos_ouro_personagem_original = [ "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
        self.menos_cartas_dist_mao_original = ["ouro_personagem_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
        self.menos_carta_mais_cara_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
        self.menos_carta_mais_barata_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
        self.menos_qtd_dist_const_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
        self.menos_qtd_dist_cada_tipo_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original",  "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
        self.menos_dist_const_jog_mais_const_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "jog_mais_cartas_mao_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
        self.menos_jog_mais_cartas_mao_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "ouro_oponentes_original", "disponibilidade_personagens", "turno_agente"]
        self.menos_ouro_oponentes_original = ["ouro_personagem_original", "cartas_dist_mao_original", "carta_mais_cara_original", "carta_mais_barata_original", "qtd_dist_const_original", "qtd_dist_cada_tipo_original", "dist_const_jog_mais_const_original", "jog_mais_cartas_mao_original", "disponibilidade_personagens", "turno_agente"]
        
        
        
        self.variaveis = self.menos_ouro_oponentes_original
        
        
    def print_estado(self, estado, estado_vetor_teste, estado_vetor):
         print(f"""
        Original: {estado_vetor_teste} 
        Classes:  {estado_vetor}
        Ouro adversarios: {conta_ouros_adversarios(estado)}
        Ouro agente: {estado["jogador_visao"].ouro}
        """)

    # To String
    def __str__(self):
        jogadores_print_str = ''
        for jogador in self.jogadores:
            jogadores_print_str += jogador.__str__()
            jogadores_print_str += '\n'
        return f'\nRODADA {self.rodada}\nTURNO {self.turno}\n\n' \
               f'Tabuleiro: {self.tabuleiro}\nJogadores: {jogadores_print_str}'
               
    def calcula_tamanho_vetor_obsercacao(self):
        tamanhos = []
        for variavel in self.variaveis:
            for _ in range(self.metodos_por_variavel[variavel]["tamanho"]):
                tamanhos.append(self.metodos_por_variavel[variavel]["largura"])
                
        
        return tamanhos

    # A nova rodada é iniciada pelo jogador que possui a coroa e segue em sentido horário
    # Fase de escolha de personagens
    def ordenar_jogadores_coroado(self):
        index_rei = 0
        for i, jogador in enumerate(self.jogadores):
            if jogador.rei:
                index_rei = i
                break
        ordenados = []
        ordenados.extend(self.jogadores[index_rei:])
        ordenados.extend(self.jogadores[:index_rei])
        self.jogadores = ordenados

    # Reorganiza a lista de jogadores conforme a sua pontuação final no jogo
    def ordenar_jogadores_pontuacao(self):
        ordem = [jogador.pontuacao_final for jogador in self.jogadores]
        self.jogadores = list(sort_together([ordem, self.jogadores], reverse=True)[1])
        # Verifica empates e aplica critério de desempate
        for i in range(len(self.jogadores) - 1):
            if (self.jogadores[i].pontuacao_final == self.jogadores[i+1].pontuacao_final
                    and self.jogadores[i].personagem.rank < self.jogadores[i+1].personagem.rank):
                self.jogadores[i], self.jogadores[i+1] = self.jogadores[i+1], self.jogadores[i]

    
    # Geração do espaço o observavel do jogo     
    def converter_estado(self, openaigym: bool = False) -> list[float]:
        
        # Controle de quem ve o estado
        jogador_visao = None
        if openaigym:
            for jogador in self.jogadores:
                if jogador.nome == 'Agente':
                    jogador_visao = jogador
        else:
            jogador_visao = self.jogador_atual
        
        # Variaveis usadas 
        estado = {
            "jogador_visao": jogador_visao,
            "jogadores": self.jogadores,
            "tabuleiro": self.tabuleiro,
            "jogador_atual": self.jogador_atual
        }
        
        estado_vetor = []
        # estado_vetor_teste = []
        
        # # Gera variáveis de teste 
        # for var in self.variaveis_original: 
        #     representacao = self.metodos_por_variavel[var]["funcao"](estado)
            
        #     if isinstance(representacao, list):
        #         # for item in representacao: estado_vetor_teste.append(item) 
        #         estado_vetor_teste.extend(representacao)
        #     else: estado_vetor_teste.append(representacao)
        
        
        
        # Gera variáveis para ambiente 
        for var in self.variaveis: 
            representacao = self.metodos_por_variavel[var]["funcao"](estado)
            # print(var, representacao)
            if isinstance(representacao, list):
                # for item in representacao: estado_vetor_teste.append(item) 
                estado_vetor.extend(representacao)
            else: estado_vetor.append(representacao)
            
        # print(estado_vetor_teste)    
        
        # self.print_estado(estado, estado_vetor_teste, estado_vetor)
        # print(estado_vetor)
        return estado_vetor
        
        
    # def converter_estado(self, openaigym: bool = False) -> list[int]:
    #     # Controle de quem ve o estado
    #     jogador_visao = None
    #     if openaigym:
    #         for jogador in self.jogadores:
    #             if jogador.nome == 'Agente':
    #                 jogador_visao = jogador
    #     else:
    #         jogador_visao = self.jogador_atual

    #     estado_vetor = []

    #     # Qtd ouro [0,1,2,3,4,5,>=6]
    #     if jogador_visao.ouro >= 6:
    #         estado_vetor.append(6)
    #     else:
    #         estado_vetor.append(jogador_visao.ouro)
        
    #     # Qtd carta mão [0,1,2,3,4,>=5]
    #     if len(jogador_visao.cartas_distrito_mao) >= 5:
    #         estado_vetor.append(5)
    #     else:
    #         estado_vetor.append(len(jogador_visao.cartas_distrito_mao))
        
    #     # Carta mão mais cara [0 a 6]
    #     # Carta mão mais barata [0 a 6]
    #     maior_custo = 0
    #     menor_custo = 10
    #     for distrito in jogador_visao.cartas_distrito_mao:
    #         # descobre o distrito mais caro da mao
    #         if distrito.valor_do_distrito > maior_custo:
    #             maior_custo = distrito.valor_do_distrito
    #         # descobre o distrito mais barato da mao
    #         if distrito.valor_do_distrito < menor_custo:
    #             menor_custo = distrito.valor_do_distrito
    #     if menor_custo == 10:
    #         menor_custo = 0
    #     estado_vetor.append(maior_custo)
    #     estado_vetor.append(menor_custo)

    #     # Qtd distritos construido [0 a 7+]
    #     if len(jogador_visao.distritos_construidos) > 7:
    #         estado_vetor.append(7)
    #     else:
    #         estado_vetor.append(len(jogador_visao.distritos_construidos))
        
    #     # Qtd distrito construido Militar [0,1,2,>=3]
    #     # Qtd distrito construido Religioso [0,1,2,>=3]
    #     # Qtd distrito construido Nobre [0,1,2,>=3]
    #     # Qtd distrito construido Comercial [0,1,2,>=3]
    #     # Qtd distrito construido Especial [0,1,2,>=3]
    #     nobre = 0
    #     religioso = 0
    #     militar = 0
    #     comercial = 0
    #     especial = 0
    #     for distrito in jogador_visao.distritos_construidos:
    #         if distrito.tipo_de_distrito == TipoDistrito.Nobre:
    #             nobre += 1
    #         if distrito.tipo_de_distrito == TipoDistrito.Religioso:
    #             religioso += 1
    #         if distrito.tipo_de_distrito == TipoDistrito.Militar:
    #             militar += 1
    #         if distrito.tipo_de_distrito == TipoDistrito.Comercial:
    #             comercial += 1
    #         if distrito.tipo_de_distrito == TipoDistrito.Especial:
    #             especial += 1
    #     if nobre >= 3:
    #         estado_vetor.append(3)
    #     else:
    #         estado_vetor.append(nobre)
    #     if religioso >= 3:
    #         estado_vetor.append(3)
    #     else:
    #         estado_vetor.append(religioso)
    #     if militar >= 3:
    #         estado_vetor.append(3)
    #     else:
    #         estado_vetor.append(militar)
    #     if comercial >= 3:
    #         estado_vetor.append(3)
    #     else:
    #         estado_vetor.append(comercial)
    #     if especial >= 3:
    #         estado_vetor.append(3)
    #     else:
    #         estado_vetor.append(especial)

    #     # Rank do personagem do jogador atual [0 a 8]
    #     # Rank 0 quando o jogador não possui personagem selecionado ainda
    #     estado_vetor.append(jogador_visao.personagem.rank)

    #     # Qtd distrito construido [0 a 7+]
    #     qtd_distritos = 0
    #     for jogador in self.jogadores:
    #         if qtd_distritos < len(jogador.distritos_construidos):
    #             qtd_distritos = len(jogador.distritos_construidos)
    #     if qtd_distritos > 7:
    #         estado_vetor.append(7)
    #     else:
    #         estado_vetor.append(qtd_distritos)
        
    #     # Qtd carta mão [0,1,2,3,4,>=5]
    #     maior_custo = 0
    #     for jogador in self.jogadores:
    #         if maior_custo < len(jogador.cartas_distrito_mao):
    #             maior_custo = len(jogador.cartas_distrito_mao)
    #     if maior_custo >= 5:
    #         estado_vetor.append(5)
    #     else:
    #         estado_vetor.append(maior_custo)

    #     # Média de ouro dos adversários (arredondada para baixo) [0,1,2,3,>=4]
    #     media = 0
    #     for jogador in self.jogadores:
    #         if jogador_visao != jogador:
    #             media += jogador.ouro
    #     media = media // (len(self.jogadores) - 1)
    #     if media > 4:
    #         media = 4
    #     estado_vetor.append(media)

    #     # Conjunto de flags para personagens disponíveis
    #     # Devem ficar por último no mapeamento do estado para lógica de verificação na classe Citadels funcionar
    #     p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = 0
    #     for carta in self.tabuleiro.baralho_personagens:
    #         if carta.rank == 1:
    #             p1 = 1
    #         elif carta.rank == 2:
    #             p2 = 1
    #         elif carta.rank == 3:
    #             p3 = 1
    #         elif carta.rank == 4:
    #             p4 = 1
    #         elif carta.rank == 5:
    #             p5 = 1
    #         elif carta.rank == 6:
    #             p6 = 1
    #         elif carta.rank == 7:
    #             p7 = 1
    #         elif carta.rank == 8:
    #             p8 = 1
    #     estado_vetor.extend([p1, p2, p3, p4, p5, p6, p7, p8])

    #     # Flag que indica se é o turno do agente
    #     estado_vetor.append(0 if self.jogador_atual is None or self.jogador_atual.nome != "Agente" else 1)

    #     ''' Observações retiradas
    #     # Qtd personagens disponíveis [2,3,4,5,6]
    #     # -1 para aproveitar idx do vetor do 1 ao 5
    #     if self.tabuleiro.baralho_personagens:
    #         estado_vetor.append(len(self.tabuleiro.baralho_personagens) - 1)
    #     else:
    #         estado_vetor.append(0)

    #     # Pontuacao [0-3,4-7,8-11,12-15,16-19,20-23,>=24]
    #     if jogador_visao.pontuacao <= 3:
    #         estado_vetor.append(0)
    #     elif jogador_visao.pontuacao <= 7:
    #         estado_vetor.append(1)
    #     elif jogador_visao.pontuacao <= 11:
    #         estado_vetor.append(2)
    #     elif jogador_visao.pontuacao <= 15:
    #         estado_vetor.append(3)
    #     elif jogador_visao.pontuacao <= 19:
    #         estado_vetor.append(4)
    #     elif jogador_visao.pontuacao <= 23:
    #         estado_vetor.append(5)
    #     else:
    #         estado_vetor.append(6)
            
    #     # Qtd ouro [0,1,2,3,4,5,>=6]
    #     maior_custo = 0
    #     for jogador in self.jogadores:
    #         if maior_custo < jogador.ouro:
    #             maior_custo = jogador.ouro
    #     if maior_custo >= 6:
    #         estado_vetor.append(6)
    #     else:
    #         estado_vetor.append(maior_custo)
            
    #     # Otimizado para regra de 5 jogadores onde no máximo 6 opções de escolha são possíveis
    #     # Personagem disponivel para escolha
    #     personagens = 0b0
    #     for carta in self.tabuleiro.baralho_personagens:
    #         if carta.rank == 1:
    #             personagens += 0b1
    #         if carta.rank == 2:
    #             personagens += 0b10
    #         if carta.rank == 3:
    #             personagens += 0b100
    #         if carta.rank == 4:
    #             personagens += 0b1000
    #         if carta.rank == 5:
    #             personagens += 0b10000
    #         if carta.rank == 6:
    #             personagens += 0b100000
    #         if carta.rank == 7:
    #             personagens += 0b1000000
    #         if carta.rank == 8:
    #             personagens += 0b10000000
    #     estado_vetor.append(int(personagens))

    #     # Otimizado para regra de 5 jogadores onde sempre uma carta é descartada de forma visível
    #     # Personagem visivel descartado
    #     if self.tabuleiro.cartas_visiveis:
    #         cartas_visiveis = self.tabuleiro.cartas_visiveis[0].rank
    #         estado_vetor.append(cartas_visiveis)
    #     else:
    #         estado_vetor.append(0)
    #     '''
    #     return estado_vetor
        
        
