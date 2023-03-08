from Simulacao import Simulacao
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaPersonagem import CartaPersonagem

# Inicialização das variáveis esseciais
num_jogadores = 6
bots = True
jogador_finalizador = None  # primeiro a construir sete distritos
simulacao = Simulacao(num_jogadores, bots)
final_jogo = False

# Main Loop
while not final_jogo:
    # Cada jogador escolhe o seu personagem
    foi_escolhido = []
    for jogador in simulacao.estado.jogadores:
        print("---------| Personagens |--------")
        # "Printa" o baralho de personagens
        while jogador.personagem.rank == 0:
            print(jogador.nome)
            for personagem in simulacao.estado.tabuleiro.baralho_personagens:
                print(personagem)
            print("Escolha uma carta de personagem [Rank]: ", end="")
            rank_carta_escolhida = int(input())
            
            for index, carta_personagem in enumerate(simulacao.estado.tabuleiro.baralho_personagens):
                if carta_personagem.rank == rank_carta_escolhida:
                    jogador.personagem = simulacao.estado.tabuleiro.baralho_personagens.pop(index)
                    foi_escolhido.append(rank_carta_escolhida)
                    break
                if rank_carta_escolhida in foi_escolhido:
                    print("Escolha inválida")
                    break
            
    # Ordena os jogadores
    simulacao.estado.ordenar_jogadores()

    # Printar estad
    print(simulacao.estado)

    # Cada jogador faz suas ações
    for jogador in simulacao.estado.jogadores:
        
        # Atribui a flag rei ao jogador com o rei
        if jogador.personagem.rank == 4:
            for antigorei in simulacao.estado.jogadores:
                if antigorei.rei:
                    antigorei.rei = False
            jogador.rei = True
            
        if jogador.roubado:
            simulacao.estado.jogadores[1].ouro += jogador.ouro
            jogador.ouro = 0 
            
        fim_turno = False
        while not fim_turno:
            print(jogador.nome)
            print("Ações disponíveis: ")

            acoes = simulacao.acoes_disponiveis()
            for indexAcao, acao in enumerate(acoes):
                print(f"\t{indexAcao} - {acao.descricao}")

            acao_escolhida = int(input("Escolha uma ação: "))
            print()
            if acao_escolhida == -1:
                final_jogo = True
                break

            if 0 <= acao_escolhida < len(acoes):
                acoes[acao_escolhida].ativar(simulacao.estado)
            else:
                print("Escolha inválida")

            # Printar estad
            print(simulacao.estado)
            
            if jogador.acoes_realizadas[TipoAcao.PassarTurno.value] == 1:
                fim_turno = True

        if len(jogador.distritos_construidos) >= 7:
            jogador.terminou = True 
            if jogador_finalizador is None:
                jogador_finalizador = jogador



    # verificar final de jogo e atualizar flag
    simulacao.estado.tabuleiro.baralho_personagens = simulacao.estado.tabuleiro.criar_baralho_personagem(num_jogadores)
    simulacao.estado.turno = 1
    simulacao.estado.rodada += 1
    for jogador in simulacao.estado.jogadores:
        jogador.personagem = CartaPersonagem("Nenhum", 0)
    simulacao.estado.ordenar_jogadores_rei()
    

# contabilizar a pontuacao e verificar ponto


for jogador in simulacao.estado.jogadores:

    # +1 ponto pra cada moeada do valor de distrito
    soma_pontos = 0
    cont_pontos_distrito = 0
    for distrito in jogador.distritos_construidos:
        cont_pontos_distrito += distrito.valor_do_distrito
        soma_pontos += distrito.valor_do_distrito
    
    # +3 se tem um distrito de cada tipo
    tipos_distritos = [] 
    cont_pontos_tipos_distritos = 0
    num_dist_especiais = 0
    for distrito in jogador.distritos_construidos:
        if distrito.tipo_de_distrito not in tipos_distritos:
            tipos_distritos.append(distrito.tipo_de_distrito)
        if distrito.tipo_de_distrito == TipoDistrito.Especial:
            num_dist_especiais += 1

    if len(tipos_distritos) == TipoDistrito.Especial:
        cont_pontos_tipos_distritos = 3
        soma_pontos += 3

    # +4 pro primeiro q fechar 7 distritos 
    cont_pontos_finalizador = 0
    if jogador_finalizador == jogador:
        cont_pontos_finalizador = 4
        soma_pontos += 4

    # +2 pros outros q fecharam 7 distritos 
    cont_pontos_finalizador_segundo = 0
    if jogador_finalizador != jogador and jogador.terminou: 
        cont_pontos_finalizador_segundo = 2
        soma_pontos += 2

    # pontos extras de distritos especiais 
    cont_pontos_distritos_especiais = 0
    soma_pontos += 0 

    # cofre secreto (n pode ser construido) - revelar no final - +3 pontos
    for distrito in jogador.cartas_distrito_mao:
        if distrito.nome_do_distrito == 'cofre secreto':
            soma_pontos += 3
            cont_pontos_distritos_especiais += 3

    for distrito_construido in jogador.distritos_construidos:
        
        # tesouro imperial
        if distrito_construido.nome_do_distrito == 'tesouro imperial':
            soma_pontos += jogador.ouro
            cont_pontos_distritos_especiais += jogador.ouro

        # Portão do dragão
        elif distrito_construido.nome_do_distrito == 'portao do dragao':
            soma_pontos += 2
            cont_pontos_distritos_especiais += 2

        # bairro assombrado
        elif distrito_construido.nome_do_distrito == 'bairro_assombrado':
            if len(tipos_distritos) == 4 and num_dist_especiais > 1:
                soma_pontos += 3
                cont_pontos_distritos_especiais += 3

    print(f"\n\n{jogador.nome}\n\t"
          f"Pontos por valor de distrito: {cont_pontos_distrito}\n\t"
          f"Pontos por tipos de distritos: {cont_pontos_tipos_distritos}\n\t"
          f"Pontos por terminar primeiro: {cont_pontos_finalizador}\n\t"
          f"Pontos por terminar após o primeiro: {cont_pontos_finalizador_segundo}\n\t"
          f"Pontos por distritos especiais: {cont_pontos_distritos_especiais}\n\t"
          f"Pontuação total: {soma_pontos}")
