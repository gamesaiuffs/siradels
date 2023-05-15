from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoPersonagem import TipoPersonagem
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
import random


class EstrategiaDjonatan(Estrategia):
    def __init__(self):
        super().__init__('Djonatan.')
    
    # Verifica se o personagem pode ser alvo
    @staticmethod
    def verificar_personagem(estado: Estado, i) -> int:
        flag = 0
        try:
            if estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[i]):
                flag += 1
        except:
            flag = 0
        return flag

    # Estratégia usada na fase de escolha dos personagens
    @staticmethod
    def escolher_personagem(estado: Estado) -> int:
        
        #flags de controle
        flag = 0
        religiosos = 0
        nobres = 0
        militares = 0

        #define o maior custo
        maior_custo = 0
        for distrito in estado.jogador_atual.cartas_distrito_mao:
                if maior_custo < distrito.valor_do_distrito:
                    maior_custo = distrito.valor_do_distrito
        
        #define o menor custo
        menor_custo = 10
        for distrito in estado.jogador_atual.cartas_distrito_mao:
            if menor_custo > distrito.valor_do_distrito:
                menor_custo = distrito.valor_do_distrito
        
        #controles de estrat�gias
                
            #cardeal carry
        for distrito in estado.jogador_atual.distritos_construidos:
            if distrito.tipo_de_distrito == 0:
                religiosos += 1

            #rei carry
        for distrito in estado.jogador_atual.distritos_construidos:
            if distrito.tipo_de_distrito == 2:
                nobres += 1
            #senhor da guerra carry
        for distrito in estado.jogador_atual.distritos_construidos:
            if distrito.tipo_de_distrito == 1:
                militares += 1
        #### seleção ###

        #caso critico
        for jogador in estado.jogadores:
            if len(jogador.distritos_construidos) <= 5 and len(jogador.distritos_construidos) > 4:
                EstrategiaDjonatan.verificar_personagem(estado, 7)
                if flag > 0:
                    estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[7])  

        #ideal
        #se não houver ladrão e tiver ouro, priorize a alquimista, se não tiver alquimista, priorize a o mago
        
        if estado.tabuleiro.personagens[TipoPersonagem.Ladrao.value] in estado.tabuleiro.cartas_visiveis and estado.jogador_atual.ouro >= maior_custo:
            EstrategiaDjonatan.verificar_personagem(estado, 5)
            if flag > 0:
                return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[5])
            else:
                EstrategiaDjonatan.verificar_personagem(estado, 3)
                if flag > 0:
                    return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[3])   
        #se tiver muita carta, priorizar o cardeal
        if len(estado.jogador_atual.cartas_distrito_mao) >= maior_custo:
            EstrategiaDjonatan.verificar_personagem(estado, 4)
            if flag > 0:
                return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[4])
            
        #se não tiver nada, priorizar a navegadora
        if len(estado.jogador_atual.cartas_distrito_mao) == 0 and estado.jogador_atual.ouro <= 3:
            EstrategiaDjonatan.verificar_personagem(estado, 6)
            if flag > 0:
                return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[6])
            
        #carry de coleta
        if religiosos >= 2 or nobres >= 2 or militares >= 2:
            if militares > nobres and militares > religiosos:
                EstrategiaDjonatan.verificar_personagem(estado, 7)
                if flag > 0:
                    return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[7])
                
            if religiosos > nobres and religiosos > militares:
                EstrategiaDjonatan.verificar_personagem(estado, 4)
                if flag > 0:
                    return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[4])
                
            if nobres > religiosos and nobres > militares:
                EstrategiaDjonatan.verificar_personagem(estado, 0)
                if flag > 0:
                    return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[0])
            
        # SEGUNDO PLANO

        #tente a assassina
        EstrategiaDjonatan.verificar_personagem(estado, 1)
        if flag > 0:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[1])
        
        #tente o ladr�o
        EstrategiaDjonatan.verificar_personagem(estado, 2)
        if flag > 0:
            return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[2])
        
        #se n�o der, pegue o rei
        if estado.tabuleiro.personagens[TipoPersonagem.Navegadora.value] not in estado.tabuleiro.baralho_personagens:
            EstrategiaDjonatan.verificar_personagem(estado, 0)
            if flag > 0:
                return estado.tabuleiro.baralho_personagens.index(estado.tabuleiro.personagens[0])
            
        return random.randint(0, len(estado.tabuleiro.baralho_personagens) - 1)

    # Estratégia usada na fase de escolha das ações no turno
    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        maior_custo = 0
        menor_custo = 10
        if TipoAcao.ColetarCartas in acoes_disponiveis \
                or TipoAcao.ColetarOuro in acoes_disponiveis:
            if len(estado.jogador_atual.cartas_distrito_mao) == 0:
                if TipoAcao.Forja in acoes_disponiveis:
                    if estado.jogador_atual.ouro >= 2:
                        return acoes_disponiveis.index(TipoAcao.Forja)
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
            #distrito de maior custo na m�o
            for distrito in estado.jogador_atual.cartas_distrito_mao:
                if maior_custo < distrito.valor_do_distrito:
                    maior_custo = distrito.valor_do_distrito  
            if estado.jogador_atual.ouro > maior_custo:
                return acoes_disponiveis.index(TipoAcao.ColetarCartas)
            #distrito de menor custo na m�o
            for distrito in estado.jogador_atual.cartas_distrito_mao:
                if menor_custo > distrito.valor_do_distrito:
                    menor_custo = distrito.valor_do_distrito  
            if estado.jogador_atual.ouro < menor_custo:
                return acoes_disponiveis.index(TipoAcao.ColetarOuro)

        #for�a habilidade de personagem
        if TipoAcao.HabilidadeAssassina in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeAssassina)
        if TipoAcao.HabilidadeLadrao in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeLadrao)
        if TipoAcao.HabilidadeMago in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeMago)
        if TipoAcao.HabilidadeRei in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeRei)
        if TipoAcao.HabilidadeCardeal in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeCardeal)
        if TipoAcao.HabilidadeNavegadora in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeNavegadora)
        if TipoAcao.HabilidadeSenhorDaGuerraColetar in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraColetar)        
        if TipoAcao.HabilidadeSenhorDaGuerraDestruir in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.HabilidadeSenhorDaGuerraDestruir)
        if TipoAcao.Museu in acoes_disponiveis:
            for i, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
                if carta in estado.jogador_atual.distritos_construidos:
                    return acoes_disponiveis.index(TipoAcao.Museu)
            for i, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
                if carta.valor_do_distrito == 1:
                    return acoes_disponiveis.index(TipoAcao.Museu)
                
        #if TipoAcao.Forja in acoes_disponiveis:
        #    if estado.jogador_atual.cartas_distrito_mao == 0 and estado.jogador_atual.ouro >= 2:
        #        return acoes_disponiveis.index(TipoAcao.Forja)
        
        if TipoAcao.Laboratorio in acoes_disponiveis:
            for i, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
                if carta in estado.jogador_atual.distritos_construidos:
                    return acoes_disponiveis.index(TipoAcao.Laboratorio)
        if TipoAcao.Arsenal in acoes_disponiveis:
            for jogador in estado.jogadores:
                if jogador != estado.jogador_atual:
                    for distrito in jogador.distritos_construidos:
                        if distrito.valor_do_distrito >= 5:
                            return acoes_disponiveis.index(TipoAcao.Arsenal)
        #for�a constru��o de distritos
        if TipoAcao.ConstruirDistrito in acoes_disponiveis:
            return acoes_disponiveis.index(TipoAcao.ConstruirDistrito)

        return random.randint(0, len(acoes_disponiveis) - 1)

    # Estratégia usada na ação de coletar cartas
    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        maior_custo = 0
        idx = 0
        for i, carta in enumerate(cartas_compradas):
            if carta.tipo_de_distrito == 4:
                return i
        for i, carta in enumerate(cartas_compradas):
            if carta.valor_do_distrito > maior_custo and carta not in estado.jogador_atual.distritos_construidos:
                maior_custo = carta.valor_do_distrito
                idx = i
            return idx
        return random.randint(0, qtd_cartas - 1)

    # Estratégia usada na ação de construir distritos
    @staticmethod
    def construir_distrito(estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_cardeal: list[CartaDistrito],
                           distritos_para_construir_necropole: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[CartaDistrito],
                           distritos_para_construir_estrutura: list[CartaDistrito]) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_cardeal) + \
                         len(distritos_para_construir_necropole) + len(distritos_para_construir_covil_ladroes) + len(distritos_para_construir_estrutura)

        for i, distrito in enumerate(distritos_para_construir):
            if distrito.tipo_de_distrito == 1:
                return i
        for i, distrito in enumerate(distritos_para_construir):
            if distrito.tipo_de_distrito == 2 or distrito.tipo_de_distrito == 0 and estado.jogador_atual.ouro >= distrito.valor_do_distrito and distrito not in estado.jogador_atual.distritos_construidos:
                return i
        try:
            return random.randint(1, tamanho_maximo)
        except:
            return 0

    # Estratégia usada na ação de construir distritos (efeito Cardeal)
    @staticmethod
    def construir_distrito_cardeal(estado: Estado, diferenca: int, i: int) -> int:
            idx = 0
            menor_custo = 10
            for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
                if distrito in estado.jogador_atual.distritos_construidos:
                    return i
                if distrito.valor_do_distrito > menor_custo:
                    menor_custo == distrito.valor_do_distrito
                    idx = i
            return idx

            return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        idx = 0
        menor_custo = 10
        for i, distrito in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if distrito in estado.jogador_atual.distritos_construidos:
                return i
            if distrito.valor_do_distrito > menor_custo:
                menor_custo == distrito.valor_do_distrito
                idx = i
            return idx
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na habilidade da Assassina
    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:

        #mate a navegadora, se não, mate o mago
        if estado.tabuleiro.personagens[TipoPersonagem.Navegadora.value] not in estado.tabuleiro.cartas_visiveis:
            return EstrategiaDjonatan.verificar_personagem(estado, 6)
        if estado.tabuleiro.personagens[TipoPersonagem.Mago.value] not in estado.tabuleiro.cartas_visiveis:
            return EstrategiaDjonatan.verificar_personagem(estado, 3)

        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Ladrão
    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:

        #roube o mago, se não tiver mago, roube a alquimista, se não, roube o senhor da guerra
        if estado.tabuleiro.personagens[TipoPersonagem.Alquimista.value] not in estado.tabuleiro.baralho_personagens:
            return EstrategiaDjonatan.verificar_personagem(estado, 5)
        if estado.tabuleiro.personagens[TipoPersonagem.Mago.value] not in estado.tabuleiro.baralho_personagens:
            return EstrategiaDjonatan.verificar_personagem(estado, 2)
        if estado.tabuleiro.personagens[TipoPersonagem.SenhorDaGuerra.value] not in estado.tabuleiro.baralho_personagens:
            return EstrategiaDjonatan.verificar_personagem(estado, 7)
        
        return random.randint(0, len(opcoes_personagem) - 1)

    # Estratégia usada na habilidade do Mago (escolha do jogador alvo)
    @staticmethod
    def habilidade_mago_jogador(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        #veja quem tem mais cartas
        max_num_cartas = 0
        idx = 0
        
        for i, jogador_alvo in enumerate(opcoes_jogadores):
            if len(jogador_alvo.cartas_distrito_mao) > max_num_cartas:
                max_num_cartas = len(jogador_alvo.cartas_distrito_mao)
                idx = i
        return idx

        return random.randint(0, len(opcoes_jogadores) - 1)

    # Estratégia usada na habilidade do Mago (escolha da carta da mão)
    @staticmethod
    def habilidade_mago_carta(estado: Estado, opcoes_cartas: list[CartaDistrito]) -> int:
        max = 0
        for i, carta in enumerate(opcoes_cartas):
            if carta.tipo_de_distrito.value == 4:
                return i 
        
        for i, carta in enumerate(opcoes_cartas):
            if max < carta.valor_do_distrito and carta.nome_do_distrito not in estado.jogador_atual.distritos_construidos:
                max = carta.valor_do_distrito
                idx = i

        return idx
        return random.randint(0, len(opcoes_cartas) - 1)

    # Estratégia usada na habilidade da Navegadora
    @staticmethod
    def habilidade_navegadora(estado: Estado) -> int:
        if estado.jogador_atual.cartas_distrito_mao == 0:
            return 1
        else:
            if estado.jogador_atual.ouro < 4:
                return 0
            else:
                return 1
            
    # Estratégia usada na habilidade do Senhor da Guerra
    @staticmethod
    def habilidade_senhor_da_guerra(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador, int)]) -> int:
        finalizador = None
        maior_pontuacao = 0
        menor_custo = 10
        idx = 0
        maior_custo = 0
        #maior custo parece render melhores resultados
        for i, (carta, jogador, muralha) in enumerate(distritos_para_destruir):
            if carta.valor_do_distrito > maior_custo and carta not in estado.jogador_atual.distritos_construidos:
                maior_custo = carta.valor_do_distrito
                idx = i
            return idx
        #for i, (distrito, jogador, muralha) in enumerate(distritos_para_destruir):
        #    if distrito.valor_do_distrito < menor_custo:
        #        menor_custo = distrito.valor_do_distrito
        #        idx = i
        #return idx

    # Estratégia usada na ação do Laboratório
    @staticmethod
    def laboratorio(estado: Estado) -> int:
        for i, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if carta in estado.jogador_atual.distritos_construidos:
                return i
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    # Estratégia usada na ação do Arsenal
    @staticmethod
    def arsenal(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        for i, (carta, jogador) in enumerate(distritos_para_destruir):
            if carta.valor_do_distrito >= 5:
                return i
        return random.randint(0, len(distritos_para_destruir))
        
    # Estratégia usada na ação do Museu
    @staticmethod
    def museu(estado: Estado) -> int:
        for i, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if carta in estado.jogador_atual.distritos_construidos:
                return i
        for i, carta in enumerate(estado.jogador_atual.cartas_distrito_mao):
            if carta.valor_do_distrito == 1:
                return i
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)
