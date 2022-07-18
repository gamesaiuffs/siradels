class Board:
    def __init__(self, deck, turn, stage, characters):  
        self.deck = deck 
        self.turn = turn 
        self.stage = stage 
        self.characters = characters

    def __str__(self):
        return f"deck: {self.deck}, turn: {self.turn} stage: {self.stage} characters:  {self.characters}"
