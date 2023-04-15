# Imports
from classes.enum.TipoDistrito import TipoDistrito
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from random import shuffle


class Tabuleiro:
    # Construtor
    def __init__(self, num_personagens: int):
        # Define o número de personagens (8 ou 9)
        self.num_personagens = num_personagens
        self.cartas_visiveis = []
        self.cartas_nao_visiveis = []
        self.baralho_personagens = []
        self.baralho_distritos = []
        self.criar_baralho_distritos()

    # To String
    def __str__(self):
        texto_baralho = "Nenhuma carta!" if len(self.baralho_distritos) == 0 else ""
        for carta in self.baralho_distritos:
            texto_baralho += carta.__str__() + " | "
        texto_cartas_visiveis = "Nenhuma carta!" if len(self.cartas_visiveis) == 0 else ""
        for carta in self.cartas_visiveis:
            texto_cartas_visiveis += carta.__str__() + " | "
        texto_cartas_n_visiveis = "Nenhuma carta!" if len(self.cartas_nao_visiveis) == 0 else ""
        for carta in self.cartas_nao_visiveis:
            texto_cartas_n_visiveis += carta.__str__() + " | "
        texto_personagens = ""
        for carta in self.baralho_personagens:
            texto_personagens += carta.__str__() + " | "
        return f"\nBaralho: {texto_baralho}" \
               f"\nCartas visiveis: {texto_cartas_visiveis}" \
               f"\nCartas não visiveis: {texto_cartas_n_visiveis}" \
               f"\nPersonagens que sobraram: {texto_personagens}\n"

    # Cria baralho com as cartas dos personagens
    # Não foram implementados os demais personagens (necessitará de adaptação para incluí-los)
    def criar_baralho_personagem(self, num_jogadores):
        assassina = CartaPersonagem("Assassina", 1, "Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno")
        ladrao = CartaPersonagem(
            "Ladrão", 2, "Anuncie um personagem que você deseja roubar. Quando o personagem roubado for revelado, você pega todo o ouro dele")
        mago = CartaPersonagem(
            "Mago", 3, "Olhe a mão de outro jogador e escolha 1 carta. Pague para construí-la imediatamente ou adicione-a à sua mão. "
                       "Você pode construir distritos idênticos.")
        rei = CartaPersonagem("Rei", 4, "Pegue a coroa. Ganhe 1 ouro para cada um dos seus distritos NOBRES.")
        cardeal = CartaPersonagem(
            "Cardeal", 5, "Se você não tiver ouro suficiente para construir um distrito, troque suas cartas pelo ouro de outro jogador (1 carta: 1 ouro). "
                          "Ganhe 1 carta para cada um dos seus distritos RELIGIOSOS.")
        alquimista = CartaPersonagem(
            "Alquimista", 6, "Ao final do seu turno, você pega de volta todo o ouro pago para construir distritos neste turno. "
                             "Você não pode pagar mais ouro do que tem.")
        navegadora = CartaPersonagem("Navegadora", 7, "Ganhe 4 ouros extras ou 4 cartas extras. Você não pode construir distritos.")
        senhor_guerra = CartaPersonagem(
            "Senhor da Guerra", 8, "Destrua 1 distrito, pagando 1 ouro a menos que o custo dele. Ganhe 1 ouro para cada um dos seus distritos MILITARES")
        # Coloca os personagens numa lista e os embaralha (com exceção do rei que será colocado depois)
        mao_jogador = [assassina, ladrao, mago, cardeal, alquimista, navegadora, senhor_guerra]
        shuffle(mao_jogador)
        # Regras específicas para o baralho de personagens de acordo com número d ejogadores
        if num_jogadores == 4:
            # Duas cartas viradas para cima e uma para baixo
            self.cartas_visiveis.append(mao_jogador.pop(0))
            self.cartas_visiveis.append(mao_jogador.pop(0))
            self.cartas_nao_visiveis.append(mao_jogador.pop(0))
        elif num_jogadores == 5:
            # Uma carta virada para cima e uma para baixo
            self.cartas_visiveis.append(mao_jogador.pop(0))
            self.cartas_nao_visiveis.append(mao_jogador.pop(0))
        elif num_jogadores == 6:
            # Uma carta virada para baixo
            self.cartas_nao_visiveis.append(mao_jogador.pop(0))
        # Coloca o rei na lista de personagens (nunca deve ser descartado)
        mao_jogador.append(rei)
        self.baralho_personagens = mao_jogador

        # Cria baralho com as cartas de distritos
    def criar_baralho_distritos(self):
        #  Instância os distritos básicos
        baralho = [CartaDistrito(1, TipoDistrito.Religioso, 'Templo', 3),
                   CartaDistrito(2, TipoDistrito.Religioso, 'Igreja', 3),
                   CartaDistrito(3, TipoDistrito.Religioso, 'Mosteiro', 3),
                   CartaDistrito(5, TipoDistrito.Religioso, 'Catedral', 2),
                   CartaDistrito(1, TipoDistrito.Militar, 'Torre de Vigia', 3),
                   CartaDistrito(2, TipoDistrito.Militar, 'Prisão', 3),
                   CartaDistrito(3, TipoDistrito.Militar, 'Caserna', 3),
                   CartaDistrito(5, TipoDistrito.Militar, 'Fortaleza', 2),
                   CartaDistrito(3, TipoDistrito.Nobre, 'Solar', 5),
                   CartaDistrito(4, TipoDistrito.Nobre, 'Castelo', 4),
                   CartaDistrito(5, TipoDistrito.Nobre, 'Palácio', 3),
                   CartaDistrito(1, TipoDistrito.Comercial, 'Taverna', 5),
                   CartaDistrito(2, TipoDistrito.Comercial, 'Mercado', 4),
                   CartaDistrito(2, TipoDistrito.Comercial, 'Posto de Comércio', 3),
                   CartaDistrito(3, TipoDistrito.Comercial, 'Docas', 3),
                   CartaDistrito(4, TipoDistrito.Comercial, 'Porto', 3),
                   CartaDistrito(5, TipoDistrito.Comercial, 'Prefeitura', 2)]
        # Criando duplicatas dos distritos básicos conforme quantidade
        aux = []
        for carta in baralho:
            qtd = 1
            while qtd < carta.quantidade:
                aux.append(carta)
                qtd += 1
        baralho.extend(aux)
        # Instância os distritos especiais
        especiais = [CartaDistrito(0, TipoDistrito.Especial, 'Cofre Secreto', 1,
                                   "O Cofre não pode ser contruído. Ao final da partida, revele o Cofre Secreto da sua mão para marcar 3 pontos extras."),
                     CartaDistrito(2, TipoDistrito.Especial, 'Bairro Assombrado', 1,
                                   "Ao final da partida, o Bairro Assombrado vale como 1 tipo de distrito à sua escolha."),
                     CartaDistrito(2, TipoDistrito.Especial, 'Estábulos', 1,
                                   "A construção dos Estábulos não conta para o seu limite de construção neste turno."),
                     CartaDistrito(3, TipoDistrito.Especial, 'Estrutura', 1,
                                   "Você pode cosntruir um distrito destruindo a Estrutura, em vez de pagar os custos do distrito em questão."),
                     CartaDistrito(3, TipoDistrito.Especial, 'Arsenal', 1,
                                   "No seu turno, destrua o Arsenal para destruir 1 distrito à sua escolha."),
                     CartaDistrito(3, TipoDistrito.Especial, 'Torre de Menagem', 1,
                                   "O personagem de ranque 8 não pode usar a habilidade dele contra a Torre de Menagem."),
                     CartaDistrito(3, TipoDistrito.Especial, 'Estátua', 1,
                                   "Se você tiver a coroa no final da partida, marque 5 pontos extras."),
                     CartaDistrito(4, TipoDistrito.Especial, 'Monumento', 1,
                                   "Você não pode construir o Monumento se tiver 5 ou mais distritos na sua cidade. "
                                   "Considere o Monumento como 2 distritos para fins de uma cidade completa."),
                     CartaDistrito(4, TipoDistrito.Especial, 'Abrigo para Pobres', 1,
                                   "Se não houver ouro no seu tesouro no fim do seu turno, ganhe 1 ouro."),
                     CartaDistrito(4, TipoDistrito.Especial, 'Observatório', 1,
                                   "Se você optou por comprar cartas ao coletar recursos, compre 3 cartas em vez de 2."),
                     CartaDistrito(4, TipoDistrito.Especial, 'Museu', 1,
                                   "Uma vez por turno, coloque 1 carta da sua mão, voltada para baixo, sob o museu. "
                                   "Ao final da partida, marque 1 ponto extra para cada carta sob o Museu."),
                     CartaDistrito(4, TipoDistrito.Especial, 'Basílica', 1,
                                   "Ao final da partida, marque 1 ponto extra para cada distrito especial na sua cidade que tenha um número ímpar como custo."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Fábrica', 1,
                                   "Você paga 1 ouro a menos para construir qualquer outro distrito ESPECIAL."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Pedreira', 1,
                                   "Você pode construir distritos que são idênticos a distritos em sua cidade."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Poço dos Desejos', 1,
                                   "Ao final da partida, marque 1 ponto extra para cada distrito ESPECIAL "
                                   "na sua cidade (incluindo o Poço dos Desejos)."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Forja', 1,
                                   "Uma vez por turno, pague 2 ouros para receber 3 cartas."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Necrópole', 1,
                                   "Você pode construir a Necrópole destruindo 1 distrito na sua cidade, em vez de pagar o custo da Necrópole."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Tesouro Imperial', 1,
                                   "Ao final da partida, marque 1 ponto extra para cada ouro em seu tesouro."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Laboratório', 1,
                                   "Uma vez por turno, descarte 1 carta da sua mão para ganahr 2 ouros."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Sala de Mapas', 1,
                                   "Ao final da partida, marque 1 ponto extra para cada carta na sua mão."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Torre de Marfim', 1,
                                   "Se a Torre de Marfim for o único distrito ESPECIAL na sua cidade ao final da partida, marque 5 pontos extras."),
                     CartaDistrito(5, TipoDistrito.Especial, 'Capitólio', 1,
                                   "Se você tiver pelo menos 3 distritos do mesmo tipo no final da partida, marque 3 pontos extras."),
                     CartaDistrito(6, TipoDistrito.Especial, 'Portão do Dragão', 1,
                                   "Ao final da partida, marque 2 pontos extras."),
                     # Teatro não foi implementado
                     # CartaDistrito(6, TipoDistrito.Especial, 'Teatro', 1,
                     #  "Ao final de cada fase de escolha, você pode trocar a sua carta de personagem escolhida com a carta de personagem de um oponente."),
                     CartaDistrito(6, TipoDistrito.Especial, 'Muralha', 1,
                                   "O personagem de ranque 8 deve pagar 1 ouro a mais para usar a habilidade "
                                   "dele contra qualquer outro distrito na sua cidade."),
                     CartaDistrito(6, TipoDistrito.Especial, 'Mina de Ouro', 1,
                                   "Se você optar por ganhar ouro ao coletar recursos, ganhe 1 ouro extra."),
                     CartaDistrito(6, TipoDistrito.Especial, 'Covil dos Ladrões', 1,
                                   "Pague parte ou todo o custo do Covil dos Ladrões com cartas da sua mão, em vez de  ouro, a uma taxa de 1 carta: 1 ouro."),
                     CartaDistrito(6, TipoDistrito.Especial, 'Escola de Magia', 1,
                                   "Ao usar habilidades que obtêm recursos pelos seus distritos, "
                                   "a Escola de Magia vale como o tipo de distrito à sua escolha."),
                     CartaDistrito(6, TipoDistrito.Especial, 'Biblioteca', 1,
                                   "Se você optar por comprar cartas ao coletar recursos, mantenha todas elas em sua mão."),
                     CartaDistrito(6, TipoDistrito.Especial, 'Parque', 1,
                                   "Se não houver cartas na sua mão no fim do seu turno, ganhe 2 cartas.")]
        # Selecionar 14 cartas de distritos especiais aleatoriamente
        #shuffle(especiais)
        #baralho.extend(especiais[0:14])
        especiais.extend(baralho)
        # Embaralhar baralho final
        #shuffle(baralho)
        self.baralho_distritos = especiais
