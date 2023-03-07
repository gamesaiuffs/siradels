# Imports
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.enum.TipoAcao import TipoAcao
from typing import List


class Jogador:
    # Construtor
    def __init__(self, nome: str):
        self.pontuacao = 0
        self.nome = nome
        self.personagem = CartaPersonagem("Nenhum", 0)
        self.ouro = 2
        self.cartas_distrito_mao: List[CartaDistrito] = []
        self.distritos_construidos: List[CartaDistrito] = []
        self.rei = False
        self.morto = False
        self.roubado = False
        self.construiu = False
        self.construiu_estabulo = False
        self.ouro_gasto = 0
        self.acoes_realizadas = [False for _ in range(len(TipoAcao))]
        self.terminou = False  # True se o jogador construiu 7 distritos

    # To String
    def __str__(self) -> str:
        return f"\n{self.nome}: {self.personagem.obter_nome()} / Morto? {self.morto} / É rei? {self.rei}" \
               f" / Qtd de ouro: {self.ouro} / Pont: {self.pontuacao} / Roubado? {self.roubado}" \
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

    def construiu_distrito(self, nome: str) -> bool:
        for carta in self.distritos_construidos:
            if carta.nome_do_distrito == nome:
                return True
        return False

    def coletou_recursos(self) -> bool:
        return self.acoes_realizadas[TipoAcao.ColetarOuro.value] | self.acoes_realizadas[TipoAcao.ColetarCartas.value]
    