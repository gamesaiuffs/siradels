import Estado
from Jogador import Jogador
import Tabuleiro
from random import shuffle

class Simulacao:
    def __init__(self, num_jogadores: int, automatico: bool):
        self.estado = self.criar_estado_inicial(automatico)
        self.num_jogadores = num_jogadores

    def criar_estado_inicial(self, automatico) -> Estado:
        tabuleiro = Tabuleiro(self.num_jogadores)
        if automatico:
            jogadores = self.criar_jogadores_automatico()
        else:
            jogadores = self.criar_jogadores_manual()

        #distribuir cartas iniciais
            #cada jogador recebe 4 cartas do deck
        for jogador in jogadores:
            jogador.cartas_distrito_na_mao.append(tabuleiro.baralho_de_distritos[0:4])
            del tabuleiro.baralho_de_distritos[0:4]
        
        #sortear jogador inicial que é o rei
        shuffle(jogadores)
        jogadores[0].eh_o_rei = True
        
        return Estado(tabuleiro, jogadores)

    def criar_jogadores_automatico(self) -> list(Jogador):
        #criar jogadores iniciais
        lista_jogadores = []
        for jogador in self.num_jogadores:
            lista_jogadores.append(Jogador(f"Bot {jogador+1}"))
        
        return lista_jogadores
    
    def criar_jogadores_manual(self) -> list(Jogador):
        #criar jogadores iniciais:
        lista_jogadores = []
        for jogador in self.num_jogadores:
            nome_jogador = input()
            lista_jogadores.append(Jogador(nome_jogador))

        return lista_jogadores





                            