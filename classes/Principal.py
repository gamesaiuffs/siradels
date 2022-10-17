# Imports
from Simulacao import Simulacao

# Inicialização das variáveis esseciais
num_jogadores = 6
bots = True
simulacao = Simulacao(num_jogadores, bots)
final_jogo = False

# Main Loop
while not final_jogo:
    # Cada jogador escolhe seu personagem
    foi_escolhido = []
    for jogador in simulacao.estado.jogadores:
        print("---------| Personagens |---------")
        # "Printa" o baralho de personagens

        while len(jogador.personagem) == 0:
            print(jogador.nome)
            for personagem in simulacao.estado.tabuleiro.baralho_personagens:
                print(personagem)
            print("Escolha uma carta de personagem [Rank]: ", end="")
            rank_carta_escolhida = int(input())
            
            for index, carta_personagem in enumerate(simulacao.estado.tabuleiro.baralho_personagens):
                if carta_personagem.rank == rank_carta_escolhida:
                    jogador.personagem.append(simulacao.estado.tabuleiro.baralho_personagens.pop(index))
                    foi_escolhido.append(rank_carta_escolhida)
                    break
                if rank_carta_escolhida in foi_escolhido:
                    print("Escolha inválida")
                    break
            
    # Ordena os jogadores
    simulacao.estado.ordenar_jogadores()
    # Cada jogador faz suas ações
    for jogador in simulacao.estado.jogadores:
        fim_turno = False
        while not fim_turno:
            print("Escolha uma ação")
            print("Ações disponíveis: ")
            # [...]
            acao_escolhida = input()

    # verificar final de jogo e atualizar flag
    simulacao.estado.tabuleiro.baralho_personagens = simulacao.estado.tabuleiro.criar_baralho_personagem(num_jogadores)

# contabilizar a pontuacao e verificar ponto
