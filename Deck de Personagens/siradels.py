from random import shuffle


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

class DistrictCard:
    def __init__(self, value, type, name, effect):
        self.value = value 
        self.type = type
        self.name = name 
        self.effect = effect 

    def __str__(self):
        return print("value: ", self.value, \
            "type: ", self.type, \
            "name: ",self.name, \
            "effect: ", self.effect)

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

def create_deck():
    market = DistrictCard(2, 'comercio', 'Market', None)
    tavern = DistrictCard(1, 'comercio', 'Tavern', None)
    whatch_tower = DistrictCard(1, 'militar', 'Whatch Tower', None)
    palace = DistrictCard(5, 'nobre', 'Palace', None)

    # Criar resto do deck
    deck = [market, tavern, whatch_tower, palace]
    deck.append(deck)
    deck.append(deck)
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
    deck = create_deck()
    characters = create_players_deck(4)
    players = create_players(num_players, deck)

    board = Board(deck, 1, "escolha de personagens", characters)
    state = State(deck, players)
    
    print(board)

start(4)
#class Actions:
#    def __init__(self, choose_characters, draw_cards, get_coins, build, character_skill, district_skill, end_turn)


