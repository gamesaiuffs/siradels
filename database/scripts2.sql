drop table experiment_statistics;
drop table sample;
drop table initialize;
drop table permutation_representation;
drop table experiment_permutation;
drop table experiment;
drop table variable_representation;
drop table variable;


CREATE TABLE variable (
    id NUMERIC PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE variable_representation (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) not null,
    description VARCHAR(100) NOT NULL,
    id_variable NUMERIC NOT NULL,
    FOREIGN KEY (id_variable) REFERENCES variable(id) ON DELETE CASCADE
);

create table if not exists experiment (
    id NUMERIC PRIMARY KEY,
    title varchar(40) not null,
    numpt numeric not NULL
);

create table if not exists experiment_permutation (
    id SERIAL PRIMARY KEY,
    id_exp numeric not null,
    status varchar(10) not null check (status in ('pendente', 'rodando', 'concluido')),
    constraint fk_exp FOREIGN KEY (id_exp) REFERENCES experiment(id)
);

CREATE TABLE permutation_representation (
    id_permutation INT NOT NULL,
    id_representation INT NOT NULL,
    PRIMARY KEY (id_permutation, id_representation),
    FOREIGN KEY (id_permutation) REFERENCES experiment_permutation(id) ON DELETE CASCADE,
    FOREIGN KEY (id_representation) REFERENCES variable_representation(id) ON DELETE CASCADE
);

create table initialize (
    id numeric not null,
    status varchar(10) not null check (status in ('pendente', 'concluido')),
    id_permutation INT NOT NULL,
    constraint pk_init PRIMARY KEY (id, id_permutation),
    constraint pk_init_exp FOREIGN KEY (id_permutation) REFERENCES experiment_permutation(id) on delete cascade
);

create table sample (
    id numeric not null,
    id_initialize numeric not null,
    id_permutation int not null, 
    avscore NUMERIC(5, 2) not null,
    avrew NUMERIC not null,
    tsteps numeric not null,
    nwins numeric not null,
    constraint pk_sample PRIMARY KEY (id, id_initialize, id_permutation),
    constraint fk_sample_init FOREIGN KEY (id_initialize, id_permutation) REFERENCES initialize(id, id_permutation) on delete cascade
);

CREATE TABLE experiment_statistics (
    id SERIAL PRIMARY KEY, -- Identificador único do experimento
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
    FOREIGN KEY (id_permutation) REFERENCES experiment_permutation(id) ON DELETE CASCADE -- Relacionamento com a permutação associada
);




-- Pré requisito - variáveis cadastradas - scripts separados 
insert into variable(id, description) values (1, 'Ouros do personagem');

insert into 
variable_representation(title, description, id_variable) 
values ('ouro_personagens_classes', 'Ouro do personagem em classes pouco, medio ou muito', 1);

insert into 
variable_representation(title, description, id_variable) 
values ('ouro_personagens_padrao', 'Ouro do personagem em valor real - 0 a 5+', 1);

-- Cadastro de experimento 
insert into experiment(id, numpt, title) values (1, 300000, 'Grid Search Completo');

-- na implementação 
-- Em cada rodada
--      Temos uma permutação (pré cadastrada) que será executada 
insert into experiment_permutation(id_exp, status) values (1, 'pendente');

--      Para cada permutação: Faremos 10 inicializações
insert into initialize (id, status, id_permutation) values 
(1, 'pendente', 1),
(2, 'pendente', 1),
(3, 'pendente', 1),
(4, 'pendente', 1),
(5, 'pendente', 1),
(6, 'pendente', 1),
(7, 'pendente', 1),
(8, 'pendente', 1),
(9, 'pendente', 1),
(10, 'pendente', 1);

insert into sample(id, id_initialize, id_permutation, avscore, avrew, tsteps, nwins)
values (1, 1, 1, 12.8, -234, 300000, 22);




























































