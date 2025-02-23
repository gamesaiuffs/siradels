import matplotlib.pyplot as plt
from database.Postgres import Conexao
from enum import Enum

class TipoGrafico(Enum):
    VITORIAS=1,
    RECOMPENSA=2,
    PONTUACAO=3,
    BARRAS_WINRATE=4,
    BARRAS_RECOMPENSA=5,
    



if __name__ == "__main__":
    conexao = Conexao()
    
    tipo = TipoGrafico.BARRAS_RECOMPENSA
    
    
    if tipo == TipoGrafico.RECOMPENSA:
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
            where idexp=2
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
        
        
        # y = [float(valor[0]) for valor in valores]
        # x = [float(valor[1]) for valor in valores]
        # plot_values(y, x)
        # print(valores)
        
        plt.figure(figsize=(10, 6))
        plt.xlabel('Training timesteps')
        plt.ylabel('Win Rate')
        plt.title('Relation between timesteps and win average')
        plt.grid(True)
        
        plt.plot([float(valor[0]) for valor in exp1], [float(valor[1]) for valor in exp1], marker='o', label="Experiment 1")
        plt.plot([float(valor[0]) for valor in exp2], [float(valor[1]) for valor in exp2], marker='o', label="Experiment 2")
        plt.plot([float(valor[0]) for valor in exp3], [float(valor[1]) for valor in exp3], marker='o', label="Experiment 3")
        plt.plot([float(valor[0]) for valor in exp4], [float(valor[1]) for valor in exp4], marker='o', label="Experiment 4")
        plt.plot([float(valor[0]) for valor in exp5], [float(valor[1]) for valor in exp5], marker='o', label="Experiment 5")
        
        plt.ylim(35, 65)
        plt.xlim(75000, 300000)
        plt.legend()
        # plt.show()
        plt.savefig("graficos/exp_1a5_media_vitorias_35_65.png")


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
            where idexp=2
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
        plt.savefig("graficos/exp_1a5_media_recompensas.png")


    elif tipo == TipoGrafico.BARRAS_WINRATE:
        
        timestep = 170000
        
        plt.figure(figsize=(10, 6))
        plt.xlabel('Experiments')
        plt.ylabel('Win Rate')
        plt.title(f'Win Rate at {timestep} timesteps')
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
            where idexp=2
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
        # experiments = [exp1, exp2, exp3, exp4, exp5]
        labels = ["exp1", "exp2", "exp3", "exp4", "exp5"]
        
        print(experiments)
        # print(exp1)
        
        plt.bar(labels, experiments)
        plt.ylim(0, 65)
        plt.savefig(f"graficos/exp_1a5_barras_nwins_{timestep}stp.png")
        
        
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
            where idexp=2
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
        plt.savefig(f"graficos/exp_1a5_barras_rew_{timestep}stp.png")