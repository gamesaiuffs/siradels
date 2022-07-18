class State:
    def __init__(self, board, players):
        self.board = board 
        self.players = players

    def __str__(self):
        return print("Board: ", self.board, \
            "Players: ", self.players)