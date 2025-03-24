import numpy as np
import scipy.stats as stats
import sys

timestep = 300000

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Passe os argumentos [python <file.py> <valores>]")
        sys.exit(1)

    values = list(map(float, sys.argv[1:]))

    media_exp1 = np.mean(values)
    dp_exp1 = np.std(values, ddof=1)
    n_exp1 = len(values)
    sem_exp1 = dp_exp1 / np.sqrt(n_exp1)
    intv_exp1 = stats.norm.interval(0.90, loc=media_exp1, scale=sem_exp1)

    print("Intervalo", intv_exp1)
    print("Média: ", media_exp1)
    print("Int. conf.: ", media_exp1 - intv_exp1[0])
