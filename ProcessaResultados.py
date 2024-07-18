import re

def ler_vitorias_do_arquivo(caminho_arquivo):
    # Abre e lê o conteúdo do arquivo
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    # print(conteudo)
    
    # Expressão regular para encontrar o padrão "Agente - Vitórias: <número>"
    padrao = re.compile(r"Agente - VitÃ³rias: (\d+)")
    
    # Lista para armazenar os valores de vitórias
    vitorias = []
    
    # Encontra todas as ocorrências do padrão no conteúdo do arquivo
    matches = padrao.findall(conteudo)
    
    # Converte cada correspondência para inteiro e adiciona à lista de vitórias
    for match in matches:
        vitorias.append(int(match))
    
    return vitorias

# Caminho do arquivo de texto
caminho_arquivo = 'reforco2/hist.txt'

# Chama a função e armazena o resultado
vitorias = ler_vitorias_do_arquivo(caminho_arquivo)

# Exibe o vetor de vitórias
print(vitorias)