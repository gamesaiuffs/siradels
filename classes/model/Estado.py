# Imports
from more_itertools import sort_together
from classes.enum.TipoDistrito import TipoDistrito
from classes.model.Tabuleiro import Tabuleiro
from classes.model.Jogador import Jogador


class Estado:
    # Construtor
    def __init__(self, tabuleiro: Tabuleiro, jogadores: list[Jogador]):
        self.tabuleiro: Tabuleiro = tabuleiro
        self.jogadores: list[Jogador] = jogadores
        self.turno: int = 0
        self.rodada: int = 0
        self.jogador_atual: Jogador = None

    # To String
    def __str__(self):
        jogadores_print_str = ''
        for jogador in self.jogadores:
            jogadores_print_str += jogador.__str__()
            jogadores_print_str += '\n'
        return f'\nRODADA {self.rodada}\nTURNO {self.turno}\n\n' \
               f'Tabuleiro: {self.tabuleiro}\nJogadores: {jogadores_print_str}'

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
        self.jogadores = sort_together([ordem, self.jogadores], reverse=True)[1]

    def converter_estado(self) -> list:
        estado_vetor = []
        
        # Qtd ouro [0,1,2,3,4,5,>=6] = 56
        if self.jogador_atual.ouro >= 6:
            estado_vetor.append(6)
        else:
            estado_vetor.append(self.jogador_atual.ouro)
        
        # Qtd carta mão [0,1,2,3,4,>=5] = 48
        if len(self.jogador_atual.cartas_distrito_mao) >= 5:
            estado_vetor.append(5)
        else:
            estado_vetor.append(len(self.jogador_atual.cartas_distrito_mao))        
        
        # Carta mão mais cara [1 a 6] = 48
        # Carta mão mais barata [1 a 6] = 48
        maior_custo = 0
        menor_custo = 10
        for distrito in self.jogador_atual.cartas_distrito_mao:
            # descobre o distrito mais caro da mao
            if distrito.valor_do_distrito > maior_custo:
                maior_custo = distrito.valor_do_distrito
            # descobre o distrito mais barato da mao
            if distrito.valor_do_distrito < menor_custo:
                menor_custo = distrito.valor_do_distrito
        estado_vetor.append(maior_custo)
        estado_vetor.append(menor_custo)

        # Qtd distritos construido [0 a 6] = 56
        estado_vetor.append(len(self.jogador_atual.distritos_construidos))
        
        # Qtd distrito construido Militar [0,1,2,>=3] = 32
        # Qtd distrito construido Religioso [0,1,2,>=3] = 32
        # Qtd distrito construido Nobre [0,1,2,>=3] = 32
        nobre = 0
        religioso = 0
        militar = 0
        for distrito in self.jogador_atual.distritos_construidos:
            if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                nobre += 1
            if distrito.tipo_de_distrito == TipoDistrito.Religioso:
                religioso += 1
            if distrito.tipo_de_distrito == TipoDistrito.Militar:
                militar += 1      
        if nobre >= 3:
            estado_vetor.append(3)
        else:
            estado_vetor.append(nobre)
        if religioso >= 3:
            estado_vetor.append(3)
        else:
            estado_vetor.append(religioso)
        if militar >= 3:
            estado_vetor.append(3)
        else:
            estado_vetor.append(militar)

        # Qtd personagens disponíveis [2,3,4,5,6,7] = 48
        estado_vetor.append(len(self.tabuleiro.baralho_personagens))
        
        # Pontuacao [0-3,4-7,8-11,12-15,16-19,20-23,>=24] = 56
        if self.jogador_atual.pontuacao <= 3:
            estado_vetor.append(0)
        elif self.jogador_atual.pontuacao <= 7:
            estado_vetor.append(1)
        elif self.jogador_atual.pontuacao <= 11:
            estado_vetor.append(2)
        elif self.jogador_atual.pontuacao <= 15:
            estado_vetor.append(3)
        elif self.jogador_atual.pontuacao <= 19:
            estado_vetor.append(4)
        elif self.jogador_atual.pontuacao <= 23:
            estado_vetor.append(5)
        else:
            estado_vetor.append(6)
            
        # Qtd distrito construido [0 a 6] = 56
        maior_custo = 0
        for jogador in self.jogadores:
            if maior_custo < len(jogador.distritos_construidos):
                maior_custo = len(jogador.distritos_construidos)
        estado_vetor.append(maior_custo)
        
        # Qtd ouro [0,1,2,3,4,5,>=6] = 56
        maior_custo = 0
        for jogador in self.jogadores:
            if maior_custo < jogador.ouro:
                maior_custo = jogador.ouro
        if maior_custo >= 6:
            estado_vetor.append(6)
        else:
            estado_vetor.append(maior_custo)
        
        # Qtd carta mão [0,1,2,3,4,>=5] = 48
        maior_custo = 0
        for jogador in self.jogadores:
            if maior_custo < len(jogador.cartas_distrito_mao):
                maior_custo = len(jogador.cartas_distrito_mao)
        if maior_custo >= 5:
            estado_vetor.append(5)
        else:
            estado_vetor.append(maior_custo)
            
        # Personagem disponivel para escolha [1,2,3,4,5,6,7,8] = 510*8
        personagens = 0b0
        for carta in self.tabuleiro.baralho_personagens:
            if carta.rank == 1:
                personagens += 0b1
            if carta.rank == 2:
                personagens += 0b10
            if carta.rank == 3:
                personagens += 0b100
            if carta.rank == 4:
                personagens += 0b1000
            if carta.rank == 5:
                personagens += 0b10000
            if carta.rank == 6:
                personagens += 0b100000
            if carta.rank == 7:
                personagens += 0b1000000
            if carta.rank == 8:
                personagens += 0b10000000
        estado_vetor.append(int(personagens))

        # Quantidade de jogadores [4,5,6] = 24
        estado_vetor.append(len(self.jogadores))

        # Personagem visivel descartado [1,2,3,5,6,7,8] = 192(29 preenchidas)*8
        cartas_visiveis = 0b0
        for carta in self.tabuleiro.cartas_visiveis:
            if carta.rank == 1:
                cartas_visiveis += 0b1
            if carta.rank == 2:
                cartas_visiveis += 0b10
            if carta.rank == 3:
                cartas_visiveis += 0b100
            if carta.rank == 5:
                cartas_visiveis += 0b1000
            if carta.rank == 6:
                cartas_visiveis += 0b10000
            if carta.rank == 7:
                cartas_visiveis += 0b100000
            if carta.rank == 8:
                cartas_visiveis += 0b1000000
        estado_vetor.append(int(cartas_visiveis))

        return estado_vetor
        