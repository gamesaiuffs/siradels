# Imports
from classes.enum.TipoDistrito import TipoDistrito
from classes.enum.TipoPersonagem import TipoPersonagem
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from random import shuffle
from more_itertools import sort_together


class Tabuleiro:
    # Construtor
    def __init__(self, num_personagens: int):
        # Define o número de personagens (8 ou 9)
        self.num_personagens: int = num_personagens
        self.cartas_visiveis: list[CartaPersonagem] = []
        self.cartas_nao_visiveis: list[CartaPersonagem] = []
        self.baralho_personagens: list[CartaPersonagem] = []
        self.personagens: list[CartaPersonagem] = self.criar_personagens()
        self.baralho_distritos: list[CartaDistrito] = []
        self.criar_baralho_distritos()

    # To String
    def __str__(self):
        texto_baralho = 'Nenhuma carta!' if len(self.baralho_distritos) == 0 else ''
        for carta in self.baralho_distritos:
            texto_baralho += carta.__str__() + ' | '
        texto_cartas_visiveis = 'Nenhuma carta!' if len(self.cartas_visiveis) == 0 else ''
        for carta in self.cartas_visiveis:
            texto_cartas_visiveis += carta.__str__() + ' | '
        texto_cartas_n_visiveis = 'Nenhuma carta!' if len(self.cartas_nao_visiveis) == 0 else ''
        for carta in self.cartas_nao_visiveis:
            texto_cartas_n_visiveis += carta.__str__() + ' | '
        texto_personagens = ''
        for carta in self.baralho_personagens:
            texto_personagens += carta.__str__() + ' | '
        return f'\nBaralho: {texto_baralho}' \
               f'\nCartas visiveis: {texto_cartas_visiveis}' \
               f'\nCartas não visiveis: {texto_cartas_n_visiveis}' \
               f'\nPersonagens que sobraram: {texto_personagens}\n'

    # Cria baralho com as cartas dos personagens
    # Não foram implementados os demais personagens (necessitará de adaptação para incluí-los)
    @staticmethod
    def criar_personagens() -> list[CartaPersonagem]:
        assassina = CartaPersonagem('Assassina', 1, TipoPersonagem.Assassina,
                                    'Anuncie um personagem que você deseja assassinar. O personagem assassinado perde o turno.')
        ladrao = CartaPersonagem('Ladrão', 2, TipoPersonagem.Ladrao,
                                 'Anuncie um personagem que você deseja roubar. Quando o personagem roubado for revelado, você pega todo o ouro dele.')
        ilusionista = CartaPersonagem('Ilusionista', 3, TipoPersonagem.Ilusionista,
                                      'Troque sua mão com a de outro jogador ou descarte quantas cartas quiser para ganhar um número igual de cartas.')
        rei = CartaPersonagem('Rei', 4, TipoPersonagem.Rei, 'Pegue a coroa. Ganhe 1 ouro para cada um dos seus distritos NOBRES.')
        bispo = CartaPersonagem('Bispo', 5, TipoPersonagem.Bispo,
                                'O personagem de ranque 8 não pode usar a habilidade dele nos seus distritos.'
                                'Ganhe 1 ouro para cada um dos seus distritos RELIGIOSOS.')
        comerciante = CartaPersonagem('Comerciante', 6, TipoPersonagem.Comerciante,
                                      'Ganhe 1 ouro extra. Ganhe 1 ouro para cada um dos seus distritos COMERCIAIS.')
        arquiteta = CartaPersonagem('Arquiteta', 7, TipoPersonagem.Arquiteta, 'Ganhe 2 cartas extras. Você pode construir até 3 distritos.')
        senhor_guerra = CartaPersonagem('Senhor da Guerra', 8, TipoPersonagem.SenhorDaGuerra,
                                        'Destrua 1 distrito, pagando 1 ouro a menos que o custo dele. Ganhe 1 ouro para cada um dos seus distritos MILITARES')
        return [rei, assassina, ladrao, ilusionista, bispo, comerciante, arquiteta, senhor_guerra]

    def criar_baralho_personagem(self, num_jogadores):
        mao_jogador = self.personagens[1:]
        # O rei sempre fica disponível (fora do embaralhamento)
        rei = self.personagens[0]
        shuffle(mao_jogador)
        # Regras específicas para o baralho de personagens de acordo com número de jogadores
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
        self.ordenar_baralho_personagem()

    # Reorganiza as cartas de personagem conforme o rank
    def ordenar_baralho_personagem(self):
        ordem = [personagem.rank for personagem in self.baralho_personagens]
        self.baralho_personagens = list(sort_together([ordem, self.baralho_personagens])[1])

    # Cria baralho com as cartas de distritos
    def criar_baralho_distritos(self):
        #  Instância os distritos básicos
        baralho = [CartaDistrito(0, 1, TipoDistrito.Religioso, 'Templo', 3),
                   CartaDistrito(1, 2, TipoDistrito.Religioso, 'Igreja', 3),
                   CartaDistrito(2, 3, TipoDistrito.Religioso, 'Mosteiro', 3),
                   CartaDistrito(3, 5, TipoDistrito.Religioso, 'Catedral', 2),
                   CartaDistrito(4, 1, TipoDistrito.Militar, 'Torre de Vigia', 3),
                   CartaDistrito(5, 2, TipoDistrito.Militar, 'Prisão', 3),
                   CartaDistrito(6, 3, TipoDistrito.Militar, 'Caserna', 3),
                   CartaDistrito(7, 5, TipoDistrito.Militar, 'Fortaleza', 2),
                   CartaDistrito(8, 3, TipoDistrito.Nobre, 'Solar', 5),
                   CartaDistrito(9, 4, TipoDistrito.Nobre, 'Castelo', 4),
                   CartaDistrito(10, 5, TipoDistrito.Nobre, 'Palácio', 3),
                   CartaDistrito(11, 1, TipoDistrito.Comercial, 'Taverna', 5),
                   CartaDistrito(12, 2, TipoDistrito.Comercial, 'Mercado', 4),
                   CartaDistrito(13, 2, TipoDistrito.Comercial, 'Posto de Comércio', 3),
                   CartaDistrito(14, 3, TipoDistrito.Comercial, 'Docas', 3),
                   CartaDistrito(15, 4, TipoDistrito.Comercial, 'Porto', 3),
                   CartaDistrito(16, 5, TipoDistrito.Comercial, 'Prefeitura', 2)]
        # Criando duplicatas dos distritos básicos conforme quantidade
        aux = []
        for carta in baralho:
            qtd = 1
            while qtd < carta.quantidade:
                aux.append(carta)
                qtd += 1
        baralho.extend(aux)
        # Instância os distritos especiais
        especiais = [CartaDistrito(17, 2, TipoDistrito.Especial, 'Bairro Assombrado', 1,
                                   'Ao final da partida, o Bairro Assombrado vale como 1 tipo de distrito à sua escolha.'),
                     CartaDistrito(18, 3, TipoDistrito.Especial, 'Torre de Menagem', 1,
                                   'O personagem de ranque 8 não pode usar a habilidade dele contra a Torre de Menagem.'),
                     CartaDistrito(19, 3, TipoDistrito.Especial, 'Estátua', 1,
                                   'Se você tiver a coroa no final da partida, marque 5 pontos extras.'),
                     CartaDistrito(20, 5, TipoDistrito.Especial, 'Fábrica', 1,
                                   'Você paga 1 ouro a menos para construir qualquer outro distrito ESPECIAL.'),
                     CartaDistrito(21, 5, TipoDistrito.Especial, 'Pedreira', 1,
                                   'Você pode construir distritos que são idênticos a distritos em sua cidade.'),
                     CartaDistrito(22, 5, TipoDistrito.Especial, 'Poço dos Desejos', 1,
                                   'Ao final da partida, marque 1 ponto extra para cada distrito ESPECIAL '
                                   'na sua cidade (incluindo o Poço dos Desejos).'),
                     CartaDistrito(23, 5, TipoDistrito.Especial, 'Forja', 1,
                                   'Uma vez por turno, pague 2 ouros para receber 3 cartas.'),
                     CartaDistrito(24, 5, TipoDistrito.Especial, 'Tesouro Imperial', 1,
                                   'Ao final da partida, marque 1 ponto extra para cada ouro em seu tesouro.'),
                     CartaDistrito(25, 5, TipoDistrito.Especial, 'Laboratório', 1,
                                   'Uma vez por turno, descarte 1 carta da sua mão para ganhar 2 ouros.'),
                     CartaDistrito(26, 5, TipoDistrito.Especial, 'Sala de Mapas', 1,
                                   'Ao final da partida, marque 1 ponto extra para cada carta na sua mão.'),
                     CartaDistrito(27, 6, TipoDistrito.Especial, 'Portão do Dragão', 1,
                                   'Ao final da partida, marque 2 pontos extras.'),
                     CartaDistrito(28, 6, TipoDistrito.Especial, 'Covil dos Ladrões', 1,
                                   'Pague parte ou todo o custo do Covil dos Ladrões com cartas da sua mão, em vez de  ouro, a uma taxa de 1 carta: 1 ouro.'),
                     CartaDistrito(29, 6, TipoDistrito.Especial, 'Escola de Magia', 1,
                                   'Ao usar habilidades que obtêm recursos pelos seus distritos, '
                                   'a Escola de Magia vale como o tipo de distrito à sua escolha.'),
                     CartaDistrito(30, 6, TipoDistrito.Especial, 'Biblioteca', 1,
                                   'Se você optar por comprar cartas ao coletar recursos, mantenha todas elas em sua mão.')]
        baralho.extend(especiais)
        # Embaralhar baralho final
        shuffle(baralho)
        self.baralho_distritos = baralho
