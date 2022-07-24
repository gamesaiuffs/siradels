class CharacterCard:
    def __init__(self, name, effect, rank, skill, morto, roubado):
        self.name = name 
        self.effect = effect 
        self.rank = rank
        self.skill = skill
        self.morto = morto
        self.roubado = roubado

    def __str__(self):
        print("name: ", self.name,\
            "effect: ", self.effect,\
            "rank: ", self.rank,\
            "skill: ", self.skill,\
            "morto: ", self.morto,\
            "roubado: ", self.roubado)
