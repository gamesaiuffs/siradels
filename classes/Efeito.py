# Imports
from abc import abstractmethod
import Estado
import Jogador


class Efeito:
    # Construtor
    def __init__(self, passiva: bool, descricao: str):
        self.descricao = descricao
        self.passiva = passiva

    # To String
    def __str__(self):
        return f'\nDescrição: {self.descricao}' \
               f'\nPassiva: {self.passiva}'

    @abstractmethod
    def ativar_efeito(self, estado: Estado, jogador: Jogador) -> Estado:
        # WIP
        pass
