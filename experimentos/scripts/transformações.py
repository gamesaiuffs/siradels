from classes.enum.TipoDistrito import TipoDistrito

def discretizar(valor, intervalos):
    """
    Recebe uma lista com valores de intervalos e um valor, \n
    e então retorna o a classe (intervalo) ao qual o valor pertence. 
    """
    for i, limite in enumerate(intervalos):
        if valor <= limite:
            return limite
    return len(intervalos)

def binarizar(valor, limite):
    """
    Recebe um valor de entrada e um valor de limite.\n
    retorna 1 se valor > limite, senão 0.  
    """
    return 1 if valor > limite else 0

def escalar(valor, min_val, max_val):
    """
    Recebe um valor de entrada e o valor mínimo e máximo de escala. \n
    Retorna o valor de entrada normalizado de acordo com o intervalo.
    """
    return (valor - min_val) / (max_val - min_val)

def codificar_one_hot(valor, categorias):
    """
    Recebe um valor e uma lista com as categorias de valores.\n
    Retorna a entrada codificada em one hot.
    """
    vetor = [0] * len(categorias)
    if valor in categorias:
        vetor[categorias.index(valor)] = 1
    return vetor

# Novos metodos 
def limitar_valores(valor: int, limites: list):
    """
    Recebe um valor e os limites [inferior, superior]\n
    Retorna o valor dentro dos limites
    """
    if valor < limites[0]: return limites[0]
    elif valor > limites[1]: return limites[1]
    else: return valor
    
def limitar_valores_vetor(valores: list, limites: list):
    """
    Recebe um vetor de valores e os limites [inferior, superior]\n
    Retorna um vetor com os valores dentro dos limites
    """
    lista = []
    for val in valores:
        if val < limites[0]: lista.append(limites[0])
        elif val > limites[1]: lista.append(limites[1])
        else: lista.append(val)
        
    return lista

def intervalos_em_classes(valor, limites):
    """
    Recebe um valor e as classes, com limite inferior e superior \n
        [(classe, lim_inf, lim_sup), (classe, lim_inf, lim_sup)] \n
        [(1, 0, 2), (2, 3, 4), (3, 5, 10000)]\n
    Retorna a classe ao qual o valor pertence
    """
    for classe, lim_inf, lim_sup in limites:
        if valor >= lim_inf and valor <= lim_sup: return classe
        
    raise Exception("Classe não encontrada")

def intervalos_em_classes_vetor(lista_valores: list, limites):
    """
    Recebe uma lista de valores e as classes, com limite inferior e superior \n
        [(classe, lim_inf, lim_sup), (classe, lim_inf, lim_sup)] \n
        [(1, 0, 2), (2, 3, 4), (3, 5, 10000)]\n
    Retorna um vetor com todos os valores do original adequados às classes
    """
    nova_lista = []
    for valor in lista_valores:
        for classe, lim_inf, lim_sup in limites:
            if valor >= lim_inf and valor <= lim_sup: 
                nova_lista.append(classe)
            
    return nova_lista

# Funções especificas 
def encontra_carta_mais_cara(estado): 
    """
    Recebe a variável com os componentes do estado\n
    Retorna a carta mais cara da lista
    """
    # print(estado)
    maior_custo = 0
    for distrito in estado["jogador_visao"].cartas_distrito_mao:
        # descobre o distrito mais caro da mao
        if distrito.valor_do_distrito > maior_custo:
            maior_custo = distrito.valor_do_distrito
    
    return maior_custo


def encontra_carta_mais_barata(estado): 
    """
    Recebe a variável com os componentes do estado\n
    Retorna a carta mais barata da lista
    """
    menor_custo = 10
    for distrito in estado["jogador_visao"].cartas_distrito_mao:
        # descobre o distrito mais barato da mao
        if distrito.valor_do_distrito < menor_custo:
            menor_custo = distrito.valor_do_distrito
            
    if menor_custo == 10:
        menor_custo = 0

    return menor_custo

def conta_tipos_distritos(jogador): 
    """
    Recebe o jogador do qual serão contados os tipos de distritos\n
    Retorna uma lista de 5 posicoes com as quantidades totais de distritos de cada tipo do agente na ordem [nobre, religioso, militar, comercial, especial]
    """
    nobre = 0
    religioso = 0
    militar = 0
    comercial = 0
    especial = 0
    for distrito in jogador.distritos_construidos:
        if distrito.tipo_de_distrito == TipoDistrito.Nobre:
            nobre += 1
        elif distrito.tipo_de_distrito == TipoDistrito.Religioso:
            religioso += 1
        elif distrito.tipo_de_distrito == TipoDistrito.Militar:
            militar += 1
        elif distrito.tipo_de_distrito == TipoDistrito.Comercial:
            comercial += 1
        elif distrito.tipo_de_distrito == TipoDistrito.Especial:
            especial += 1 
            
    return [nobre, religioso, militar, comercial, especial]


