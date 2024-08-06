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
        # --- Declaração de variáveis gerais
        jogador = estado.jogador_atual
        tabuleiro = estado.tabuleiro
        personagens = tabuleiro.baralho_personagens

        def decisao():
            # Ação final da tomada de ação selecionando a carta mais benéfica
            maior_confianca = max(peso_escolhas.items(), key=lambda item: item[0])
            for index, carta in enumerate(estado.tabuleiro.baralho_personagens):
                nome = carta.nome
                if nome == maior_confianca[0]:
                    return index
                else:
                    return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

        peso_escolhas = {}
        for personagem in personagens:
            # Beneficio Financeiro / Agressivo
            id = personagem.nome
            nivel_confianca = 0
            peso_escolhas[id] = [nivel_confianca]
        ids_personagens_disponiveis = peso_escolhas.keys()

        # Mood
        analise = {
            'ambicao': 0,
            'agressividade': 0,
            'resistencia': 0
        }
        # Decide o que é melhor como ação atribuindo motivações
        if estado.jogador_atual.cartas_distrito_mao == 0:
            analise['resistencia'] += 1
        else:
            if TipoPersonagem.Ilusionista in estado.tabuleiro.baralho_personagens:
                peso_escolhas[TipoPersonagem.Ilusionista.name] -= 3
        if estado.jogador_atual.ouro <= 6:
            analise['ambicao'] += 1
        if len(estado.jogador_atual.distritos_construidos) <= 5:
            analise['ambicao'] += 1
            analise['resistencia'] += 1
        else:
            analise['agressividade'] += 1
            analise['resistencia'] += 1
        if any(inimigo.pontuacao > estado.jogador_atual.pontuacao for inimigo in estado.jogadores):
            analise['agressividade'] += 1

        sentimento_dominante = max(analise.items(), key=lambda item: item[0])[0]
        for personagem in personagens:
            if sentimento_dominante == analise['ambicao']:
                # Se personagem x estiver disponivel, aumenta a chance de usar-lo
                if personagem.tipo_personagem == TipoPersonagem.Comerciante or personagem.tipo_personagem == TipoPersonagem.Arquiteta:
                    peso_escolhas[personagem.nome] += random.randint(2, 6)
                elif personagem.tipo_personagem == TipoPersonagem.Rei:
                    peso_escolhas[personagem.nome] += random.randint(2, 5)
                elif len(estado.jogador_atual.distritos_construidos) > 7 and (
                        personagem.tipo_personagem == TipoPersonagem.Bispo):
                    peso_escolhas[personagem.nome] -= random.randint(1, 5)
            if sentimento_dominante == analise['resistencia']:
                if personagem.tipo_personagem == TipoPersonagem.Rei:
                    peso_escolhas[personagem.nome] -= random.randint(1, 5)
                if personagem.tipo_personagem == TipoPersonagem.Ilusionista:
                    peso_escolhas[personagem.nome] += random.randint(1, 5)
            if sentimento_dominante == analise['agressividade']:
                if personagem.tipo_personagem == TipoPersonagem.Ilusionista:
                    peso_escolhas[personagem.nome] += random.randint(1, 5)
                if personagem.tipo_personagem == TipoPersonagem.SenhorDaGuerra:
                    peso_escolhas[personagem.nome] += random.randint(1, 3)
                if personagem.tipo_personagem == TipoPersonagem.Ladrao or personagem.tipo_personagem == TipoPersonagem.Assassina:
                    peso_escolhas[personagem.nome] += random.randint(1, 10)

            # Se não houver cartas, aumenta a chance de pegar o ilusionista

        # Análise dos inimigos
        for inimigo in estado.jogadores:
            if inimigo.personagem.tipo_personagem is not TipoPersonagem.Rei:
                if TipoPersonagem.Assassina in ids_personagens_disponiveis:
                    analise['agressividade'] += 1
            if inimigo.pontuacao > jogador.pontuacao:
                analise['agressividade'] += 1
                # Escolha por influência
                if inimigo.personagem.tipo_personagem in ids_personagens_disponiveis:
                    peso_escolhas[inimigo.personagem.tipo_personagem.name] += random.randint(1, 5)

            return decisao()

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        if TipoAcao.ConstruirDistrito in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.ConstruirDistrito)

        carta_disponivel = estado.jogador_atual.personagem.tipo_personagem
        # Ações disponiveis
        peso_acoes = {}
        for acoes in acoes_disponiveis:
            id = acoes.name
            nivel_confianca = 0
            peso_acoes[id] = nivel_confianca
        ids_acoes_disponiveis = peso_acoes.keys()

        analise = {
            'ambicao': 0,
            'agressividade': 0,
            'resistencia': 0
        }
        # Decide o que é melhor como ação atribuindo motivações
        if estado.jogador_atual.cartas_distrito_mao == 0:
            analise['resistencia'] += 1
        else:
            if TipoPersonagem.Ilusionista in estado.tabuleiro.baralho_personagens:
                peso_acoes[TipoPersonagem.Ilusionista.name] -= 3
        if estado.jogador_atual.ouro <= 6:
            analise['ambicao'] += 1
        if len(estado.jogador_atual.distritos_construidos) <= 5:
            analise['ambicao'] += 1
            analise['resistencia'] += 1
        else:
            analise['agressividade'] += 1
            analise['resistencia'] += 1
        if any(inimigo.pontuacao > estado.jogador_atual.pontuacao for inimigo in estado.jogadores):
            analise['agressividade'] += 1
        if all(inimigo.pontuacao < estado.jogador_atual.pontuacao for inimigo in estado.jogadores):
            analise['agressividade'] += 1
            # Fica mais agressivo se os jogadores inimigos estiverem ganhando
        for inimigo in estado.jogadores:
            if inimigo.pontuacao > estado.jogador_atual.pontuacao:
                analise['ambicao'] += 1

        sentimento_dominante = max(analise.items(), key=lambda item: item[1])[0]
        for acao in acoes_disponiveis:
            if estado.jogador_atual.ouro <= 5 and acao == TipoAcao.ColetarOuro:
                peso_acoes[acao.name] += 2
            if sentimento_dominante == 'ambicao':
                # Se personagem x estiver disponivel, aumenta a chance de usar-lo
                if acao == TipoAcao.HabilidadeComerciante:
                    peso_acoes[acao.name] += random.randint(3, 6)
                if acao == TipoAcao.ColetarOuro or acao == TipoAcao.HabilidadeRei:
                    peso_acoes[acao.name] += random.randint(1, 5)
            if sentimento_dominante == 'resistencia':
                if acao == TipoAcao.HabilidadeIlusionistaTrocar:
                    peso_acoes[acao.name] += random.randint(1, 5)
                if acao == TipoAcao.ColetarCartas:
                    peso_acoes[acao.name] += random.randint(1, 5)
            if sentimento_dominante == 'agressividade':
                if acao == TipoAcao.ColetarOuro or acao == TipoAcao.ConstruirDistrito:
                    peso_acoes[acao.name] += random.randint(1, 5)
                if acao == TipoAcao.HabilidadeIlusionistaTrocar:
                    peso_acoes[acao.name] += random.randint(1, 5)
                if acao == TipoAcao.HabilidadeSenhorDaGuerraDestruir:
                    peso_acoes[acao.name] += random.randint(1, 5)
                if acao == TipoAcao.HabilidadeAssassina or acao == TipoAcao.HabilidadeLadrao:
                    peso_acoes[acao.name] += random.randint(1, 5)

        def decisao():
            # Ação final da tomada de ação selecionando a carta mais benéfica
            maior_confianca = max(peso_acoes.items(), key=lambda item: item[0])
            for index, acao in enumerate(acoes_disponiveis):
                nome = acao.name
                if nome == maior_confianca[0] and TipoAcao.ConstruirDistrito in acoes_disponiveis:
                    return index
                else:
                    return random.randint(0, len(acoes_disponiveis) - 1)

        # Distritos
        tipos_distritos = []
        distritos_construidos = [distrito for distrito in estado.jogador_atual.distritos_construidos]
        for tipo in distritos_construidos:
            tipos_distritos.append(tipo.tipo_de_distrito)
            if TipoAcao.HabilidadeComerciante in acoes_disponiveis:
                peso_acoes[TipoAcao.HabilidadeComerciante.name] += 2

        if TipoDistrito.Nobre in tipos_distritos and TipoAcao.HabilidadeRei in acoes_disponiveis:
            peso_acoes[TipoAcao.HabilidadeRei.name] += 7
        if TipoDistrito.Religioso in tipos_distritos and TipoAcao.HabilidadeBispo in acoes_disponiveis:
            peso_acoes[TipoAcao.HabilidadeBispo.name] += 7
        if TipoDistrito.Comercial in tipos_distritos and TipoAcao.HabilidadeComerciante in acoes_disponiveis:
            peso_acoes[TipoAcao.HabilidadeComerciante.name] += 7
        if TipoDistrito.Militar in tipos_distritos and TipoAcao.HabilidadeSenhorDaGuerraColetar in acoes_disponiveis:
            peso_acoes[TipoAcao.HabilidadeSenhorDaGuerraColetar.name] += 7

        return decisao()

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado, distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes)

        # Escolhe sempre construir o distrito mais caro da mão sempre que possível
        distritos = {}
        for i, distrito in enumerate(distritos_para_construir):
            index = i
            distritos[index] = distrito.valor_do_distrito

        try:
            maior_valor = max(distritos.items(), key=lambda item: item[0])[0]
            return maior_valor - 1
        except ValueError:
            return random.randint(0, tamanho_maximo - 1)

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        lista_opcoes = {}
        for opcoes in opcoes_personagem:
            id = opcoes.nome
            nivel_confianca = 0
            lista_opcoes[id] = nivel_confianca

        def decisao():
            # Ação final da tomada de ação selecionando a carta mais benéfica
            maior_confianca = max(lista_opcoes.items(), key=lambda item: item[0])
            for index, opcao in enumerate(lista_opcoes):
                nome = opcao[index]
                if nome == maior_confianca[0]:
                    return index
                else:
                    return random.randint(0, len(lista_opcoes) - 1)

        for opcao in opcoes_personagem:
            if opcao.tipo_personagem == TipoPersonagem.Comerciante or opcao.tipo_personagem == TipoPersonagem.Arquiteta:
                lista_opcoes[opcao.nome] += 5
            if any(jogador.pontuacao for jogador in estado.jogadores) > estado.jogador_atual.pontuacao:
                if opcao.tipo_personagem == TipoPersonagem.Comerciante:
                    lista_opcoes[opcao.nome] += 7
                elif opcao.tipo_personagem == TipoPersonagem.Bispo:
                    lista_opcoes[opcao.nome] += 1
            if estado.jogador_atual.ouro > 6:
                if opcao.tipo_personagem == TipoPersonagem.Ladrao:
                    lista_opcoes[opcao.nome] += 4

        decisao()
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
