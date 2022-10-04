
#nao utilizada

from random import shuffle
from CartaPersonagem import CartaPersonagem


class BaralhoPersonagem:

    @staticmethod
    def criar_baralho(num_jogadores: int) -> list(CartaPersonagem):
        assassino = CartaPersonagem("assassino", None, 1, None)  # criar efeito e skill
        ladrao = CartaPersonagem('Ladrão', None, 2, None)
        mago = CartaPersonagem("Mago", None, 3, None)
        rei = CartaPersonagem("Rei", None, 4, None)
        cardeal = CartaPersonagem("Cardeal", None, 5, None)
        alquimista = CartaPersonagem("Alquimista", None, 6, None)
        navegadora = CartaPersonagem("Navegadora", None, 7, None)
        senhor_da_guerra = CartaPersonagem("Senhor da Guerra", None, 8, None)

        baralho_personagens = [assassino, ladrao, mago, rei, cardeal, alquimista, navegadora, senhor_da_guerra]
        shuffle(baralho_personagens)
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

        # Criar resto dos personagens
        return players_deck