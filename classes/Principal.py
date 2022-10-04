from classes.Simulacao import Simulacao

num_jogadores = 7
simulacao = Simulacao(num_jogadores, False)
final_jogo = False
while not final_jogo:
    for jogador in simulacao.estado.jogadores:
        print("Escolha uma carta de personagem")
        print(simulacao.estado.tabuleiro.baralho_de_personagens)
        carta_escolhida = input()
        jogador.carta_personagem.append(simulacao.estado.tabuleiro.baralho_de_personagens.pop([carta_escolhida]))

    simulacao.estado.ordenar_jogadores()
    for jogador in simulacao.estado.jogadores:
        fim_turno = False
        while not fim_turno:
            print("Escolha uma ação")
            print("Ações disponíveis...")
            acao_escolhida = input()
    # verificar final de jogo e atualizar flag
    simulacao.estado.tabuleiro.criar_baralho_personagem(num_jogadores)

# contabilizar a pontuacao e verificar ponto
