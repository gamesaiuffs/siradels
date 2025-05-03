create table if not exists experiment (
    idexp NUMERIC PRIMARY KEY,
    title varchar(40),
    numpt numeric not NULL,
    status varchar(10) not null check (status in ('pendente', 'concluido'))
);

create table initialize (
    idin numeric not null,
    status varchar(10) not null check (status in ('pendente', 'concluido')),
    idexp numeric not null,
    constraint pk_init PRIMARY KEY (idin, idexp),
    constraint pk_init_exp FOREIGN KEY (idexp) REFERENCES experiment(idexp) on delete cascade
);

create table sample (
    id_sample numeric not null,
    idin numeric not null,
    idexp numeric not null, 
    avscore NUMERIC(5, 2) not null,
    avrew NUMERIC not null,
    tsteps numeric not null,
    nwins numeric not null,
    constraint pk_sample PRIMARY KEY (id_sample, idin, idexp),
    constraint fk_sample_init FOREIGN KEY (idin, idexp) REFERENCES initialize(idin, idexp) on delete cascade
);

insert into experiment(idexp, title, numpt, status) values (6, 'entradas padrao - substitui o exp2', 300000, 'pendente');
-- delete from experiment where idexp = 3;

-- CREATE TABLE experiment_statistics (
--     id SERIAL PRIMARY KEY, -- Identificador único do experimento
--     id_permutation INT NOT NULL, -- Identificador da permutação associada ao experimento
--     mean_score NUMERIC(5, 2), -- Média das pontuações obtidas em todas as amostras
--     std_score NUMERIC(5, 2), -- Desvio padrão das pontuações
--     ci_score NUMERIC(5, 2), -- Intervalo de confiança das pontuações
--     mean_reward NUMERIC(5, 2), -- Média das recompensas obtidas em todas as amostras
--     std_reward NUMERIC(5, 2), -- Desvio padrão das recompensas
--     ci_reward NUMERIC(5, 2), -- Intervalo de confiança das recompensas
--     mean_t_steps NUMERIC(5, 2), -- Média dos passos realizados em todas as amostras
--     std_t_steps NUMERIC(5, 2), -- Desvio padrão dos passos realizados
--     ci_t_steps NUMERIC(5, 2), -- Intervalo de confiança dos passos realizados
--     FOREIGN KEY (id_permutation) REFERENCES experiment_permutation(id) ON DELETE CASCADE -- Relacionamento com a permutação associada
-- );


--------------------------------------------------------



CREATE TABLE variable (
    id_variable SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE variable_representation (
    id_representation SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL,
    id_variable INT NOT NULL,
    FOREIGN KEY (id_variable) REFERENCES variable(id_variable) ON DELETE CASCADE
);

CREATE TABLE permutation_representation (
    id_permutation INT NOT NULL,
    id_representation INT NOT NULL,
    PRIMARY KEY (id_permutation, id_representation),
    FOREIGN KEY (id_permutation) REFERENCES experiment_permutation(id_permutation) ON DELETE CASCADE,
    FOREIGN KEY (id_representation) REFERENCES variable_representation(id_representation) ON DELETE CASCADE
);


-- Pós calculada 
CREATE TABLE experiment_statistics (
    -- id_experiment SERIAL PRIMARY KEY, -- Identificador único do experimento
    id_permutation INT NOT NULL, -- Identificador da permutação associada ao experimento
    mean_score NUMERIC(5, 2), -- Média das pontuações obtidas em todas as amostras
    std_score NUMERIC(5, 2), -- Desvio padrão das pontuações
    ci_score NUMERIC(5, 2), -- Intervalo de confiança das pontuações
    mean_reward NUMERIC(5, 2), -- Média das recompensas obtidas em todas as amostras
    std_reward NUMERIC(5, 2), -- Desvio padrão das recompensas
    ci_reward NUMERIC(5, 2), -- Intervalo de confiança das recompensas
    mean_t_steps NUMERIC(5, 2), -- Média dos passos realizados em todas as amostras
    std_t_steps NUMERIC(5, 2), -- Desvio padrão dos passos realizados
    ci_t_steps NUMERIC(5, 2), -- Intervalo de confiança dos passos realizados
    FOREIGN KEY (id_permutation) REFERENCES experiment_permutation(id_permutation) ON DELETE CASCADE -- Relacionamento com a permutação associada
);



drop table round;
drop table initialize;
drop table experiment;

insert into experiments values (1, 100, '2024-12-12', )

# Pegar valor de todos pelo máximo atingido 
select idin, max(nwins)
from sample
where idexp=3
group by idin
order by idin;

# Média do maximo atingido em todas as inicializações 
select avg(max) from (select idin, max(nwins) from sample where idexp=5 group by idin order by idin);


# Pegar vitorias de cada inicialização em 300000 steps
select idin, nwins 
from sample 
where idexp=5 and tsteps = 300000;

55 52 47 47 51 49 62 58 45 57

select stddev(nwins) from (select idin, nwins 
from sample 
where idexp=6 and tsteps = 300000
);

# Médias das inicializações de cada experimento
# experimento   % win
# 1             54.5%
# 2             52.80             
# 3             53.20
# 4             54.00
# 5             52.30


# Media do valor de todas as inicializações para cada timestep 
select tsteps, avg(nwins) as vitorias
from sample 
where idexp=10
GROUP BY tsteps
order by tsteps;


# Media da recompensa de todas as inicializações para cada timestep 
select tsteps, avg(avrew) as recompensas
from sample 
where idexp=5
GROUP BY tsteps
order by tsteps;


select avg(nwins) as media_vitorias from sample where idexp=21 and tsteps = 300000;

# Resultados dos experimentos 

#Experimento 1
# experimento   % vitoria   representação               ambiente
# 1             54.5%       originais                   box
# 2             52.80       original limitado           multidiscreto
# 3             53.20       proporções                  box
# 4             54.00       3 classes                   multidiscreto
# 5             52.30       2 classes (binario)         binario


# Experimento variando variáveis usadas (com representação binária) - preliminares 

# Ambiente binario sem alteraçõe 
# 53%

# Só as 9 ultimas (sem num de ouros e cartas distrito do personagem)
# 35% 

# Sem o vetor de disponibilidade 
# 26%

# Experimento 2 - removendo variáveis - representação original 

# variavel removida        media vitorias (%)                                                       
# ouro_personagem          54.8
# cartas_personagem        51.6



select * from sample where idexp=5; 





# Media da recompensa de todas as inicializações para cada timestep 
select avscore as recompensas
from sample 
where idexp=1 and tsteps=300000
order by tsteps;

# exp 1 - tstep 300000 - pontuação média
# 20.29, 19.99, 20.58, 23.19, 22.08, 21.93, 22.14, 21.86, 22.15, 22.33
# Média:  21.654
# Desvio padrão: 1.020971215
# Variação: 1.042382222 
# Lim inferior 21.123
# Lim superior: 22.185
#Margem de erro: 0.53106



# Verificar se todas as inicializações foram concluídas
select exp.title as title, exp.idexp, count(*) as inits
from experiment exp right join initialize init on exp.idexp = init.idexp
group by exp.title, exp.idexp
order by exp.idexp;
 
 delete from experiment where idexp = 16;