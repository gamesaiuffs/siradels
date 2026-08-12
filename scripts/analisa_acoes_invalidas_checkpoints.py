"""
Analisa a taxa de escolhas invalidas de personagens em modelos salvos.

O script carrega checkpoints intermediarios dos experimentos e roda partidas
completas contra bots aleatorios. Em cada fase de escolha de personagem, ele
conta quantas vezes o modelo sugeriu uma carta indisponivel antes de finalmente
selecionar uma carta valida.

As configuracoes principais ficam nas constantes abaixo.
"""

from __future__ import annotations

import csv
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

import numpy as np
from stable_baselines3 import DQN, PPO

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import classes.model.Estado as estado_module
import scripts.represents as represents_module
from classes.Experimento import Experimento
from classes.enum.TipoAcao import TipoAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador
from classes.strategies.Estrategia import Estrategia
from classes.strategies.EstrategiaTotalmenteAleatoria import EstrategiaTotalmenteAleatoria


# ---------------------------------------------------------------------------
# Configuracoes
# ---------------------------------------------------------------------------

BASE_DIR = Path("aaa_experimentos_final")
OUTPUT_DIR = Path("analises_acoes_invalidas")
OUTPUT_CSV = OUTPUT_DIR / "acoes_invalidas_checkpoints.csv"
SUMMARY_CSV = OUTPUT_DIR / "acoes_invalidas_resumo.csv"

NUM_INITS = 10
CHECKPOINTS = range(1, 31)
NUM_EPISODES = 100

# deterministic=False reproduz melhor a avaliacao atual com Agente.
# deterministic=True mede a acao principal da politica aprendida.
DETERMINISTIC_MODES = [False, True]

MAX_INVALID_ATTEMPTS_PER_CHOICE = 1000
RANDOM_SEED = 12345


@dataclass(frozen=True)
class ExperimentConfig:
    idexp: int
    label: str
    representation_name: str
    representation: list[str]
    model_class: type[PPO] | type[DQN]


EXPERIMENTS = [
    ExperimentConfig(
        idexp=31,
        label="PPO - original cru",
        representation_name="original",
        representation=represents_module.variaveis_original,
        model_class=PPO,
    ),
    ExperimentConfig(
        idexp=32,
        label="PPO - original limitado",
        representation_name="padrao",
        representation=represents_module.variaveis_padrao,
        model_class=PPO,
    ),
    ExperimentConfig(
        idexp=33,
        label="PPO - proporcoes",
        representation_name="proporcoes",
        representation=represents_module.proporcoes,
        model_class=PPO,
    ),
    ExperimentConfig(
        idexp=34,
        label="PPO - 3 classes",
        representation_name="classes",
        representation=represents_module.variaveis_classes,
        model_class=PPO,
    ),
    ExperimentConfig(
        idexp=35,
        label="PPO - binario",
        representation_name="binario",
        representation=represents_module.variaveis_classes_bin,
        model_class=PPO,
    ),
]


# ---------------------------------------------------------------------------
# Infra de avaliacao
# ---------------------------------------------------------------------------

def aplicar_representacao(representation: list[str]) -> None:
    """Atualiza a representacao global usada por Estado.converter_estado()."""
    represents_module.REPRESENT = representation
    estado_module.REPRESENT = representation


