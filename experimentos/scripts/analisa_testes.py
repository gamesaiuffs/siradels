import re
import sys

def extrair_porcentagens(linhas):
    posicoes = {"Primeiro": [], "Segundo": [], "Terceiro": [], "Quarto": [], "Quinto": []}
    
    for linha in linhas:
        match = re.match(r"\s*(Primeiro|Segundo|Terceiro|Quarto|Quinto)\s*:\s*([\d.]+)%", linha)
        if match:
            posicao, valor = match.groups()
            posicoes[posicao].append(float(valor))
    
    return posicoes

def calcular_media_porcentagens(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    posicoes = extrair_porcentagens(linhas)
    
    medias = {pos: sum(valores) / len(valores) for pos, valores in posicoes.items() if valores}
    return medias

if __name__ == "__main__":
    
    num_experimento = sys.argv[1]
    arquivo = f"../../aaa_experimentos_final/{num_experimento}/resultado_contra_personais.txt"
    
    medias = calcular_media_porcentagens(arquivo)

    for posicao, media in medias.items():
        print(f"{posicao}: {media:.2f}%")