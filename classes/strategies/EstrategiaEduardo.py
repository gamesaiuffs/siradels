from classes.strategies.estrategiaEduardoUtils.estrategiaEscolhaDistrito import *
from classes.strategies.estrategiaEduardoUtils.estrategiaEscolhaEstrategia import *
from classes.strategies.estrategiaEduardoUtils.funcoesUtils.calculoTiposDistritos import *

import random


class EstrategiaEduardo(Estrategia):

    estado_interno = {
        "estrategia": 0,                # Estratégia geral
        "qtd_tipos_distritos": {}       # quantos distritos de cada tipo foram construídos
    }

    def __init__(self):
        super().__init__("Eduardo")

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        EstrategiaEduardo.estado_interno["estrategia"] = calcularEstrategiaGeral(estado)
        # debug("---------------------------------------| Escolha de personagem |-------------------------------- ")

        # estratégia de farming
        if EstrategiaEduardo.estado_interno["estrategia"] == Estrategias.Farming.value:
            # Preferência para personagens com bônus de ouro

            # calcular quantos distritos de cada tipo foram construídos
            EstrategiaEduardo.estado_interno["qtd_tipos_distritos"] = calcular_qtd_tipos_distritos_construidos(estado)

            lista_preferencia_personagens = []
            for chave, valor in EstrategiaEduardo.estado_interno["qtd_tipos_distritos"].items():
                if chave == '0': lista_preferencia_personagens.append("Bispo")
                elif chave == '1': lista_preferencia_personagens.append("Senhor da Guerra")
                elif chave == '2': lista_preferencia_personagens.append("Rei")
                elif chave == '3': lista_preferencia_personagens.append("Comerciante")

            # Religioso = 0
            # Militar = 1   
            # Nobre = 2
            # Comercial = 3
            # Especial = 4

            # escolher o menor indice possível da lista de personagens
            for nome_personagem in lista_preferencia_personagens:
                for posicao, escolha_personagem in enumerate(estado.tabuleiro.baralho_personagens):
                    if escolha_personagem.nome == nome_personagem:
                        debug(f"\nFarming - Personagem escolhido pela preferência: {escolha_personagem.nome}")
                        return posicao

            debug("\nFarming\t\tPersonagem: aleatório")
            return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

        # sem estratégia
        else:
            # print("Estratégia - nenhuma\t\tPersonagem: aleatório")
            return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:

        # decisão de cartas ou ouro
        if len(acoes_disponiveis) == 2 and acoes_disponiveis[0] == TipoAcao.ColetarOuro:
            if len(estado.jogador_atual.cartas_distrito_mao) < 2:
                debug("\nEscolheu cartas...")
                return 1 # coletar carta
            else:
                debug("\nEscolheu ouro...")
                return 0 # coletar ouro


        for index_acao, acao in enumerate(acoes_disponiveis):

            # Usar habilidade ladrão --------------------------------------------------------------
            if acao.value == TipoAcao.HabilidadeLadrao.value:
                pass

            # Usar habilidades ilusionista  --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeIlusionistaTrocar.value:
                pass

            elif acao.value == TipoAcao.HabilidadeIlusionistaDescartar.value:
                pass

            # Usar habilidade rei --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeRei.value:
                debug("Ação escolhida: Coletar ouro rei")
                return index_acao

            # Usar habilidade Bispo --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeBispo.value:
                debug("Ação escolhida: Coletar ouro bispo")
                return index_acao

            # Usar habilidade comerciante --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeComerciante.value:
                debug("Ação escolhida: Coletar ouro comerciante")
                return index_acao

            # Usar habilidade senhor da guerra  --------------------------------------------------------------
            elif acao.value == TipoAcao.HabilidadeSenhorDaGuerraColetar.value:
                debug("Ação escolhida: Coletar ouro sr guerra")
                return index_acao

            # contruir distrito ou não --------------------------------------------------------------
            elif acao.value == TipoAcao.ConstruirDistrito.value:
                # estratégia de escolha - valor médio maior do que numero de ouros ---------------------------
                valor_dist, contador, dists_para_construir= 0, 0, 0
                for distrito in estado.jogador_atual.cartas_distrito_mao:
                    valor_dist += distrito.valor_do_distrito
                    contador += 1

                # debug(f"AQUI: Valor tot: {valor_dist} qtd: {contador} Resultado: {valor_dist // contador} qtd_ouro: {estado.jogador_atual.ouro}")
                if contador != 0:
                    if (valor_dist // contador) < estado.jogador_atual.ouro:
                        debug("Ação escolhida: Construir distrito")
                        # print("index", index_acao, acao.name)
                        return index_acao

            elif acao.value == TipoAcao.HabilidadeSenhorDaGuerraDestruir.value:
                pass

            # Usar habilidade comerciante --------------------------------------------------------------
            elif acao.value == TipoAcao.Laboratorio.value:
                pass

            # Usar habilidade comerciante --------------------------------------------------------------
            elif acao.value == TipoAcao.Forja.value:
                pass

        # debug("\nAção escolhida: Passar turno\nHabilidades restantes: ")
        # for acao_restante in acoes_disponiveis:
        #     debug(f"\t{acao_restante.name}")
        # debug("----------------------------------------------------------------------------------------\n")
        return 0

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
        # ordená-los de acordo com a ordem de preferência ditada em cada estratégia
        # especiais primeiro
        # por valor -
    @staticmethod
    def construir_distrito(estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        
        escolha = estrategiaEscolhaDistrito(estado, distritos_para_construir, distritos_para_construir_covil_ladroes, EstrategiaEduardo.estado_interno)

        # debug(f"Distrito escolhido pela estratégia de pesos de farming: {distritos_para_construir[escolha].imprimir_tudo()}")

        return escolha

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade da Ilusionista (escolha do jogador alvo)
    @staticmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        return random.randint(0, len(opcoes_jogadores) - 1)

    # Estratégia usada na habilidade da Ilusionista (escolha de quantas cartas serão descartadas)
    @staticmethod
    def habilidade_ilusionista_descartar_qtd_cartas(estado: Estado, qtd_maxima: int) -> int:
        return random.randint(1, qtd_maxima)

    # Estratégia usada na habilidade da Ilusionista (escolha de qual carta descartar)
    @staticmethod
    def habilidade_ilusionista_descartar_carta(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra_destruir(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        return random.randint(0, len(distritos_para_destruir))

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)
