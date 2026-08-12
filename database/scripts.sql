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





-- EXPERIMENTO 1 COM PPO
-- experimento      % vitoria       representação           ambiente
-- 31                               original                box
-- 32                               orig limitado           multidiscreto
-- 33                               proporcoes              box
-- 34                               classes                 multidiscreto
-- 35                               binaria                 multibin


--  idexp |                  title                   | numpt  |  status   
-- -------+------------------------------------------+--------+-----------
--      2 | Entradas padrao - originais do ambiente  | 300000 | concluido
--      1 | Entradas originais -  sem transformacao  | 300000 | concluido
--      4 | Entradas em 3 classes                    | 300000 | concluido
--      5 | Entradas em 2 classes - bin              | 300000 | concluido
--      3 | Entradas em proporcoes                   | 300000 | concluido
--      6 | entradas padrao - substitui o exp2       | 300000 | concluido
--     11 | menos:menos_cartas_dist_mao              | 300000 | pendente
--     10 | menos:ouro_personagem_original           | 300000 | concluido
--     12 | menos:menos_carta_mais_cara_original     | 300000 | pendente
--     13 | menos:menos_carta_mais_barata_original   | 300000 | pendente
--     14 | menos:menos_qtd_dist_const_original      | 300000 | pendente
--     15 | menos:menos_qtd_dist_cada_tipo_original  | 300000 | pendente
--     16 | menos:men_dist_ct_jog_m_c_orig           | 300000 | pendente
--     31 | Entr originais - PPO - sem transformacao | 300000 | pendente
--     32 | PPO - original limitado                  | 300000 | pendente
--     33 | PPO - proporcoes                         | 300000 | pendente
--     34 | PPO - classes de 3                       | 300000 | pendente
--     35 | PPO - binario                            | 300000 | pendente


-- ia=# select * from sample where idexp = 31 and tsteps = 300000;
--  id_sample | idin | idexp | avscore |  avrew   | tsteps | nwins 
-- -----------+------+-------+---------+----------+--------+-------
--         30 |    1 |    31 |   20.32 |    183.0 | 300000 |    46
--         30 |    2 |    31 |   12.45 | -17702.0 | 300000 |    11
--         30 |    3 |    31 |   20.90 |    175.0 | 300000 |    52
--         30 |    4 |    31 |   13.81 |   -312.0 | 300000 |    10
--         30 |    5 |    31 |   11.18 |     84.0 | 300000 |     7
--         30 |    6 |    31 |   11.22 | -14003.0 | 300000 |     6
--         30 |    7 |    31 |   11.63 |    -10.0 | 300000 |     9
--         30 |    8 |    31 |   18.63 |    165.0 | 300000 |    38
--         30 |    9 |    31 |   12.04 |    127.0 | 300000 |    10
--         30 |   10 |    31 |   17.38 |    187.0 | 300000 |    32
-- (10 rows)

-- Em relação às sementes que vão muuuuito mal, uma teoria possível é a de que: 
-- Punir o modelo por uma ação errada e continuar no mesmo estado é uma escolha legal, especialmente se a intenção é ensinar “essa ação não serve neste estado”. Não é absurda nem “errada”.
-- O que ela traz de efeito colateral no PPO é que, como o estado não muda, a política pode repetir a mesma ação inválida muitas vezes antes de conseguir sair daquele estado. Em algoritmo on-policy, isso pode gerar rollouts cheios de -100, vantagens muito negativas, e uma atualização meio agressiva/desestabilizadora. Isso combina bem com os avrew gigantes negativos do exp. 31.
-- Então eu não chamaria de bug. Eu chamaria de decisão de modelagem com alto impacto no PPO.
-- Para sua pesquisa, eu separaria assim:
-- Se a pergunta é “como a representação afeta o treinamento no ambiente atual?”, mantenha como está, mas meça ações inválidas por episódio/checkpoint.
-- Se a pergunta é “como escala/abstração afeta aprendizado estratégico, isolando ruído de ações inválidas?”, use action masking ou encerre/trunque depois de erro.
-- Se quiser manter a punição, talvez reduza -100 ou normalize recompensas, porque o delta de pontuação fica pequeno perto dessa punição.
-- Minha suspeita: os dados crus não “fazem PPO jogar mal” diretamente; eles fazem PPO aprender pior a máscara implícita de personagens disponíveis. Aí ele toma muitas punições repetidas e algumas sementes entram em colapso.


