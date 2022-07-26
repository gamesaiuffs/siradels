from random import shuffle
from enum import Enum


class Players:
    def __init__(self, score, name, player_card, gold, hand, districts, order, king):
        self.score = score 
        self.name = name 
        self.player_card = player_card
        self.gold = gold
        self.hand = hand
        self.districts = districts
        self.order = order 
        self.king = king

    def __str__(self):
        return print("score: ", self.score, \
            "name: ", self.name, \
            "Player_card: ", self.player_card, "Gold: ", self.gold, \
            "hand: ", self.hand, \
            "districts: ", self.districts, \
            "order: ", self.order, \
            "king: ", self.king)

class Board:
    def __init__(self, deck, turn, stage, characters):  
        self.deck = deck 
        self.turn = turn 
        self.stage = stage 
        self.characters = characters

    def __str__(self):
        return f"deck: {self.deck}, turn: {self.turn} stage: {self.stage} characters:  {self.characters}"

class State:
    def __init__(self, board, players):
        self.board = board 
        self.players = players

    def __str__(self):
        return print("Board: ", self.board, \
            "Players: ", self.players)


class TipoDistrito(Enum): 

    Religioso = 1
    Militar= 2
    Nobre = 3
    Comercio = 4
    Especial=5

# print(tipoDistrito.Religioso.value) // para referencia de como usa

class CartaDeDistrito:
    def __init__(self, valor_do_distrito, tipo_de_distrito, nome_do_distrito, efeito_do_distrito,qtd_distrito):
        self.valor_do_distrito = valor_do_distrito 
        self.tipo_de_distrito= tipo_de_distrito #ou é TipoDistrito só?
        self.nome_do_distrito = nome_do_distrito 
        self.efeito_do_distrito = efeito_do_distrito 
        self.qtd_distrito=qtd_distrito


    def __str__(self): #colocar em uma string só com o format pra printar
        return print(f"Valor: ", self.valor_do_distrito, \
            "Tipo distrito: ", self.tipo_de_distrito, \
            "Nome: ",self.nome_do_distrito, \
            "Efeito: ", self.efeito_do_distrito)

class CharacterCard:
    def __init__(self, name, effect, rank, skill):
        self.name = name 
        self.effect = effect 
        self.rank = rank
        self.skill = skill

    def __str__(self):
        print("name: ", self.name, \
            "effect: ", self.effect, 
            "rank: ", self.rank,\
            "skill: ", self.skill)

