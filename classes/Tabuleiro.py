from pickle import FALSE
from BaralhoDistrito import BaralhoDistrito
from BaralhoPersonagem import BaralhoPersonagem
from Fase import Fase
from TipoDistrito import TipoDistrito
from CartaDistrito import CartaDistrito
from CartaPersonagem import CartaPersonagem
from Jogador import Jogador
from Estado import Estado

from Efeito import Efeito

from random import shuffle



class Tabuleiro:
    def __init__(self, num_jogadores):  
        self.baralho_de_distritos = self.criar_baralho()
        self.turno = 1
        self.fase = Fase.EscolhaPersonagem
        self.baralho_de_personagens = BaralhoPersonagem.criar_baralho(num_jogadores)

    def __str__(self):
        return f"deck: {self.baralho_de_distritos} turn: {self.turno} stage: {self.fase} characters:  {self.baralho_de_personagens}"

    def criar_baralho_personagem(self,num_jogadores):
        #todo
        assassino = CartaPersonagem("Assassino", None, 1, None) #criar efeito e skill 
        ladrao = CartaPersonagem("Ladrao", None, 2, None)
        mago = CartaPersonagem("Mago", None, 3, None)
        rei = CartaPersonagem("Rei", None, 4, None)
        cardeal = CartaPersonagem("Cardeal", None, 5, None)
        alquimista = CartaPersonagem("Alquimista", None, 6, None)
        navegadora = CartaPersonagem("Navegadora", None, 7, None)
        senhorGuerra = CartaPersonagem("Senhor da Guerra", None, 8, None)


        mao_jogador = [assassino, ladrao, mago, cardeal, alquimista, navegadora, senhorGuerra]

        shuffle(mao_jogador)
        cartasVisiveis = []
        
        print(mao_jogador)

        if num_jogadores == 4:
            cartasVisiveis.append(mao_jogador.pop(0)) 
            cartasVisiveis.append(mao_jogador.pop(0))
            cartasNaoVisiveis = mao_jogador.pop(0)

        elif num_jogadores == 5:
            cartasVisiveis.append(mao_jogador.pop(0))
            cartasNaoVisiveis = mao_jogador.pop(0)

        elif num_jogadores == 6:
            cartasNaoVisiveis = mao_jogador.pop(0)

        elif num_jogadores == 7:
            cartasNaoVisiveis = mao_jogador.pop(0)
            # se forem 7 jogadores, o 7 pode escolher entre a não visível e a última carta do deck principal

        mao_jogador.append(rei)

        return mao_jogador


    def criar_baralho():
        mercado = CartaDistrito(2, TipoDistrito.Comercio, 'mercado', None,4)
        taverna = CartaDistrito(1, TipoDistrito.Comercio, 'taverna', None,5)
        prefeitura=CartaDistrito(5,TipoDistrito.Comercio,'prefeitura',None,2)
        porto=CartaDistrito(4,TipoDistrito.Comercio,'porto',None,3)
        docas=CartaDistrito(3,TipoDistrito.Comercio,'docas',None,3)
        posto_de_comercio=CartaDistrito(2,TipoDistrito.Comercio,'posto de comercio',None,3)

        torre_de_vigia = CartaDistrito(1, TipoDistrito.Militar, 'torre de vigia', None,3)
        prisao = CartaDistrito(2, TipoDistrito.Militar, 'prisao',None,3)
        caserna = CartaDistrito(3,TipoDistrito.Militar, 'barracos',None,3)
        fortaleza = CartaDistrito(5,TipoDistrito.Militar,'fortaleza',None,2)

        templo=CartaDistrito(1,TipoDistrito.Religioso,'templo',None,3)
        mosteiro=CartaDistrito(3,TipoDistrito.Religioso,'mosteiro',None,3)
        catedral=CartaDistrito(5,TipoDistrito.Religioso,'catedral',None,2)
        igreja=CartaDistrito(2,TipoDistrito.Religioso,'igreja',None,3)

        #nobre
        solar = CartaDistrito(3,TipoDistrito.Nobre,'solar',None,5)
        castelo=CartaDistrito(4,TipoDistrito.Nobre,'castelo',None,4)
        palacio = CartaDistrito(5, TipoDistrito.Nobre, 'palacio', None,3)

        # //especiais
        portao_do_dragao=CartaDistrito(6,TipoDistrito.Especial,'portao do dragao',None,1)#ao final da partida marque 2 pontos extras
        bairro_assombrado=CartaDistrito(2,TipoDistrito.Especial,'bairro_assombrado',None,1)#ao final da partida,vale com 1 tipo de distrito à sua escolha
        estabulos=CartaDistrito(2,TipoDistrito.Especial,'estabulos',None,1)#a construcao dos estabulos nao conta para o seu limite de construcao para este turno
        teatro=CartaDistrito(6,TipoDistrito.Especial,'teatro',None,1)#ao final de cada fase de escolha,vc pode trocar sua carta de personagem escolhida com a carta de personagem de um oponente
        estrutura=CartaDistrito(3,TipoDistrito.Especial,'estrutura',None,1)#vc pode construir um distrito destruindo a estrutura,em vez de pagar os custos do distrito em questao
        abrigo_para_pobres=CartaDistrito(4,TipoDistrito.Especial,'abrigo para pobres',None,1)#se nao houver ouro no seu tesouro no fim do seu turno,ganhe 1 ouro
        mina_de_ouro=CartaDistrito(6,TipoDistrito.Especial,'mina de ouro',None,1)#se vc optar por ganhar ouro ao coletar recursos,ganhe 1 ouro extra
        covil_dos_ladroes=CartaDistrito(6,TipoDistrito.Especial,'covil dos ladroes',None,1)#pague parte ou todo o custo do covil dos ladroes com cartas de sua mao,em vez de ouro,a uma taxa de uma carta:um ouro
        laboratorio=CartaDistrito(5,TipoDistrito.Especial,'laboratorio',None,1)#uma vez por turno,decarte uma carta de sua mao para ganhar 2 ouros
        necropole=CartaDistrito(5,TipoDistrito.Especial,'necropole',None,1)#voce pode consturir a necropole destruindo um distrito na sua cidade,ao invez de pagar o custo da necropole
        muralha=CartaDistrito(6,TipoDistrito.Especial,'muralha',None,1)#o personagem de rank 8 deve pagar 1 ouro a mais para usar a habilidade dele contra qualquer outro distrito de sua cidade
        escola_de_magia=CartaDistrito(6,TipoDistrito.Especial,'escola de magia',None,1)#ao usar habilidades que obtem recursos pelos seus distritos,a escola de magia vale como o tipo de distrito a sua escolha
        cofre_secreto=CartaDistrito(0,TipoDistrito.Especial,'cofre secreto',None,1)#o cofre secreto nao pode ser construido.ao final da partida,revele o cofre secreto da sua mao para marcar 3 pontos extras
        tesouro_imperial=CartaDistrito(5,TipoDistrito.Especial,'tesouro imperial',None,1)#ao final da partida,marque um ponto extra para cada ouro em seu tesouro
        


        #quando chama o print(cartagenerica) ele usa o _str_ do cartadistrito, fazer um for pra printar td o baralho




        

        # Criar resto do deck
        deck = [mercado,mercado,mercado,mercado,mercado, taverna,taverna,taverna,taverna,taverna, torre_de_vigia,torre_de_vigia,torre_de_vigia, palacio,palacio,palacio,prisao,prisao,prisao,caserna,caserna,caserna,fortaleza,fortaleza,solar,solar,solar,solar,solar,templo,
        templo,templo,castelo,castelo,castelo,castelo,porto,porto,porto,catedral,catedral,mosteiro
        ,mosteiro,mosteiro,docas,docas,docas,prefeitura,prefeitura,igreja,igreja,posto_de_comercio,posto_de_comercio,posto_de_comercio,portao_do_dragao,bairro_assombrado,estabulos,teatro,estrutura,abrigo_para_pobres,mina_de_ouro,covil_dos_ladroes,
        laboratorio,necropole,muralha,escola_de_magia,cofre_secreto,tesouro_imperial]
        deck.append(deck)
        

        shuffle(deck)
        
    
        return deck
# class EfeitoAssassino(Efeito):
#     def __init__(self):
#         super().__init__(FALSE, 'Assassinar')

#     @staticmethod
#     def ativar_efeito(estado: Estado, jogador: Jogador) -> Estado:
            #tem q printar pro cara escolher qual jogador matar ai pega o nome e percorre comparando quem q ta com essa carta
            #ai da morto=true e o cara perde o turno

#         for i in estado.jogadores:
#             if i.carta_personagem.nome==assasinada:
#                 i.morto=true
#                 if morto:
#                     perde o turno


            
            

#         return estado