class AgenteContadorInvalidas(Estrategia):
    def __init__(
        self,
        model,
        deterministic: bool,
        nome: str = "Agente",
        imprimir: bool = False,
    ):
        super().__init__(nome, imprimir)
        self.model = model
        self.deterministic = deterministic
        self.total_choices = 0
        self.total_predictions = 0
        self.total_invalid_predictions = 0
        self.first_choice_invalid = 0
        self.invalid_attempts_per_choice: list[int] = []
        self.capped_choices = 0

    def escolher_personagem(self, estado: Estado) -> int:
        invalid_attempts = 0

        while True:
            obs = np.array(estado.converter_estado(openaigym=True))
            action, _ = self.model.predict(obs, deterministic=self.deterministic)
            action = int(action)
            self.total_predictions += 1

            idx_escolha_personagem = self._idx_personagem_disponivel(estado, action)
            if idx_escolha_personagem != -1:
                self.total_choices += 1
                self.total_invalid_predictions += invalid_attempts
                self.invalid_attempts_per_choice.append(invalid_attempts)
                if invalid_attempts > 0:
                    self.first_choice_invalid += 1
                return idx_escolha_personagem

            invalid_attempts += 1

            if invalid_attempts >= MAX_INVALID_ATTEMPTS_PER_CHOICE:
                self.capped_choices += 1
                self.total_choices += 1
                self.total_invalid_predictions += invalid_attempts
                self.invalid_attempts_per_choice.append(invalid_attempts)
                if invalid_attempts > 0:
                    self.first_choice_invalid += 1
                return random.randrange(len(estado.tabuleiro.baralho_personagens))

    @staticmethod
    def _idx_personagem_disponivel(estado: Estado, action: int) -> int:
        for idx, personagem in enumerate(estado.tabuleiro.baralho_personagens):
            if action == personagem.rank - 1:
                return idx
        return -1

    @staticmethod
    def escolher_acao(estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        acao_escolhida = random.randint(0, len(acoes_disponiveis) - 1)
        while len(acoes_disponiveis) > 1 and acoes_disponiveis[acao_escolhida] == TipoAcao.PassarTurno:
            acao_escolhida = random.randint(0, len(acoes_disponiveis) - 1)
        return acao_escolhida

    @staticmethod
    def coletar_cartas(estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        return random.randint(0, qtd_cartas - 1)

    @staticmethod
    def construir_distrito(
        estado: Estado,
        distritos_para_construir: list[CartaDistrito],
        distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)],
    ) -> int:
        tamanho_maximo = len(distritos_para_construir) + len(distritos_para_construir_covil_ladroes)
        return random.randint(0, tamanho_maximo - 1)

    @staticmethod
    def construir_distrito_covil_dos_ladroes(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    @staticmethod
    def habilidade_assassina(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    @staticmethod
    def habilidade_ladrao(estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        return random.randint(0, len(opcoes_personagem) - 1)

    @staticmethod
    def habilidade_ilusionista_trocar(estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        return random.randint(0, len(opcoes_jogadores) - 1)

    @staticmethod
    def habilidade_ilusionista_descartar_qtd_cartas(estado: Estado, qtd_maxima: int) -> int:
        return random.randint(1, qtd_maxima)

    @staticmethod
    def habilidade_ilusionista_descartar_carta(estado: Estado, qtd_cartas: int, i: int) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)

    @staticmethod
    def habilidade_senhor_da_guerra_destruir(estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        return random.randint(0, len(distritos_para_destruir) - 1)

    @staticmethod
    def laboratorio(estado: Estado) -> int:
        return random.randint(0, len(estado.jogador_atual.cartas_distrito_mao) - 1)


def caminho_checkpoint(config: ExperimentConfig, init: int, checkpoint: int) -> Path:
    return BASE_DIR / str(config.idexp) / f"in_{init}" / f"{checkpoint}.zip"


def avaliar_checkpoint(
    config: ExperimentConfig,
    init: int,
    checkpoint: int,
    deterministic: bool,
) -> dict[str, int | float | str]:
    model_path = caminho_checkpoint(config, init, checkpoint)
    model = config.model_class.load(model_path)
    agente = AgenteContadorInvalidas(model=model, deterministic=deterministic)

    estrategias = [
        agente,
        EstrategiaTotalmenteAleatoria("Bot 1"),
        EstrategiaTotalmenteAleatoria("Bot 2"),
        EstrategiaTotalmenteAleatoria("Bot 3"),
        EstrategiaTotalmenteAleatoria("Bot 4"),
    ]

    vitorias, pontuacao_media = Experimento.testar_estrategias_graficos(
        estrategias,
        NUM_EPISODES,
        True,
    )

    invalid_rate = agente.total_invalid_predictions / agente.total_predictions if agente.total_predictions else 0.0
    first_invalid_rate = agente.first_choice_invalid / agente.total_choices if agente.total_choices else 0.0
    avg_invalid_before_valid = mean(agente.invalid_attempts_per_choice) if agente.invalid_attempts_per_choice else 0.0
    max_invalid_before_valid = max(agente.invalid_attempts_per_choice) if agente.invalid_attempts_per_choice else 0

    return {
        "idexp": config.idexp,
        "label": config.label,
        "representation": config.representation_name,
        "init": init,
        "checkpoint": checkpoint,
        "tsteps": checkpoint * 10000,
        "deterministic": deterministic,
        "episodes": NUM_EPISODES,
        "wins": vitorias,
        "win_rate": vitorias / NUM_EPISODES,
        "avg_score": pontuacao_media,
        "choices": agente.total_choices,
        "predictions": agente.total_predictions,
        "invalid_predictions": agente.total_invalid_predictions,
        "invalid_prediction_rate": invalid_rate,
        "first_choice_invalid": agente.first_choice_invalid,
        "first_choice_invalid_rate": first_invalid_rate,
        "avg_invalid_before_valid": avg_invalid_before_valid,
        "max_invalid_before_valid": max_invalid_before_valid,
        "capped_choices": agente.capped_choices,
    }


def agregar_resumo(rows: list[dict[str, int | float | str]]) -> list[dict[str, int | float | str]]:
    grupos: dict[tuple[int, str, int, bool], list[dict[str, int | float | str]]] = {}
    for row in rows:
        key = (
            int(row["idexp"]),
            str(row["label"]),
            int(row["checkpoint"]),
            bool(row["deterministic"]),
        )
        grupos.setdefault(key, []).append(row)

    resumo = []
    for (idexp, label, checkpoint, deterministic), grupo in sorted(grupos.items()):
        resumo.append(
            {
                "idexp": idexp,
                "label": label,
                "checkpoint": checkpoint,
                "tsteps": checkpoint * 10000,
                "deterministic": deterministic,
                "num_inits": len(grupo),
                "mean_win_rate": mean(float(row["win_rate"]) for row in grupo),
                "mean_invalid_prediction_rate": mean(float(row["invalid_prediction_rate"]) for row in grupo),
                "mean_first_choice_invalid_rate": mean(float(row["first_choice_invalid_rate"]) for row in grupo),
                "mean_avg_invalid_before_valid": mean(float(row["avg_invalid_before_valid"]) for row in grupo),
                "max_invalid_before_valid": max(int(row["max_invalid_before_valid"]) for row in grupo),
                "total_capped_choices": sum(int(row["capped_choices"]) for row in grupo),
            }
        )

    return resumo


def salvar_csv(path: Path, rows: list[dict[str, int | float | str]]) -> None:
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    rows = []
    for config in EXPERIMENTS:
        aplicar_representacao(config.representation)
        print(f"Experimento {config.idexp}: {config.label}")

        for deterministic in DETERMINISTIC_MODES:
            mode = "deterministic" if deterministic else "stochastic"
            print(f"  Modo: {mode}")

            for init in range(1, NUM_INITS + 1):
                for checkpoint in CHECKPOINTS:
                    model_path = caminho_checkpoint(config, init, checkpoint)
                    if not model_path.exists():
                        print(f"    Pulando ausente: {model_path}")
                        continue

                    row = avaliar_checkpoint(config, init, checkpoint, deterministic)
                    rows.append(row)
                    print(
                        "    "
                        f"in_{init:02d} ckpt {checkpoint:02d}: "
                        f"invalid={row['invalid_prediction_rate']:.3f} "
                        f"first_invalid={row['first_choice_invalid_rate']:.3f} "
                        f"wins={row['wins']}"
                    )

    salvar_csv(OUTPUT_CSV, rows)
    salvar_csv(SUMMARY_CSV, agregar_resumo(rows))

    print(f"\nResultados detalhados: {OUTPUT_CSV}")
    print(f"Resumo por experimento/checkpoint: {SUMMARY_CSV}")


if __name__ == "__main__":
    main()
