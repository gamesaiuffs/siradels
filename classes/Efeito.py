from abc import abstractmethod
import Estado
import Jogador


class Efeito:
    def __init__(self, passivo: bool, descricao: str):
        self.passivo = passivo
        self.descricao = descricao

    def __str__(self):
        return f'descrição do efeito: {self.descricao}'

    @abstractmethod
    def ativar_efeito(self, estado: Estado, jogador: Jogador) -> Estado:
        pass
