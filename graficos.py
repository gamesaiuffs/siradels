import matplotlib.pyplot as plt
from database.Postgres import Conexao

def plot_values(y, x):
    plt.figure(figsize=(8, 5))
    plt.plot(y, x, marker='o', linestyle='-')
    plt.xlabel('Timesteps')
    plt.ylabel('Win Rate')
    plt.title('Relation between timesteps and win avarage')
    plt.grid(True)
    plt.show()
    plt.ylim(0, 100)
    plt.savefig("graficos/1.png")

if __name__ == "__main__":
    conexao = Conexao()
    
    # grafico de recompensa 
    # valores = conexao.consultar(
    #     """
    #     select tsteps, avg(avrew) as recompensas
    #     from sample 
    #     where idexp=5
    #     GROUP BY tsteps
    #     order by tsteps;
    #     """)
    
    valores = conexao.consultar(
        """
        select tsteps, avg(nwins) as recompensas
        from sample 
        where idexp=1
        GROUP BY tsteps
        order by tsteps;
        """)
    
    
    y = [float(valor[0]) for valor in valores]
    x = [float(valor[1]) for valor in valores]
    plot_values(y, x)
    # print(valores)
