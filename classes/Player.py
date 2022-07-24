class Player:
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
