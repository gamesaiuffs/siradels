from abc import ABC, abstractmethod

from classes.strategies.Estrategia import Estrategia

from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoPersonagem import TipoPersonagem
from classes.enum.TipoDistrito import TipoDistrito

from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador

# Imports adicionais
import random
import math

class EstrategiaLuis(Estrategia):
    def __init__(self, descricao: str):
        self.descricao: str = descricao

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        def decisao():
            try:
                maior_confianca = max(lista_personagens.items(), key=lambda item: item[0])[0]
                return lista_personagens[maior_confianca]
            except ValueError:
                return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

        # --- Declaração de variáveis gerais
        jogador = estado.jogador_atual
        tabuleiro = estado.tabuleiro
        personagens = tabuleiro.baralho_personagens
        economia = [jogador.ouro for jogador in estado.jogadores].sort()

        # Personagens
        lista_personagens = {}
        for personagem in personagens:
                id = personagem.tipo_personagem.value
                nivel_confianca = 0
                lista_personagens[id] = nivel_confianca
        ids_personagens_disponiveis = lista_personagens.keys()

        # Ação final da tomada de ação selecionando a carta mais benéfica

        # Se o mercante está disponível, pegue-o.
        if estado.jogador_atual.cartas_distrito_mao == 0 and TipoPersonagem.Ilusionista.value in ids_personagens_disponiveis:
            lista_personagens[TipoPersonagem.Ilusionista.value] += 3
        if TipoPersonagem.Comerciante.value in ids_personagens_disponiveis:
            # Aumenta a probabilidade da ação ser benéfica
            lista_personagens[TipoPersonagem.Comerciante.value] += 3
        # Se alguém tem dinheiro e o ladrão estiver disponivel, aumente o score do Ladrão em 1
        if (any(jogador.ouro for jogador in estado.jogadores) >= 2) and TipoPersonagem.Ladrao.value in ids_personagens_disponiveis:
            lista_personagens[TipoPersonagem.Ladrao.value] += 1


        return decisao()



    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        if len(acoes_disponiveis) > 1:
            return random.randint(1, len(acoes_disponiveis) - 1)
        return 0

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes)
        return random.randint(0, tamanho_maximo - 1)

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
