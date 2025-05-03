import matplotlib.pyplot as plt
from database.Postgres import Conexao
from enum import Enum
import numpy as np
import scipy.stats as stats
class TipoGrafico(Enum):
    VITORIAS=1,
    RECOMPENSA=2,
    PONTUACAO=3,
    INTERVALO_CONFIANCA_VITORIAS=4,
    BARRAS_RECOMPENSA=5,
    



if __name__ == "__main__":
    conexao = Conexao()
    
    tipo = TipoGrafico.INTERVALO_CONFIANCA_VITORIAS
    
    
    if tipo == TipoGrafico.VITORIAS:
        exp1 = conexao.consultar(
            """
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=12
            GROUP BY tsteps
            order by tsteps;
            """)
        exp2 = conexao.consultar(
            """
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=13
            GROUP BY tsteps
            order by tsteps;
            """)
        exp3 = conexao.consultar(
            """
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=14
            GROUP BY tsteps
            order by tsteps;
            """)
        exp4 = conexao.consultar(
            """
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=15
            GROUP BY tsteps
            order by tsteps;
            """)
        exp5 = conexao.consultar(
            """
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=17
            GROUP BY tsteps
            order by tsteps;
            """)
        
        
        # y = [float(valor[0]) for valor in valores]
        # x = [float(valor[1]) for valor in valores]
        # plot_values(y, x)
        # print(valores)
        
        plt.figure(figsize=(10, 6))
        plt.xlabel('Training timesteps')
        plt.ylabel('Win Rate')
        plt.title('Relation between timesteps and win average')
        plt.grid(True)
        
        plt.plot([float(valor[0]) for valor in exp1], [float(valor[1]) for valor in exp1], marker='o', label="Experiment 12")
        plt.plot([float(valor[0]) for valor in exp2], [float(valor[1]) for valor in exp2], marker='o', label="Experiment 13")
        plt.plot([float(valor[0]) for valor in exp3], [float(valor[1]) for valor in exp3], marker='o', label="Experiment 14")
        plt.plot([float(valor[0]) for valor in exp4], [float(valor[1]) for valor in exp4], marker='o', label="Experiment 15")
        plt.plot([float(valor[0]) for valor in exp5], [float(valor[1]) for valor in exp5], marker='o', label="Experiment 17")
        
        plt.ylim(0, 65)
        plt.xlim(0, 300000)
        plt.legend()
        # plt.show()
        plt.savefig("graficos_atualizado/teste_exps_12_13_14_15_16.png")


    elif tipo == TipoGrafico.RECOMPENSA:
        
        exp1 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=1
            GROUP BY tsteps
            order by tsteps;
            """)
        exp2 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=6
            GROUP BY tsteps
            order by tsteps;
            """)
        exp3 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=3
            GROUP BY tsteps
            order by tsteps;
            """)
        exp4 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=4
            GROUP BY tsteps
            order by tsteps;
            """)
        exp5 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=5
            GROUP BY tsteps
            order by tsteps;
            """)
        
        plt.figure(figsize=(10, 6))
        plt.xlabel('Training timesteps')
        plt.ylabel('Reward average')
        plt.title('Relation between timesteps and reward average')
        plt.grid(True)
        
        plt.plot([float(valor[0]) for valor in exp1], [float(valor[1]) for valor in exp1], marker='o', label="Experiment 1")
        plt.plot([float(valor[0]) for valor in exp2], [float(valor[1]) for valor in exp2], marker='o', label="Experiment 2")
        plt.plot([float(valor[0]) for valor in exp3], [float(valor[1]) for valor in exp3], marker='o', label="Experiment 3")
        plt.plot([float(valor[0]) for valor in exp4], [float(valor[1]) for valor in exp4], marker='o', label="Experiment 4")
        plt.plot([float(valor[0]) for valor in exp5], [float(valor[1]) for valor in exp5], marker='o', label="Experiment 5")

        plt.legend()
        plt.savefig("graficos_atualizado/exp_1a5_media_recompensas.png")


    elif tipo == TipoGrafico.INTERVALO_CONFIANCA_VITORIAS:
        
        timestep = 300000
        
        fig = plt.figure(figsize=(10, 6))
        plt.xlabel('Experiments')
        plt.ylabel('Win Rate')
        plt.title(f'Win Rate at {timestep} training timesteps and 90% confidence interval')
        # plt.grid(True)
        
        exp1 = conexao.consultar(
            """
            
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=1
            GROUP BY tsteps
            order by tsteps;
            """)
        exp2 = conexao.consultar(
            """
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=6
            GROUP BY tsteps
            order by tsteps;
            """)
        exp3 = conexao.consultar(
            """
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=3
            GROUP BY tsteps
            order by tsteps;
            """)
        exp4 = conexao.consultar(
            """
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=4
            GROUP BY tsteps
            order by tsteps;
            """)
        exp5 = conexao.consultar(
            """
            select tsteps, avg(nwins) as recompensas
            from sample 
            where idexp=5
            GROUP BY tsteps
            order by tsteps;
            """)
        
        experiments = [float(exp1[timestep // 10000 - 1][1]), float(exp2[timestep // 10000 - 1][1]), float(exp3[timestep // 10000 - 1][1]), float(exp4[timestep // 10000 - 1][1]), float(exp5[timestep // 10000 - 1][1])]
        labels = ["1", "2", "3", "4", "5"]
        
        print("valores usados nos itervalos:")
                
        # Videos de referência:
        # https://www.youtube.com/watch?v=CGF9YnkNul8
        # https://www.youtube.com/watch?v=nrl--O0c9SI
        
        error_values_exp1 = conexao.consultar(
            """
            select avscore as recompensas
            from sample 
            where idexp=1 and tsteps=300000
            order by tsteps;
            """)
        error_values_exp1 = [float(value[0]) for value in error_values_exp1]
        print("1: ", error_values_exp1)
        # media_exp1 = np.mean(error_values_exp1)
        # dp_exp1 = np.std(error_values_exp1, ddof=1)
        # n_exp1 = len(error_values_exp1)
        # sem_exp1 = dp_exp1 / np.sqrt(n_exp1)
        # intv_exp1 = stats.norm.interval(0.90, loc=media_exp1, scale=sem_exp1)
        intv_exp1 = stats.norm.interval(0.90, loc=np.mean(error_values_exp1), scale=stats.sem(error_values_exp1))

        # Experimento 2 (retreinado e identificado na base como idexp=6)
        error_values_exp2 = conexao.consultar(
            """
            select avscore as recompensas
            from sample 
            where idexp=6 and tsteps=300000
            order by tsteps;
            """)
        error_values_exp2 = [float(value[0]) for value in error_values_exp2]
        # print("2: ", error_values_exp2)
        # media_exp2 = np.mean(error_values_exp2)
        # dp_exp2 = np.std(error_values_exp2, ddof=1)
        # n_exp2 = len(error_values_exp2)
        # sem_exp2 = dp_exp2 / np.sqrt(n_exp2)
        # intv_exp2 = stats.norm.interval(0.90, loc=media_exp2, scale=sem_exp2)
        intv_exp2 = stats.norm.interval(0.90, loc=np.mean(error_values_exp2), scale=stats.sem(error_values_exp2))
        

        # Experimento 3 
        error_values_exp3 = conexao.consultar(
            """
            select avscore as recompensas
            from sample 
            where idexp=3 and tsteps=300000
            order by tsteps;
            """)
        error_values_exp3 = [float(value[0]) for value in error_values_exp3]
        # print("3: ", error_values_exp3)
        # media_exp3 = np.mean(error_values_exp3)
        # dp_exp3 = np.std(error_values_exp3, ddof=1)
        # n_exp3 = len(error_values_exp3)
        # sem_exp3 = dp_exp3 / np.sqrt(n_exp3)
        # intv_exp3 = stats.norm.interval(0.90, loc=media_exp3, scale=sem_exp3)
        intv_exp3 = stats.norm.interval(0.90, loc=np.mean(error_values_exp3), scale=stats.sem(error_values_exp3))
        

        # Experimento 4 
        error_values_exp4 = conexao.consultar(
            """
            select avscore as recompensas
            from sample 
            where idexp=4 and tsteps=300000
            order by tsteps;
            """)
        error_values_exp4 = [float(value[0]) for value in error_values_exp4]
        # print("4: ", error_values_exp4)
        # media_exp4 = np.mean(error_values_exp4)
        # dp_exp4 = np.std(error_values_exp4, ddof=1)
        # n_exp4 = len(error_values_exp4)
        # sem_exp4 = dp_exp4 / np.sqrt(n_exp4)
        # intv_exp4 = stats.norm.interval(0.90, loc=media_exp4, scale=sem_exp4)
        intv_exp4 = stats.norm.interval(0.90, loc=np.mean(error_values_exp4), scale=stats.sem(error_values_exp4))
        

        # Experimento 5
        error_values_exp5 = conexao.consultar(
            """
            select avscore as recompensas
            from sample 
            where idexp=5 and tsteps=300000
            order by tsteps;
            """)
        error_values_exp5 = [float(value[0]) for value in error_values_exp5]
        # print("5: ", error_values_exp5)
        # media_exp5 = np.mean(error_values_exp5)
        # dp_exp5 = np.std(error_values_exp5, ddof=1)
        # n_exp5 = len(error_values_exp5)
        # sem_exp5 = dp_exp5 / np.sqrt(n_exp5)
        # intv_exp5 = stats.norm.interval(0.90, loc=media_exp5, scale=sem_exp5)
        intv_exp5 = stats.norm.interval(0.90, loc=np.mean(error_values_exp5), scale=stats.sem(error_values_exp5))
        
        
        # print(media_exp1)
        # print(dp_exp1)
        # print(n_exp1)
        
        dy = [
            np.mean(error_values_exp1) - intv_exp1[0], 
            np.mean(error_values_exp2) - intv_exp2[0], 
            np.mean(error_values_exp3) - intv_exp3[0], 
            np.mean(error_values_exp4) - intv_exp4[0], 
            np.mean(error_values_exp5) - intv_exp5[0], 
        ]
        
        print("intervalos de confiança:")
        print(dy)
        
        plt.bar(labels, experiments, yerr=dy, color="lightgray", ec="black", ecolor="red", capsize=5)
        plt.ylim(50, 57)
        # plt.plot([0, 6], [54, 54], "-k")
        
        # print(dy)
        
        plt.savefig(f"graficos_atualizado/exp_1a5_barras_nwins_{timestep}.png")
        
        
    elif tipo == TipoGrafico.BARRAS_RECOMPENSA:
        timestep = 110000
        
        plt.figure(figsize=(10, 6))
        plt.xlabel('Experiments')
        plt.ylabel('Win Rate')
        plt.title(f'Win Rate at {timestep} timesteps')
        # plt.grid(True)
        
        exp1 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=1
            GROUP BY tsteps
            order by tsteps;
            """)
        exp2 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=6
            GROUP BY tsteps
            order by tsteps;
            """)
        exp3 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=3
            GROUP BY tsteps
            order by tsteps;
            """)
        exp4 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=4
            GROUP BY tsteps
            order by tsteps;
            """)
        exp5 = conexao.consultar(
            """
            select tsteps, avg(avrew) as recompensas
            from sample 
            where idexp=5
            GROUP BY tsteps
            order by tsteps;
            """)
        
        experiments = [float(exp1[timestep // 10000 - 1][1]), float(exp2[timestep // 10000 - 1][1]), float(exp3[timestep // 10000 - 1][1]), float(exp4[timestep // 10000 - 1][1]), float(exp5[timestep // 10000 - 1][1])]
        # experiments = [exp1, exp2, exp3, exp4, exp5]
        labels = ["exp1", "exp2", "exp3", "exp4", "exp5"]
        
        print(experiments)
        # print(exp1)
        
        plt.bar(labels, experiments)
        if max(experiments) > 0:
            plt.ylim(0, max(experiments) + 10)
        else: 
            plt.ylim(min(experiments) - 30, 0)
        plt.savefig(f"graficos_atualizado/exp_1a5_barras_rew_{timestep}stp.png")