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
        self.construiu = False
        self.coletou_recursos = False
        self.ouro_gasto = 0
        self.acoes_realizadas = [0 for _ in range(19)]
        self.terminou = False # True se o jogador construiu 7 distritos 

    # To String
    def __str__(self) -> str:
        return f"\n{self.nome}: {self.personagem.obter_nome()} / Morto? {self.morto} / É rei? {self.rei} / Qtd de ouro: {self.ouro} / Pont: {self.pontuacao} / Roubado? {self.roubado}" \
               f"\nMão: {self.imprimir_nomes_distritos(self.cartas_distrito_mao)}" \
               f"\nDistritos construídos: {self.imprimir_nomes_distritos(self.distritos_construidos)}" \

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

    @staticmethod
    def imprimir_nomes_distritos(distritos: list[CartaDistrito]) -> str:
        if len(distritos) == 0:
            return "Nenhum distrito"
        i = iter(distritos)
        texto = str(next(i).nome_do_distrito)
        for distrito in i:
            texto += ", " + str(distrito.nome_do_distrito)
        return texto
