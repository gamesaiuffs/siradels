from enum import Enum

# JAtual
    # Qtd ouro [0,1,2,3,4,5,>=6] = 56
    # Qtd carta mão [0,1,2,3,4,>=5] = 48
    # Carta mão mais cara [1 a 6] = 48
    # Carta mão mais barata [1 a 6] = 48
    # Qtd distritos construido [0 a 6] = 56
    # Qtd distrito construido Militar [0,1,2,>=3] = 32
    # Qtd distrito construido Religioso [0,1,2,>=3] = 32
    # Qtd distrito construido Nobre [0,1,2,>=3] = 32
    # Qtd personagens disponíveis [2,3,4,5,6,7] = 48
    # Pontuacao [0-3,4-7,8-11,12-15,16-19,20-23,>=24] = 56
    # JMais
    # Qtd distrito construido [0 a 6] = 56
    # Qtd ouro [0,1,2,3,4,5,>=6] = 56
    # Qtd carta mão [0,1,2,3,4,>=5] = 48
    # Personagem visivel descartado [1,2,3,5,6,7,8] = 56
    # Personagem disponivel para escolha [1,2,3,4,5,6,7,8] = 64
    # Quantidade de jogadores [4,5,6] = 24

    # Simulacao treinar tabelas individualmente versus treinar tudo junto
    # Adversários totalmente aleatório executando todas ações antes de passar
    # IA usar mesma estratégia do aleatório para demais ações

class TipoTabelaPersonagem(Enum):
    JaQtdOuro = 0
    JaQtdCarta = 1
    JaCartaCara = 2
    JaCartaBarata = 3
    JaConstruidos = 4
    JaConstruidosMilitar = 5
    JaConstruidosReligioso = 6
    JaConstruidosNobre = 7
    JaQtdPersonagem = 8
    JaPontuacao = 9
    JmConstruidos = 10
    JmQtdOuro = 11
    JmQtdCarta = 12
    PersonagemDisponivel = 13
    QtdJogadores = 14
    PersonagemDescartado = 15
