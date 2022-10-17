# Imports
from CartaDistrito import CartaDistrito
from CartaPersonagem import CartaPersonagem


class Jogador:
    # Construtor
    def __init__(self, nome: str):
        self.pontuacao = 0 
        self.nome = nome 
        self.personagem = CartaPersonagem("Nenhum", 0)
        self.ouro = 2
        self.cartas_distrito_mao = []
        self.distritos_construidos = []
        self.rei = False
        self.morto = False
        self.roubado = False

    # To String
    def __str__(self) -> str:
        return f"\nNome: {self.nome}" \
               f"\nPersonagem: {self.personagem}" \
               f"\nPontuação: {self.pontuacao}" \
               f"\nOuro: {self.ouro}" \
               f"\nCartas de distrito na mão: {self.imprimir_distritos(self.cartas_distrito_mao)}" \
               f"\nDistritos cronstruidos: {self.imprimir_distritos(self.distritos_construidos)}" \
               f"\nÉ o rei: {self.rei}" \
               f"\nEstá morto: {self.morto}" \
               f"\nFoi roubado: {self.roubado}"

    # Imprimir lista de distritos
    @staticmethod
    def imprimir_distritos(distritos: list[CartaDistrito]) -> str:
        if len(distritos) == 0:
            return "Nenhum distrito"
        i = iter(distritos)
        texto = "\n\t" + str(next(i))
        for distrito in i:
            texto += ", " + str(distrito)
        return texto