-- As principais hipóteses, olhando para o seu código, são estas:
-- O PPO aprende disponibilidade de personagem melhor quando ela está “destacada” pela representação
-- Nos vetores com classes/binário/limitado, quase tudo está em escala pequena: 0..1, 0..2, 0..7. A disponibilidade dos personagens também é 0/1.
-- Nos dados crus, algumas features podem crescer muito mais: ouro, cartas na mão, ouro dos oponentes etc. Mesmo que a disponibilidade esteja no vetor como 0/1, ela compete com features de magnitude maior. Para uma MLP sem normalização, isso pode fazer o PPO dar menos peso aos bits de disponibilidade, justamente os bits necessários para evitar ação inválida.
-- Essa é minha hipótese mais forte.
-- Box cru não recebe o mesmo tratamento que MultiDiscrete/MultiBinary
-- Pelo modelo salvo, o exp. 31 usou Box com shape 25. Já os experimentos limitados/classes/binários usam outros espaços. Isso muda como o SB3 interpreta/preprocessa a observação.
-- Então não é só “valores diferentes”; também é “tipo de observation space diferente”. Os ambientes discretos podem estar entregando uma codificação mais amigável para a política.
-- O custo de errar é muito maior que o sinal positivo normal
-- A ação inválida dá -100. O ganho por pontuação costuma ser bem menor e, no seu ambiente box/md/mb, aparece como delta de pontuação * 10.
-- Se nos dados crus o agente demora mais para aprender ações válidas, ele acumula muitos -100 antes de aprender qualquer coisa útil. A partir daí, algumas sementes podem entrar numa região ruim da política e não recuperar. Nos outros ambientes, talvez ele aprenda cedo o padrão de disponibilidade e nunca caia nesse buraco.
-- PPO é mais sensível a escala que DQN
-- DQN também sofre com escala, mas PPO depende diretamente de estimativas de vantagem, valor e atualização clipped. Observações mal escaladas podem gerar política/valor mais instáveis. Isso explicaria por que o efeito aparece forte agora em PPO, mesmo que DQN não tenha mostrado a mesma tragédia.
-- As representações abstratas reduzem ruído e estados raros
-- Classes e binário “juntam” muitos estados diferentes em poucos valores. Isso pode facilitar a generalização: o agente vê várias situações como parecidas e aprende mais rápido “quando rank X está disponível”.
-- Nos dados crus, pequenas diferenças numéricas criam estados mais variados. Com só 300000 steps, algumas inicializações podem não ver dados suficientes para estabilizar essa associação.
-- O exp. de proporções não é só escala menor, é também informação relativa
-- Proporção pode estar ajudando mais do que “normalizar”: ela transforma variáveis em relações comparativas. PPO pode aprender melhor com “meu ouro relativo à mesa” do que com “tenho 7 ouros”. Então proporção talvez não seja apenas menos instável; talvez seja uma representação semanticamente melhor.
-- A avaliação com Agente mascara ações inválidas
-- Durante a avaliação de vitórias, [Agente.py (line 18)](/home/eduardo/projetos/siradels/classes/strategies/Agente.py:18) fica chamando predict até sair uma ação válida. Então uma política que erra muito pode ainda jogar a partida depois de várias tentativas. Já evaluate_policy no ambiente recebe -100 diretamente.
-- Isso pode explicar a diferença entre nwins e avrew, e também sugere uma métrica chave: contar quantas tentativas inválidas acontecem antes de cada escolha válida.



-- ia=# select * from sample where idexp = 31 and tsteps = 300000;
--  id_sample | idin | idexp | avscore |  avrew   | tsteps | nwins 
-- -----------+------+-------+---------+----------+--------+-------
--         30 |    1 |    31 |   20.32 |    183.0 | 300000 |    46
--         30 |    2 |    31 |   12.45 | -17702.0 | 300000 |    11
--         30 |    3 |    31 |   20.90 |    175.0 | 300000 |    52
--         30 |    4 |    31 |   13.81 |   -312.0 | 300000 |    10
--         30 |    5 |    31 |   11.18 |     84.0 | 300000 |     7
--         30 |    6 |    31 |   11.22 | -14003.0 | 300000 |     6
--         30 |    7 |    31 |   11.63 |    -10.0 | 300000 |     9
--         30 |    8 |    31 |   18.63 |    165.0 | 300000 |    38
--         30 |    9 |    31 |   12.04 |    127.0 | 300000 |    10
--         30 |   10 |    31 |   17.38 |    187.0 | 300000 |    32
-- (10 rows)

