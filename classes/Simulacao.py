import Estado
import Jogador
import Tabuleiro

class Simulacao:
    def __init__(self, num_jogadores: int, automatico: bool):
        self.estado = self.criar_estado_inicial() 

    def criar_estado_inicial() -> Estado:
        tabuleiro = Tabuleiro(num_jogadores)
        if automatico:
            jogadores = criar_jogadores_automatico()
        else:
            jogadores = criar_jogadores_manual()

        #distribuir cartas iniciais
        #cada jogador recebe 2 cartas do deck
        
        #sortear jogador inicial que é o rei
        
        return Estado(tabuleiro, jogadores)

    def criar_jogadores(num_jogadores:int) -> list(Jogador):
        #todo
        #criar jogadores iniciais

    def criar_tabuleiro() -> Tabuleiro:
        #todo

    def distribuir_cartas_iniciais()

#simulacao = Simulacao(....)#criar estado inicial que cria jogadores



                            