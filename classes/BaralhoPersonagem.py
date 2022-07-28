import CartaPersonagem


class BaralhoPersonagem:

    @staticmethod
    def criar_baralho(num_jogadores: int) -> list(CartaPersonagem):
        assassin = CharacterCard("assassin", None, 1, None)  # criar efeito e skill
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

        # Criar resto dos personagens
        return players_deck