def criar_baralho():
    mercado = CartaDeDistrito(2, TipoDistrito.Comercio, 'mercado', None,4)
    taverna = CartaDeDistrito(1, TipoDistrito.Comercio, 'taverna', None,5)
    prefeitura=CartaDeDistrito(5,TipoDistrito.Comercio,'prefeitura',None,2)
    porto=CartaDeDistrito(4,TipoDistrito.Comercio,'porto',None,3)
    docas=CartaDeDistrito(3,TipoDistrito.Comercio,'docas',None,3)
    posto_de_comercio=CartaDeDistrito(2,TipoDistrito.Comercio,'posto de comercio',None,3)




    torre_de_vigia = CartaDeDistrito(1, TipoDistrito.Militar, 'torre de vigia', None,3)
    prisao = CartaDeDistrito(2, TipoDistrito.Militar, 'prisao',None,3)
    caserna = CartaDeDistrito(3,TipoDistrito.Militar, 'barracos',None,3)
    fortaleza = CartaDeDistrito(5,TipoDistrito.Militar,'fortaleza',None,2)

    templo=CartaDeDistrito(1,TipoDistrito.Religioso,'templo',None,3)
    mosteiro=CartaDeDistrito(3,TipoDistrito.Religioso,'mosteiro',None,3)
    catedral=CartaDeDistrito(5,TipoDistrito.Religioso,'catedral',None,2)
    igreja=CartaDeDistrito(2,TipoDistrito.Religioso,'igreja',None,3)

    #nobre
    solar = CartaDeDistrito(3,TipoDistrito.Nobre,'solar',None,5)
    castelo=CartaDeDistrito(4,TipoDistrito.Nobre,'castelo',None,4)
    palacio = CartaDeDistrito(5, TipoDistrito.Nobre, 'palacio', None,3)


    # //especiais
    portao_do_dragao=CartaDeDistrito(6,TipoDistrito.Especial,'portao do dragao',None,1)#ao final da partida marque 2 pontos extras
    bairro_assombrado=CartaDeDistrito(2,TipoDistrito.Especial,'bairro_assombrado',None,1)#ao final da partida,vale com 1 tipo de distrito à sua escolha
    estabulos=CartaDeDistrito(2,TipoDistrito.Especial,'estabulos',None,1)#a construcao dos estabulos nao conta para o seu limite de construcao para este turno
    teatro=CartaDeDistrito(6,TipoDistrito.Especial,'teatro',None,1)#ao final de cada fase de escolha,vc pode trocar sua carta de personagem escolhida com a carta de personagem de um oponente
    estrutura=CartaDeDistrito(3,TipoDistrito.Especial,'estrutura',None,1)#vc pode construir um distrito destruindo a estrutura,em vez de pagar os custos do distrito em questao
    abrigo_para_pobres=CartaDeDistrito(4,TipoDistrito.Especial,'abrigo para pobres',None,1)#se nao houver ouro no seu tesouro no fim do seu turno,ganhe 1 ouro
    mina_de_ouro=CartaDeDistrito(6,TipoDistrito.Especial,'mina de ouro',None,1)#se vc optar por ganhar ouro ao coletar recursos,ganhe 1 ouro extra
    covil_dos_ladroes=CartaDeDistrito(6,TipoDistrito.Especial,'covil dos ladroes',None,1)#pague parte ou todo o custo do covil dos ladroes com cartas de sua mao,em vez de ouro,a uma taxa de uma carta:um ouro
    laboratorio=CartaDeDistrito(5,TipoDistrito.Especial,'laboratorio',None,1)#uma vez por turno,decarte uma carta de sua mao para ganhar 2 ouros
    necropole=CartaDeDistrito(5,TipoDistrito.Especial,'necropole',None,1)#voce pode consturir a necropole destruindo um distrito na sua cidade,ao invez de pagar o custo da necropole
    muralha=CartaDeDistrito(6,TipoDistrito.Especial,'muralha',None,1)#o personagem de rank 8 deve pagar 1 ouro a mais para usar a habilidade dele contra qualquer outro distrito de sua cidade
    escola_de_magia=CartaDeDistrito(6,TipoDistrito.Especial,'escola de magia',None,1)#ao usar habilidades que obtem recursos pelos seus distritos,a escola de magia vale como o tipo de distrito a sua escolha
    cofre_secreto=CartaDeDistrito(0,TipoDistrito.Especial,'cofre secreto',None,1)#o cofre secreto nao pode ser construido.ao final da partida,revele o cofre secreto da sua mao para marcar 3 pontos extras
    tesouro_imperial=CartaDeDistrito(5,TipoDistrito.Especial,'tesouro imperial',None,1)#ao final da partida,marque um ponto extra para cada ouro em seu tesouro
    


    #quando chama o print(cartagenerica) ele usa o _str_ do cartadistrito, fazer um for pra printar td o baralho




    

    # Criar resto do deck
    deck = [mercado,mercado,mercado,mercado,mercado, taverna,taverna,taverna,taverna,taverna, torre_de_vigia,torre_de_vigia,torre_de_vigia, palacio,palacio,palacio,prisao,prisao,prisao,caserna,caserna,caserna,fortaleza,fortaleza,solar,solar,solar,solar,solar,templo,
    templo,templo,castelo,castelo,castelo,castelo,porto,porto,porto,catedral,catedral,mosteiro
    ,mosteiro,mosteiro,docas,docas,docas,prefeitura,prefeitura,igreja,igreja,posto_de_comercio,posto_de_comercio,posto_de_comercio,portao_do_dragao,bairro_assombrado,estabulos,teatro,estrutura,abrigo_para_pobres,mina_de_ouro,covil_dos_ladroes,
    laboratorio,necropole,muralha,escola_de_magia,cofre_secreto,tesouro_imperial]
    deck.append(deck)
    

    shuffle(deck)
    
  
    return deck


    
def create_players_deck(num_of_players):
    assassin = CharacterCard("assassin", None, 1, None) #criar efeito e skill 
    thief = CharacterCard('Thief', None, 2, None)
    mage = CharacterCard("Mage", None, 3, None)
    king = CharacterCard("King", None, 4, None)

    players_deck = [assassin, thief, mage, assassin, thief, mage, assassin, thief]
    shuffle(players_deck)
    players_out_visible = []
    
    print(players_deck)

    if num_of_players == 4:
        players_out_visible.append(players_deck.pop(0))
        players_out_visible.append(players_deck.pop(0))
        players_out_not_visible = players_deck.pop(0)

    elif num_of_players == 5:
        players_out_visible.append(players_deck.pop(0))
        players_out_not_visible = players_deck.pop(0)

    elif num_of_players == 6:
        players_out_not_visible = players_deck.pop(0)

    elif num_of_players == 7:
        players_out_not_visible = players_deck.pop(0)
        # se forem 7 jogadores, o 7 pode escolher entre a não visível e a última carta do deck principal

    players_deck.append(king)

    #Criar resto dos personagens
    return players_deck

def create_players(num_of_players, deck):
    players_list = []

    for player in range(num_of_players):
        hand = deck[0:4]
        players_list.append(Players(0, player, None, 2, hand, [], player, True if player == 1 else False))
        del deck[0:4]

    return players_list

#score, name, player_card, gold, hand, districts, order, king

def start(num_players):
    deck = criar_baralho()
    characters = create_players_deck(4)
    players = create_players(num_players, deck)

    board = Board(deck, 1, "escolha de personagens", characters)
    state = State(deck, players)
    
    print(board)

start(4)
#class Actions:
#    def __init__(self, choose_characters, draw_cards, get_coins, build, character_skill, district_skill, end_turn)


