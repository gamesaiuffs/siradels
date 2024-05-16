from collections import defaultdict
from classes.enum.TipoPersonagem import TipoPersonagem
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.enum.TipoAcao import TipoAcao


class Jogador:
    # Construtor
    def __init__(self):
        self.pontuacao: int = 0
        self.pontuacao_final: int = 0
        self.nome: str = ''
        self.personagem: CartaPersonagem = CartaPersonagem('Nenhum', 0, TipoPersonagem.Nenhum)
        self.ouro: int = 2
        self.cartas_distrito_mao: list[CartaDistrito] = []
        self.distritos_construidos: list[CartaDistrito] = []
        self.rei: bool = False
        self.morto: bool = False
        self.roubado: bool = False
        self.qtd_construido_turno: int = 0
        self.acoes_realizadas: list[bool] = [False for _ in range(len(TipoAcao))]
        self.terminou: bool = False  # True se o jogador construiu 7 distritos
        self.vencedor: bool = False
        self.tem_distrito = defaultdict(int)

    # To String
    def __str__(self) -> str:
        return f'\n{self.nome}: {self.personagem.obter_nome()} / Morto? {self.morto} / É rei? {self.rei}' \
               f' / Qtd de ouro: {self.ouro} / Pont: {self.pontuacao} / Roubado? {self.roubado}' \
               f'\nMão: {Jogador.imprimir_nomes_distritos(self.cartas_distrito_mao)}' \
               f'\nDistritos construídos: {Jogador.imprimir_nomes_distritos(self.distritos_construidos)}' \


    # Imprimir lista de distritos
    @staticmethod
    def imprimir_distritos(distritos: list[CartaDistrito]) -> str:
        if len(distritos) == 0:
            return 'Nenhum distrito'
        i = iter(distritos)
        texto = '\n\t' + str(next(i))
        for distrito in i:
            texto += ', ' + str(distrito)
        return texto

    def construir(self, distrito: CartaDistrito):
        self.pontuacao += distrito.valor_do_distrito
        self.distritos_construidos.append(distrito)
        self.tem_distrito[distrito.nome_do_distrito] += 1
        self.qtd_construido_turno += 1

    def destruir(self, estado, distrito: CartaDistrito):
        self.pontuacao -= distrito.valor_do_distrito
        estado.tabuleiro.baralho_distritos.append(distrito)
        self.distritos_construidos.remove(distrito)
        self.tem_distrito[distrito.nome_do_distrito] -= 1

    @staticmethod
    def imprimir_nomes_distritos(distritos: list[CartaDistrito]) -> str:
        if len(distritos) == 0:
            return 'Nenhum distrito'
        i = iter(distritos)
        texto = str(next(i).nome_do_distrito)
        for distrito in i:
            texto += ', ' + str(distrito.nome_do_distrito)
        return texto

    def construiu_distrito(self, nome: str) -> bool:
        return self.tem_distrito[nome] > 0

    def coletou_recursos(self) -> bool:
        return self.acoes_realizadas[TipoAcao.ColetarOuro.value] or self.acoes_realizadas[TipoAcao.ColetarCartas.value]
    