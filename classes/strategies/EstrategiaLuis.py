from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
from classes.enum.TipoPersonagem import TipoPersonagem
from classes.enum.TipoDistrito import TipoDistrito
import random


class EstrategiaLuisII(Estrategia):
    def __init__(self, nome: str = 'João Luis'):
        super().__init__(nome)

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        # constantes
        taxa_construcao = 4
        taxa_construcao = 4
        grande_incentivo = 3
        medio_incentivo = 2
        pequeno_incentivo = 1
        certeza = 1000

        jogador = estado.jogador_atual
        tabuleiro = estado.tabuleiro
        personagens = estado.tabuleiro.personagens
        decision = 0

        def decisao():
            # Ação final da tomada de ação selecionando a carta mais benéfica
            top_choice = max(peso_escolha.items(), key=lambda item: item[0])
            for index, carta in enumerate(estado.tabuleiro.baralho_personagens):
                name = carta.nome
                if name == top_choice[0]:
                    return index
                else:
                    return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

        peso_escolha = {personagem.nome: 0 for personagem in personagens}
        sentimento = {
            'avareza': 0,  # Foca em ganhar ouro e construir
            'violencia': 0,  # Foca em prejudicar outros jogadores
            'gasto': 0,  # Gasta tudo
        }

        if jogador.cartas_distrito_mao == 0 and len(jogador.distritos_construidos) < 5:
            sentimento['avareza'] += medio_incentivo
        elif jogador.ouro <= 5:
            sentimento['avareza'] += pequeno_incentivo

        if any(inimigo.pontuacao > estado.jogador_atual.pontuacao for inimigo in estado.jogadores):
            sentimento['violencia'] += pequeno_incentivo

        if jogador.ouro >= 4:
            sentimento['gasto'] += certeza
        sentimento_atual = max(sentimento.items(), key=lambda item: item[1])[0]

        # Calculate distrito total cost
        custo_distritos = sum(distrito.valor_do_distrito for distrito in jogador.cartas_distrito_mao)

        # Initialize choice weights
        peso_escolha = {personagem.nome: 0 for personagem in personagens}

        if sentimento_atual == 'avareza':
            for personagem in personagens:
                if personagem.tipo_personagem == TipoPersonagem.Comerciante:
                    peso_escolha[personagem.nome] += grande_incentivo
                elif jogador.ouro > 0:
                    if personagem.tipo_personagem == TipoPersonagem.Arquiteta and custo_distritos // jogador.ouro >= taxa_construcao:
                        peso_escolha[personagem.nome] += grande_incentivo
                elif personagem.tipo_personagem == TipoPersonagem.Rei:
                    peso_escolha[personagem.nome] += medio_incentivo
                    if TipoDistrito.Nobre in jogador.distritos_construidos:
                        peso_escolha[personagem.nome] += pequeno_incentivo
                elif len(jogador.distritos_construidos) > 7 and personagem.tipo_personagem == TipoPersonagem.Bispo:
                    peso_escolha[personagem.nome] -= pequeno_incentivo

        elif sentimento_atual == 'violencia':
            for personagem in personagens:
                if personagem.tipo_personagem == TipoPersonagem.Rei:
                    peso_escolha[personagem.nome] -= grande_incentivo
                elif jogador.cartas_distrito_mao == 0 and personagem.tipo_personagem == TipoPersonagem.Ilusionista:
                    peso_escolha[personagem.nome] += medio_incentivo
                elif any(inimigo.pontuacao > estado.jogador_atual.pontuacao for inimigo in
                         estado.jogadores) and personagem.tipo_personagem == TipoPersonagem.SenhorDaGuerra and jogador.ouro >= 4:
                    peso_escolha[personagem.nome] += medio_incentivo
                elif personagem.tipo_personagem in (TipoPersonagem.Ladrao, TipoPersonagem.Assassina):
                    peso_escolha[personagem.nome] += pequeno_incentivo
        elif sentimento_atual == 'gasto':
            for personagem in personagens:
                if personagem.tipo_personagem == TipoPersonagem.Arquiteta:
                    peso_escolha[personagem.nome] += certeza
                elif personagem.tipo_personagem == TipoPersonagem.Rei:
                    peso_escolha[personagem.nome] += grande_incentivo
                    if TipoDistrito.Nobre in jogador.distritos_construidos:
                        peso_escolha[personagem.nome] += pequeno_incentivo
                elif len(jogador.distritos_construidos) > 7 and personagem.tipo_personagem == TipoPersonagem.Bispo:
                    peso_escolha[personagem.nome] -= pequeno_incentivo

        def decisao(peso):
            # Seleciona a ação baseada no peso mais favorável
            melhor_escolha = max(peso.items(), key=lambda item: item[1])
            for index, carta in enumerate(estado.tabuleiro.baralho_personagens):
                if carta.nome == melhor_escolha[0]:
                    return index
            return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

        return decisao(peso_escolha)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        # Deixa passar turno por último
        acao_escolhida = random.randint(0, len(acoes_disponiveis) - 1)
        while len(acoes_disponiveis) > 1 and acoes_disponiveis[acao_escolhida] == TipoAcao.PassarTurno:
            acao_escolhida = random.randint(0, len(acoes_disponiveis) - 1)
        return acao_escolhida

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
        # Retira opções de personagens descartados
        opcoes = []
        for personagem in opcoes_personagem:
            if personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes.append(personagem)
        return random.randint(0, len(opcoes) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)
        # Retira opções de personagens descartados
        opcoes = []
        for personagem in opcoes_personagem:
            if personagem not in estado.tabuleiro.cartas_visiveis:
                opcoes.append(personagem)
        return random.randint(0, len(opcoes) - 1)

    # Estratégia usada na habilidade da Ilusionista (escolha do jogador alvo)
    @staticmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        return random.randint(0, len(opcoes_jogadores) - 1)
        # Ilusionista sempre troca de mão com o adversário que possui mais cartas, o desempate é uma escolha aleatória entre empatados
        mais_cartas = 0
        for jogador in opcoes_jogadores:
            if len(jogador.cartas_distrito_mao) > mais_cartas:
                mais_cartas = len(jogador.cartas_distrito_mao)
        opcoes = []
        for idx, jogador in enumerate(opcoes_jogadores):
            if len(jogador.cartas_distrito_mao) == mais_cartas:
                opcoes.append(idx)
        return random.sample(opcoes, 1)[0]

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
        return random.randint(0, len(distritos_para_destruir) - 1)

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)
