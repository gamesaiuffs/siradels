def discretizar(valor, intervalos):
    """
    Recebe uma lista com valores de intervalos e um valor, 
    e então retorna o a classe (intervalo) ao qual o valor pertence. 
    """
    for i, limite in enumerate(intervalos):
        if valor <= limite:
            return i
    return len(intervalos)

def binarizar(valor, limite):
    """
    Recebe um valor de entrada e um valor de limite.
    retorna 1 se valor > limite, senão 0.  
    """
    return 1 if valor > limite else 0

def escalar(valor, min_val, max_val):
    """
    Recebe um valor de entrada e o valor mínimo e máximo de escala. 
    Retorna o valor de entrada normalizado de acordo com o intervalo.
    """
    return (valor - min_val) / (max_val - min_val)

def codificar_one_hot(valor, categorias):
    """
    Recebe um valor e uma lista com as categorias de valores.
    Retorna a entrada codificada em one hot.
    """
    vetor = [0] * len(categorias)
    if valor in categorias:
        vetor[categorias.index(valor)] = 1
    return vetor