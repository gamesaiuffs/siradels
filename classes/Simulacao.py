import Estado
import Jogador
import Tabuleiro

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
        #cada jogador recebe 2 cartas do deck
        
        #sortear jogador inicial que é o rei
        
        return Estado(tabuleiro, jogadores)

    def criar_jogadores_automatico(self) -> list(Jogador):
        #criar jogadores iniciais

    def distribuir_cartas_iniciais(self):
        #
#simulacao = Simulacao(....)#criar estado inicial que cria jogadores



                            