def conta_tipos_distritos_mesa(estado): 
    """
    Recebe o jogador do qual serão contados os tipos de distritos\n
    Retorna uma lista de 5 posicoes com as quantidades totais de distritos de cada tipo dos oponentes na ordem [nobre, religioso, militar, comercial, especial]
    """
    nobre = 0
    religioso = 0
    militar = 0
    comercial = 0
    especial = 0
    for jogador in estado["jogadores"]:
        for distrito in jogador.distritos_construidos:
            if distrito.tipo_de_distrito == TipoDistrito.Nobre:
                nobre += 1
            elif distrito.tipo_de_distrito == TipoDistrito.Religioso:
                religioso += 1
            elif distrito.tipo_de_distrito == TipoDistrito.Militar:
                militar += 1
            elif distrito.tipo_de_distrito == TipoDistrito.Comercial:
                comercial += 1
            elif distrito.tipo_de_distrito == TipoDistrito.Especial:
                especial += 1 
                    
    return [nobre, religioso, militar, comercial, especial]


def conta_distritos_construidos(estado): 
    """
    Recebe a variável com os componentes do estado\n
    Retorna uma lista de 5 posicoes com o numero de distritos construidos de cada jogador
    """
    construidos = []
    for jogador in estado["jogadores"]:
        construidos.append(len(jogador.distritos_construidos))
        
    return construidos


def conta_cartas_mao(estado): 
    """
    Recebe a variável com os componentes do estado\n
    Retorna uma lista de 5 posicoes com o numero de cartas de cada jogador
    """
    cartas = []
    for jogador in estado["jogadores"]:
        cartas.append(len(jogador.cartas_distrito_mao))
        
    return cartas

def conta_ouros_adversarios(estado): 
    """
    Recebe a variável com os componentes do estado\n
    Retorna uma lista de 4 posicoes com o numero de ouros dos jogadores adversarios
    """
    ouros = []
    for jogador in estado["jogadores"]:
        if estado["jogador_visao"] != jogador:
            ouros.append(jogador.ouro)

    return ouros


def disponibilidade_personagens(baralho_personagens):
    """
    Recebe a lista contendo o baralho de personagens disponíveis para a escolha
    Retorna um vetor binário de representação da dispoibilidade (8 posições)
    """
    p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = 0
    for carta in baralho_personagens:
        if carta.rank == 1:
            p1 = 1
        elif carta.rank == 2:
            p2 = 1
        elif carta.rank == 3:
            p3 = 1
        elif carta.rank == 4:
            p4 = 1
        elif carta.rank == 5:
            p5 = 1
        elif carta.rank == 6:
            p6 = 1
        elif carta.rank == 7:
            p7 = 1
        elif carta.rank == 8:
            p8 = 1
    return [p1, p2, p3, p4, p5, p6, p7, p8]


def total_ouros_mesa(estado):
    """
    Recebe a variável de estado montada 
    Retorna uma lista com o ouro de todos os jogadores da mesa 
    """
    ouros = []
    for jogador in estado["jogadores"]:
        ouros.append(jogador.ouro)
        
    return ouros





# Funções de calculo da proporção 

def ouro_personagem_proporcao(x):
    soma = sum(total_ouros_mesa(x))
    if soma == 0: return 0.0
    return x["jogador_visao"].ouro / soma


def cartas_dist_mao_proporcao(x):
    maximo = max(conta_cartas_mao(x))
    if maximo == 0: return 0.0
    return len(x["jogador_visao"].cartas_distrito_mao) / maximo

def qtd_dist_const_proporcao(x):
    maximo = max(conta_distritos_construidos(x))
    if maximo == 0: return 0.0
    return len(x["jogador_visao"].distritos_construidos) / maximo

def qtd_dist_cada_tipo_proporcao(x):
    qtd_oponentes = conta_tipos_distritos_mesa(x)
    qtd_agente = conta_tipos_distritos(x["jogador_visao"])
    return [agente / oponente if oponente != 0 else 0.0 for oponente, agente in zip(qtd_oponentes, qtd_agente)]
        
def jog_mais_cartas_mao_proporcao(x): 
    media = sum(conta_cartas_mao(x)) / 5
    if media == 0: return 0.0
    return max(conta_cartas_mao(x)) / media

def ouro_oponentes_proporcao(x):
    ouro_agente = x["jogador_visao"].ouro
    ouro_adversarios = conta_ouros_adversarios(x)
    if ouro_agente == 0: return ouro_adversarios
    return [ouro / ouro_agente for ouro in ouro_adversarios]
