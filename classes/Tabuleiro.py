from BaralhoDistrito import BaralhoDistrito
from BaralhoPersonagem import BaralhoPersonagem
from Fase import Fase
from TipoDistrito import TipoDistrito

class Tabuleiro:
    def __init__(self, num_jogadores):  
        self.baralho_de_distritos = BaralhoDistrito.criar_baralho()
        self.turno = 1
        self.fase = Fase.EscolhaPersonagem
        self.baralho_de_personagens = BaralhoPersonagem.criar_baralho(num_jogadores)

    def __str__(self):
        return f"deck: {self.baralho_de_distritos} turn: {self.turno} stage: {self.fase} characters:  {self.baralho_de_personagens}"

    def criar_baralho_personagem(self):
        #todo
        assassin = CharacterCard("assassin", None, 1, None) #criar efeito e skill 
        thief = CharacterCard('Thief', None, 2, None)
        mage = CharacterCard("Mage", None, 3, None)
        king = CharacterCard("King", None, 4, None)
        cardinal = CharacterCard("Cardinal", None, 5, None)
        alchemist = CharacterCard("Alchemist", None, 6, None)
        navigator = CharacterCard("Navigator", None, 7, None)
        warlord = CharacterCard("Warlord", None, 8, None)


        players_deck = [assassin, thief, mage, cardinal, alchemist, navigator, warlord]
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

        return players_deck


def criar_baralho():
    mercado = CartaDeDistrito(2, TipoDistrito.Comercio, 'mercado', None,4)
    taverna = CartaDeDistrito(1, TipoDistrito.Comercio, 'taverna', None,5)
    prefeitura=CartaDeDistrito(5,TipoDistrito.Comercio,'prefeitura',None,2)
    porto=CartaDeDistrito(4,TipoDistrito.Comercio,'porto',None,3)
    docas=CartaDeDistrito(3,TipoDistrito.Comercio,'docas',None,3)
    posto_de_comercio=CartaDeDistrito(2,TipoDistrito.Comercio,'posto de comercio',None,3)

    torre_de_vigia = CartaDeDistrito(1, TipoDistrito.Militar, 'torre de vigia', None,3)
    prisao = CartaDeDistrito(2, TipoDistrito.Militar, 'prisao',None,3)
    caserna = CartaDeDistrito(3,TipoDistrito.Militar, 'barracos',None,3)
    fortaleza = CartaDeDistrito(5,TipoDistrito.Militar,'fortaleza',None,2)

    templo=CartaDeDistrito(1,TipoDistrito.Religioso,'templo',None,3)
    mosteiro=CartaDeDistrito(3,TipoDistrito.Religioso,'mosteiro',None,3)
    catedral=CartaDeDistrito(5,TipoDistrito.Religioso,'catedral',None,2)
    igreja=CartaDeDistrito(2,TipoDistrito.Religioso,'igreja',None,3)

    #nobre
    solar = CartaDeDistrito(3,TipoDistrito.Nobre,'solar',None,5)
    castelo=CartaDeDistrito(4,TipoDistrito.Nobre,'castelo',None,4)
    palacio = CartaDeDistrito(5, TipoDistrito.Nobre, 'palacio', None,3)

    # //especiais
    portao_do_dragao=CartaDeDistrito(6,TipoDistrito.Especial,'portao do dragao',None,1)#ao final da partida marque 2 pontos extras
    bairro_assombrado=CartaDeDistrito(2,TipoDistrito.Especial,'bairro_assombrado',None,1)#ao final da partida,vale com 1 tipo de distrito à sua escolha
    estabulos=CartaDeDistrito(2,TipoDistrito.Especial,'estabulos',None,1)#a construcao dos estabulos nao conta para o seu limite de construcao para este turno
    teatro=CartaDeDistrito(6,TipoDistrito.Especial,'teatro',None,1)#ao final de cada fase de escolha,vc pode trocar sua carta de personagem escolhida com a carta de personagem de um oponente
    estrutura=CartaDeDistrito(3,TipoDistrito.Especial,'estrutura',None,1)#vc pode construir um distrito destruindo a estrutura,em vez de pagar os custos do distrito em questao
    abrigo_para_pobres=CartaDeDistrito(4,TipoDistrito.Especial,'abrigo para pobres',None,1)#se nao houver ouro no seu tesouro no fim do seu turno,ganhe 1 ouro
    mina_de_ouro=CartaDeDistrito(6,TipoDistrito.Especial,'mina de ouro',None,1)#se vc optar por ganhar ouro ao coletar recursos,ganhe 1 ouro extra
    covil_dos_ladroes=CartaDeDistrito(6,TipoDistrito.Especial,'covil dos ladroes',None,1)#pague parte ou todo o custo do covil dos ladroes com cartas de sua mao,em vez de ouro,a uma taxa de uma carta:um ouro
    laboratorio=CartaDeDistrito(5,TipoDistrito.Especial,'laboratorio',None,1)#uma vez por turno,decarte uma carta de sua mao para ganhar 2 ouros
    necropole=CartaDeDistrito(5,TipoDistrito.Especial,'necropole',None,1)#voce pode consturir a necropole destruindo um distrito na sua cidade,ao invez de pagar o custo da necropole
    muralha=CartaDeDistrito(6,TipoDistrito.Especial,'muralha',None,1)#o personagem de rank 8 deve pagar 1 ouro a mais para usar a habilidade dele contra qualquer outro distrito de sua cidade
    escola_de_magia=CartaDeDistrito(6,TipoDistrito.Especial,'escola de magia',None,1)#ao usar habilidades que obtem recursos pelos seus distritos,a escola de magia vale como o tipo de distrito a sua escolha
    cofre_secreto=CartaDeDistrito(0,TipoDistrito.Especial,'cofre secreto',None,1)#o cofre secreto nao pode ser construido.ao final da partida,revele o cofre secreto da sua mao para marcar 3 pontos extras
    tesouro_imperial=CartaDeDistrito(5,TipoDistrito.Especial,'tesouro imperial',None,1)#ao final da partida,marque um ponto extra para cada ouro em seu tesouro
    


    #quando chama o print(cartagenerica) ele usa o _str_ do cartadistrito, fazer um for pra printar td o baralho




    

    # Criar resto do deck
    deck = [mercado,mercado,mercado,mercado,mercado, taverna,taverna,taverna,taverna,taverna, torre_de_vigia,torre_de_vigia,torre_de_vigia, palacio,palacio,palacio,prisao,prisao,prisao,caserna,caserna,caserna,fortaleza,fortaleza,solar,solar,solar,solar,solar,templo,
    templo,templo,castelo,castelo,castelo,castelo,porto,porto,porto,catedral,catedral,mosteiro
    ,mosteiro,mosteiro,docas,docas,docas,prefeitura,prefeitura,igreja,igreja,posto_de_comercio,posto_de_comercio,posto_de_comercio,portao_do_dragao,bairro_assombrado,estabulos,teatro,estrutura,abrigo_para_pobres,mina_de_ouro,covil_dos_ladroes,
    laboratorio,necropole,muralha,escola_de_magia,cofre_secreto,tesouro_imperial]
    deck.append(deck)
    

    shuffle(deck)
    
  
    return deck