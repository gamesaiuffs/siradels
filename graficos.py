import matplotlib.pyplot as plt
from database.Postgres import Conexao
from enum import Enum

class TipoGrafico(Enum):
    VITORIAS=1,
    RECOMPENSA=2,
    PONTUACAO=3
    



if __name__ == "__main__":
    conexao = Conexao()
    
    tipo = TipoGrafico.RECOMPENSA
    
    
    if tipo == TipoGrafico.VITORIAS:
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
        plt.xlabel('Timesteps')
        plt.ylabel('Win Rate')
        plt.title('Relation between timesteps and win avarage')
        plt.grid(True)
        
        plt.plot([float(valor[0]) for valor in exp1], [float(valor[1]) for valor in exp1], marker='o', label="Experimento 1")
        plt.plot([float(valor[0]) for valor in exp2], [float(valor[1]) for valor in exp2], marker='o', label="Experimento 2")
        plt.plot([float(valor[0]) for valor in exp3], [float(valor[1]) for valor in exp3], marker='o', label="Experimento 3")
        plt.plot([float(valor[0]) for valor in exp4], [float(valor[1]) for valor in exp4], marker='o', label="Experimento 4")
        plt.plot([float(valor[0]) for valor in exp5], [float(valor[1]) for valor in exp5], marker='o', label="Experimento 5")
        
        plt.ylim(0, 70)
        plt.legend()
        # plt.show()
        plt.ylim(0, 100)
        plt.savefig("graficos/geral.png")


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
        plt.xlabel('Timesteps')
        plt.ylabel('Win Rate')
        plt.title('Relation between timesteps and win avarage')
        plt.grid(True)
        
        plt.plot([float(valor[0]) for valor in exp1], [float(valor[1]) for valor in exp1], marker='o', label="Experimento 1")
        plt.plot([float(valor[0]) for valor in exp2], [float(valor[1]) for valor in exp2], marker='o', label="Experimento 2")
        plt.plot([float(valor[0]) for valor in exp3], [float(valor[1]) for valor in exp3], marker='o', label="Experimento 3")
        plt.plot([float(valor[0]) for valor in exp4], [float(valor[1]) for valor in exp4], marker='o', label="Experimento 4")
        plt.plot([float(valor[0]) for valor in exp5], [float(valor[1]) for valor in exp5], marker='o', label="Experimento 5")
        
        # plt.ylim(0, 70)
        plt.legend()
        # plt.show()
        # plt.ylim(0, 100)
        plt.savefig("graficos/geral.png")
