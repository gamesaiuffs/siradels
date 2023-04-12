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

    # Printar estado
    print(simulacao.estado)

    # Cada jogador faz as suas ações
    for jogador in simulacao.estado.jogadores:
        # Aplica habilidades/efeitos de início de turno

        # Aplica habilidade da Assassina
        if jogador.morto:
            continue
        # Aplica habilidade do Ladrão
        if jogador.roubado:
            for ladrao in simulacao.estado.jogadores:
                if ladrao.personagem.nome == "Ladrão":
                    ladrao.ouro += jogador.ouro
                    jogador.ouro = 0
                    break
        # Aplica habilidade passiva do Rei
        if jogador.personagem.nome == "Rei":
            for antigorei in simulacao.estado.jogadores:
                antigorei.rei = False
            jogador.rei = True

        # inicia turno do jogador
        while True:
            # Printar estado
            print(simulacao.estado)

            print(jogador.nome)
            # Mostra apenas ações disponíveis segundo regras do jogo
            print("Ações disponíveis: ")
            acoes = simulacao.acoes_disponiveis()
            for indexAcao, acao in enumerate(acoes):
                print(f"\t{indexAcao} - {acao.descricao}")

            while True:
                escolha = input("Escolha sua ação: ")
                try:
                    escolha = int(escolha)
                except ValueError:
                    print("Escolha inválida.")
                    continue
                if not 0 <= escolha < len(acoes):
                    print("Escolha inválida.")
                    continue
                break
            # Pula uma linha
            print()

            # Executa ação escolhida
            acoes[escolha].ativar(simulacao.estado)
            
            if jogador.acoes_realizadas[TipoAcao.PassarTurno.value]:
                break
        # Identifica se o jogador construiu o Monumento
        monumento = False
        for construido in jogador.distritos_construidos:
            if construido.nome_do_distrito == 'Monumento':
                monumento = True
                break
        # Marca fim de jogo e jogador finalizador (monumento conta como 2 distritos para fins de uma cidade completa)
        if len(jogador.distritos_construidos) >= 7 or (len(jogador.distritos_construidos) == 6 and monumento):
            jogador.terminou = True 
            if jogador_finalizador is None:
                jogador_finalizador = jogador

    # Preparação para nova rodada
    simulacao.estado.tabuleiro.baralho_personagens = simulacao.estado.tabuleiro.criar_baralho_personagem(num_jogadores)
    simulacao.estado.turno = 1
    simulacao.estado.rodada += 1
    for jogador in simulacao.estado.jogadores:
        jogador.personagem = CartaPersonagem("Nenhum", 0)
        jogador.acoes_realizadas[TipoAcao.PassarTurno.value] = False
    simulacao.estado.ordenar_jogadores_rei()
    

simulacao.computar_pontuacao_final()
for jogador in simulacao.estado.jogadores:
    print(f"\n\n{jogador.nome}\n\t"
          f"Pontuação total: {jogador.pontuacao_final}")
