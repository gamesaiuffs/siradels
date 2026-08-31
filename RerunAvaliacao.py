# -*- coding: utf-8 -*-
from classes.classification.ClassificaEstados import ClassificaEstados, carregar_best_params
from classes.classification.AnaliseResultados import AnaliseResultados

n_features = 30
data = "2026-03-26"
jogos_base = f"Jogos {n_features}f {data}"
rotulos_base = f"Rótulos {n_features}f {data}"

jogos = jogos_base + "por_round"
rotulos = rotulos_base + "por_round"

# -------------------------------------------------------
# 1) RECÁLCULO DOS MODELOS SOB O PIPELINE ATUAL
# -------------------------------------------------------
# Os arquivos em results/evaluation/*_evaluation.pkl (CART/RF/XGB/LOGREG/MLP) foram gerados antes
# do commit 489110d (2026-04-06), que corrigiu um bug em _balance_fold_classes_by_swapping: o
# código antigo verificava rótulos [1,2,3,4,5], mas o dataset sempre usa [0,1,2,3,4], então o
# balanceamento de classes por fold nunca era executado. Os novos baselines heurísticos (RANDOM,
# MOST_DISTRICTS, HIGHEST_SCORE) já usam o pipeline corrigido, então os modelos supervisionados
# precisam ser recalculados para ficarem comparáveis (pré-requisito do Comentário 5). Reaproveita
# os hiperparâmetros do Optuna, sem nova busca.

print("\n===== RECÁLCULO DOS MODELOS (pipeline corrigido) =====\n")

best_cart = carregar_best_params("CART")
best_rf = carregar_best_params("RF")
best_xgb = carregar_best_params("XGB")
best_mlp = carregar_best_params("MLP")

ClassificaEstados.treinar_e_avaliar_CART(jogos, rotulos, best_cart)
ClassificaEstados.treinar_e_avaliar_RF(jogos, rotulos, best_rf)
ClassificaEstados.treinar_e_avaliar_XGB(jogos, rotulos, best_xgb)
ClassificaEstados.treinar_e_avaliar_MLP(jogos, rotulos, best_mlp)
ClassificaEstados.treinar_regressao_logistica(jogos, rotulos, nome_modelo="LOGREG", class_weight="balanced")

print("\n===== RECÁLCULO POR ESTÁGIO DE PROGRESSO =====\n")

ClassificaEstados.treinar_e_avaliar_progress_CART(jogos, rotulos)
ClassificaEstados.treinar_e_avaliar_progress_RF(jogos, rotulos)
ClassificaEstados.treinar_e_avaliar_progress_XGB(jogos, rotulos)
ClassificaEstados.treinar_e_avaliar_progress_MLP(jogos, rotulos)
ClassificaEstados.treinar_e_avaliar_progress_LogReg(jogos, rotulos)

# -------------------------------------------------------
# 2) ABLAÇÕES DE FEATURES (Comentário 3 e Reviewer 5)
# -------------------------------------------------------
# NO_HISTORY remove as 50 colunas cumulativas de papel/interação (times_killed, times_robbed,
# role_rank_1..8 por jogador) que podem funcionar como impressão digital da política do agente.
# NO_GAP remove as 20 colunas de gap relativo ao líder (gold/hand/built/city_cost_diff_max por
# jogador), que podem estar entregando a resposta pronta ao modelo (Reviewer 5).
# Rodado para XGB (modelo sob disputa) e LOGREG (concorrente mais próximo no Comentário 5).

logreg_params = {"class_weight": "balanced"}

print("\n===== ABLAÇÃO NO_HISTORY =====\n")

ClassificaEstados.treinar_e_avaliar_ablation(jogos, rotulos, best_xgb, "XGB", "NO_HISTORY")
ClassificaEstados.treinar_e_avaliar_progress_ablation(jogos, rotulos, "XGB", "NO_HISTORY")

ClassificaEstados.treinar_e_avaliar_ablation(jogos, rotulos, logreg_params, "LOGREG", "NO_HISTORY")
ClassificaEstados.treinar_e_avaliar_progress_ablation(jogos, rotulos, "LOGREG", "NO_HISTORY")

print("\n===== ABLAÇÃO NO_GAP =====\n")

ClassificaEstados.treinar_e_avaliar_ablation(jogos, rotulos, best_xgb, "XGB", "NO_GAP")
ClassificaEstados.treinar_e_avaliar_progress_ablation(jogos, rotulos, "XGB", "NO_GAP")

ClassificaEstados.treinar_e_avaliar_ablation(jogos, rotulos, logreg_params, "LOGREG", "NO_GAP")
ClassificaEstados.treinar_e_avaliar_progress_ablation(jogos, rotulos, "LOGREG", "NO_GAP")

# -------------------------------------------------------
# 3) TESTES PAREADOS (Comentário 5)
# -------------------------------------------------------

print("\n===== TESTES PAREADOS =====\n")

AnaliseResultados.testes_pareados(
    ["XGB", "RF", "LOGREG", "CART", "MLP", "HIGHEST_SCORE", "MOST_DISTRICTS", "RANDOM"],
    filenames={"LOGREG": "LogReg_evaluation_LOGREG.pkl"}
)

print("\n===== CONCLUÍDO =====\n")
