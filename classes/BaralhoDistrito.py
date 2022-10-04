# nao utilizada
import CartaDistrito
import TipoDistrito
import Efeito
import Estado
import Jogador

'''class BaralhoDistrito:
    def __init__(self, value, type, name, effect):
        self.value = value 
        self.type = type
        self.name = name 
        self.effect = effect 

    def __str__(self):
        return print("value: ", self.value, \
            "type: ", self.type, \
            "name: ",self.name, \
            "effect: ", self.effect)
'''


##Exemplo implementação efeito distrito
class EfeitoPortaoDragao(Efeito):
    def __init__(self):
        super().__init__(True, 'Ao final da partida, marque 2 pontos extras')

    @staticmethod
    def ativar_efeito(estado: Estado, jogador: Jogador) -> Estado:
        jogador.pontuacao += 2
        return estado


portao_do_dragao = CartaDistrito(6, TipoDistrito.Especial, 'portao do dragao', EfeitoPortaoDragao(), 1)  # ao final da partida marque 2 pontos extras
