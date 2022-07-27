import CartaDeDistrito
import CartaDePersonagem
import Fase

class Tabuleiro:
    def __init__(self, num_jogadores):  
        self.baralho_de_distritos = self.criar_baralho_distritos()
        self.turno = 1
        self.fase = Fase.EscolhaPersonagem
        self.baralho_de_personagens = self.criar_baralho_personagem(num_jogadores)

    def __str__(self):
        return f"deck: {self.baralho_de_distritos} turn: {self.turno} stage: {self.fase} characters:  {self.baralho_de_personagens}"

    def criar_baralho_distritos():
        #todo
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
    def criar_baralho_personagem():
        #todo
        assassin = CharacterCard("assassin", None, 1, None) #criar efeito e skill 
        thief = CharacterCard('Thief', None, 2, None)
        mage = CharacterCard("Mage", None, 3, None)
        king = CharacterCard("King", None, 4, None)
        cardinal = CharacterCard("Cardinal", None, 5, None)
        alchemist = CharacterCard("Alchemist", None, 6, None)
        navigator = CharacterCard("Navigator", None, 7, None)
        warlord = CharacterCard("Warlord", None, 8, None)


        players_deck = [assassin, thief, mage, cardinal, alchemist, navigator, warlord]
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

        return players_deck