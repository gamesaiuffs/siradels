from classes.model.Estado import Estado

def calcular_qtd_tipos_distritos_construidos(estado: Estado):
    # verificar distritos construídos
    qtd_distritos_cada_tipo = {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0
    }

    # mapear quantos distritos de cada tipo foram construídos
    for dist in estado.jogador_atual.distritos_construidos:
        qtd_distritos_cada_tipo[str(dist.tipo_de_distrito.value)] += 1

    # ordenar dicionário por número de distritos construídos de cada tipo
    qtd_distritos_cada_tipo = dict(sorted(qtd_distritos_cada_tipo.items(), key=lambda item: item[1], reverse=True))

    return  qtd_distritos_cada_tipo