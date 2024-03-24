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
            # Ação final da tomada de ação selecionando a carta mais benéfica
            maior_confianca = max(lista_personagens.items(), key=lambda item: item[0])
            for index, carta in enumerate(estado.tabuleiro.baralho_personagens):
                nome = carta.nome
                if nome == maior_confianca[0]:
                    return index
                else:
                    return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

        # --- Declaração de variáveis gerais
        jogador = estado.jogador_atual
        tabuleiro = estado.tabuleiro
        personagens = tabuleiro.baralho_personagens
        economia = [jogador.ouro for jogador in estado.jogadores].sort()

        # Personagens
        lista_personagens = {}
        for personagem in personagens:
            id = personagem.tipo_personagem.name
            nivel_confianca = 0
            lista_personagens[id] = nivel_confianca
        ids_personagens_disponiveis = lista_personagens.keys()

        # Se não houver cartas, aumenta a chance de pegar o ilusionista
        if estado.jogador_atual.cartas_distrito_mao == 0 and TipoPersonagem.Ilusionista.name in ids_personagens_disponiveis:
            lista_personagens[TipoPersonagem.Ilusionista.name] += random.randint(1, 3)
        # Se o Comerciante estiver disponível [...]
        if TipoPersonagem.Comerciante.name in ids_personagens_disponiveis:
            # Aumenta a probabilidade da ação ser benéfica
            lista_personagens[TipoPersonagem.Comerciante.name] += random.randint(2, 5)
            if estado.jogador_atual.ouro < 7:
                lista_personagens[TipoPersonagem.Comerciante.name] += random.randint(2, 5)
        if TipoPersonagem.Arquiteta.name in ids_personagens_disponiveis:
            lista_personagens[TipoPersonagem.Arquiteta.name] += random.randint(2, 5)
        if TipoPersonagem.Rei.name in ids_personagens_disponiveis:
            lista_personagens[TipoPersonagem.Rei.name] += random.randint(1, 4)
        # Se alguém tem dinheiro e o jog está com pouco e o ladrão estiver disponivel
        if (any(jogador.ouro for jogador in
                estado.jogadores) >= 2) and (estado.jogador_atual.ouro <= 1) and (
                TipoPersonagem.Ladrao.name in ids_personagens_disponiveis):
            lista_personagens[TipoPersonagem.Ladrao.name] += random.randint(1, 3)

        if len(estado.jogador_atual.distritos_construidos) > 5 and (
                TipoPersonagem.Bispo.name in ids_personagens_disponiveis):
            lista_personagens[TipoPersonagem.Bispo.name] += random.randint(1, 3)



        # Análise dos inimigos
        for inimigo in estado.jogadores:

            if len(inimigo.distritos_construidos) and (
                    TipoPersonagem.SenhorDaGuerra.name in ids_personagens_disponiveis):
                lista_personagens[TipoPersonagem.SenhorDaGuerra.name] -= 1
                if inimigo.pontuacao > jogador.pontuacao * 2:
                    lista_personagens[TipoPersonagem.SenhorDaGuerra.name] += 2
            # Se o inimigo tiver um assassino ou um ladrão, jogue defensivamente
            if inimigo.personagem.tipo_personagem.Assassina or jogador.personagem.tipo_personagem.Ladrao:
                if TipoPersonagem.Comerciante.name in ids_personagens_disponiveis:
                    lista_personagens[TipoPersonagem.Comerciante.name] -= random.randint(3, 5)
                if TipoPersonagem.Arquiteta.name in ids_personagens_disponiveis:
                    lista_personagens[TipoPersonagem.Arquiteta.name] -= random.randint(3, 5)
                if TipoPersonagem.Rei.name in ids_personagens_disponiveis:
                    lista_personagens[TipoPersonagem.Rei.name] -= random.randint(2, 5)
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
    def habilidade_senhor_da_guerra_destruir(estado: Estado,
                                             distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        return random.randint(0, len(distritos_para_destruir))

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)
