# Imports
from Simulacao import Simulacao

# Inicialização das variáveis esseciais
num_jogadores = 6
simulacao = Simulacao(num_jogadores, True)
final_jogo = False

# Main Loop
while not final_jogo:
    # Cada jogador escolhe seu personagem
    for jogador in simulacao.estado.jogadores:
        print("---------| Personagens |---------")
        print("Escolha uma carta de personagem: ")
        # "Printa" o baralho de personagens
        for personagem in simulacao.estado.tabuleiro.baralho_personagens:
            print(personagem)

        print("Escolha uma ação: ")
        carta_escolhida = input()
        jogador.personagem.append(simulacao.estado.tabuleiro.baralho_personagens.pop([carta_escolhida]))
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
