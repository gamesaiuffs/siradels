import os
from collections import defaultdict
import re  # Para capturar a lista de estratégias corretamente
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def identificar_pastas_e_arquivos(base_path):
    treinamentos = {}  # Estrutura: {nomeTreino: {estrategia: [arquivos]}}

    for treino in os.listdir(base_path):
        treino_path = os.path.join(base_path, treino)
        if not os.path.isdir(treino_path):
            continue

        arquivos_por_estrategia = defaultdict(list)
        for i in range(10):  # Assumindo que sempre há 10 pastas numeradas de 0 a 9
            treino_num_path = os.path.join(treino_path, str(i))
            if not os.path.isdir(treino_num_path):
                continue

            for arquivo in os.listdir(treino_num_path):
                if arquivo.endswith(".csv"):
                    caminho_completo = os.path.join(treino_num_path, arquivo)
                    estrategia = identificar_estrategia(caminho_completo)
                    if estrategia:
                        arquivos_por_estrategia[estrategia].append(caminho_completo)

        treinamentos[treino] = arquivos_por_estrategia

    return treinamentos

def identificar_estrategia(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        primeira_linha = file.readline().strip()
        match = re.search(r"\[(.*?)\]", primeira_linha)
        if match:
            lista_estrategias = sorted(match.group(0).strip("[]").replace("'", "").split(", "))
            return tuple(lista_estrategias)
        print(f"Erro ao ler {caminho_arquivo}: Lista de estratégias não encontrada")
        return None


# ================================================
# Função Auxiliar para Criar Pastas
# ================================================
def criar_pasta(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Pasta criada: {path}")

# ================================================
# Processamento de Dados (mantido)
# ================================================
def processar_arquivos_csv(arquivos_csv):
    dados_agregados = defaultdict(lambda: {
        'vitorias': [],
        'taxa_vitorias': [],
        'pontuacao_media': []
    })
    num_simulacoes = None
    
    for arquivo in arquivos_csv:
        with open(arquivo, 'r') as f:
            linhas = f.readlines()
        
        # Verificar número de simulações
        atual_num_simulacoes = int(linhas[1].split(': ')[1])
        if num_simulacoes is None:
            num_simulacoes = atual_num_simulacoes
        elif atual_num_simulacoes != num_simulacoes:
            print(f"Aviso: Número de simulações inconsistente em {arquivo}")

        # Processar cada linha de jogador
        for linha in linhas[2:]:
            partes = linha.strip().split(',')
            nome_jogador = partes[0]
            vitorias = int(partes[1])
            taxa = float(partes[2])
            pontuacao = float(partes[3])
            
            dados_agregados[nome_jogador]['vitorias'].append(vitorias)
            dados_agregados[nome_jogador]['taxa_vitorias'].append(taxa)
            dados_agregados[nome_jogador]['pontuacao_media'].append(pontuacao)
    
    return dados_agregados, num_simulacoes

def calcular_metricas(dados_agregados):
    metricas = {}
    for jogador, dados in dados_agregados.items():
        metricas[jogador] = {
            'vitorias_media': np.mean(dados['vitorias']),
            'vitorias_std': np.std(dados['vitorias']),
            'taxa_media': np.mean(dados['taxa_vitorias']),
            'taxa_std': np.std(dados['taxa_vitorias']),
            'pontuacao_media': np.mean(dados['pontuacao_media']),
            'pontuacao_std': np.std(dados['pontuacao_media']),
            'cv_vitorias': (np.std(dados['vitorias']) / np.mean(dados['vitorias'])) * 100 if np.mean(dados['vitorias']) > 0 else 0,
        }
    return metricas

# ================================================
# Geração de Gráficos e Tabelas com Nova Estrutura
# ================================================
def gerar_graficos_e_tabelas(dados_agregados, metricas, treino_nome, estrategia_nome, num_simulacoes):
    # Criar caminho seguro para pastas
    estrategia_nome_safe = str(estrategia_nome).replace("(", "").replace(")", "").replace(", ", "_")
    dir_base = os.path.join("graficos", treino_nome, estrategia_nome_safe)
    criar_pasta(dir_base)
    
    jogadores = sorted(dados_agregados.keys(), key=lambda x: (x != 'MCTS', x))
    cores = ['#1f77b4' if j == 'MCTS' else '#2ca02c' for j in jogadores]
    
    # ========== Gráfico de Barras ==========
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        x=jogadores,
        y=[metricas[j]['taxa_media'] for j in jogadores],
        hue=jogadores,
        palette=cores,
        legend=False,
        capsize=0.2
    )
    
    # Adicionar erro manualmente
    taxas_std = [metricas[j]['taxa_std'] for j in jogadores]
    for i, bar in enumerate(ax.patches):
        xpos = bar.get_x() + bar.get_width()/2
        ax.errorbar(xpos, bar.get_height(), yerr=taxas_std[i], color='black', capsize=5, lw=1)
    
    plt.title(f"{treino_nome} vs {estrategia_nome}\nTaxa de Vitórias Média ({num_simulacoes} simulações)")
    plt.xticks(rotation=45)
    plt.ylabel("Taxa de Vitórias")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_base, "barras.png"), dpi=300)
    plt.close()
    
    # ========== Boxplot ==========
    plt.figure(figsize=(12, 6))
    dados_boxplot = [dados_agregados[j]['taxa_vitorias'] for j in jogadores]
    sns.boxplot(data=dados_boxplot, palette=cores)
    plt.xticks(ticks=range(len(jogadores)), labels=jogadores, rotation=45)
    plt.title(f"Distribuição das Taxas de Vitórias\n{treino_nome} vs {estrategia_nome}")
    plt.ylabel("Taxa de Vitórias")
    plt.tight_layout()
    plt.savefig(os.path.join(dir_base, "boxplot.png"), dpi=300)
    plt.close()
    
    # ========== Tabela Resumo ==========
    df = pd.DataFrame.from_dict(metricas, orient='index')
    df = df[['vitorias_media', 'vitorias_std', 'taxa_media', 'taxa_std', 'pontuacao_media', 'pontuacao_std', 'cv_vitorias']]
    df.columns = ['Média Vitórias', 'DP Vitórias', 'Média Taxa', 'DP Taxa', 'Média Pontuação', 'DP Pontuação', 'CV Vitórias (%)']
    df.to_csv(os.path.join(dir_base, "resumo.csv"), float_format="%.3f")

# ================================================
# Loop Principal de Processamento
# ================================================
base_path = './treinos'
resultado = identificar_pastas_e_arquivos(base_path)

for treino, estrategias in resultado.items():
    for estrategia, arquivos in estrategias.items():
        dados_agregados, num_simulacoes = processar_arquivos_csv(arquivos)
        metricas = calcular_metricas(dados_agregados)
        gerar_graficos_e_tabelas(dados_agregados, metricas, treino, estrategia, num_simulacoes)
        print(f"Processado: {treino} > {estrategia}")

print("\nAnálise concluída! Verifique a pasta 'graficos'")


# Exemplo de execução
# base_path = './treinos'
# resultado = identificar_pastas_e_arquivos(base_path)
# for treino, arquivos in resultado.items():
#     print(f"Treino: {treino}")
#     for estrategia, lista_arquivos in arquivos.items():
#         print(f"  Estratégia: {estrategia} -> {len(lista_arquivos)} arquivos")