-- ia=# select * from sample where idexp = 32 and tsteps = 300000;
--  id_sample | idin | idexp | avscore | avrew | tsteps | nwins 
-- -----------+------+-------+---------+-------+--------+-------
--         30 |    1 |    32 |   21.50 | 163.0 | 300000 |    53
--         30 |    2 |    32 |   20.39 | 219.0 | 300000 |    52
--         30 |    3 |    32 |   21.33 | 180.0 | 300000 |    53
--         30 |    4 |    32 |   21.35 | 210.0 | 300000 |    52
--         30 |    5 |    32 |   20.52 | 245.0 | 300000 |    52
--         30 |    6 |    32 |   21.74 | 221.0 | 300000 |    57
--         30 |    7 |    32 |   21.65 | 226.0 | 300000 |    52
--         30 |    8 |    32 |   22.36 | 283.0 | 300000 |    60
--         30 |    9 |    32 |   23.06 | 194.0 | 300000 |    63
--         30 |   10 |    32 |   21.39 | 248.0 | 300000 |    56
-- (10 rows)

-- ia=# select * from sample where idexp = 33 and tsteps = 300000;
--  id_sample | idin | idexp | avscore | avrew | tsteps | nwins 
-- -----------+------+-------+---------+-------+--------+-------
--         30 |    1 |    33 |   20.07 | 252.0 | 300000 |    43
--         30 |    2 |    33 |   21.39 | 134.0 | 300000 |    57
--         30 |    3 |    33 |   20.36 | 226.0 | 300000 |    45
--         30 |    4 |    33 |   21.95 | 217.0 | 300000 |    59
--         30 |    5 |    33 |   19.24 | 227.0 | 300000 |    40
--         30 |    6 |    33 |   20.77 | 236.0 | 300000 |    52
--         30 |    7 |    33 |   20.47 | 198.0 | 300000 |    47
--         30 |    8 |    33 |   20.34 | 203.0 | 300000 |    49
--         30 |    9 |    33 |   21.44 | 191.0 | 300000 |    54
--         30 |   10 |    33 |   21.81 | 178.0 | 300000 |    54
-- (10 rows)

-- ia=# select * from sample where idexp = 34 and tsteps = 300000;
--  id_sample | idin | idexp | avscore | avrew | tsteps | nwins 
-- -----------+------+-------+---------+-------+--------+-------
--         30 |    1 |    34 |   20.10 | 232.0 | 300000 |    45
--         30 |    2 |    34 |   20.13 | 194.0 | 300000 |    52
--         30 |    3 |    34 |   21.33 | 143.0 | 300000 |    55
--         30 |    4 |    34 |   21.01 | 214.0 | 300000 |    52
--         30 |    5 |    34 |   20.76 | 242.0 | 300000 |    49
--         30 |    6 |    34 |   22.03 | 222.0 | 300000 |    56
--         30 |    7 |    34 |   20.58 | 203.0 | 300000 |    53
--         30 |    8 |    34 |   22.11 | 203.0 | 300000 |    60
--         30 |    9 |    34 |   19.86 | 199.0 | 300000 |    44
--         30 |   10 |    34 |   21.76 | 207.0 | 300000 |    55
-- (10 rows)

-- ia=# select * from sample where idexp = 35 and tsteps = 300000;
--  id_sample | idin | idexp | avscore | avrew | tsteps | nwins 
-- -----------+------+-------+---------+-------+--------+-------
--         30 |    1 |    35 |   20.22 | 209.0 | 300000 |    41
--         30 |    2 |    35 |   21.06 | 190.0 | 300000 |    60
--         30 |    3 |    35 |   20.97 | 172.0 | 300000 |    49
--         30 |    4 |    35 |   20.40 | 163.0 | 300000 |    50
--         30 |    5 |    35 |   21.28 | 238.0 | 300000 |    55
--         30 |    6 |    35 |   22.01 | 182.0 | 300000 |    57
--         30 |    7 |    35 |   18.67 | 214.0 | 300000 |    29
--         30 |    8 |    35 |   20.81 | 147.0 | 300000 |    50
--         30 |    9 |    35 |   19.73 | 211.0 | 300000 |    47
--         30 |   10 |    35 |   20.06 | 204.0 | 300000 |    47
-- (10 rows)







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