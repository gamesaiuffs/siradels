CREATE TABLE variable (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE variable_representation (
    id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL,
    id_variable INT NOT NULL,
    FOREIGN KEY (id_variable) REFERENCES variable(id) ON DELETE CASCADE
);

create table if not exists experiment (
    id NUMERIC PRIMARY KEY,
    title varchar(40),
    numpt numeric not NULL
);

create table if not exists experiment_permutation (
    id SERIAL PRIMARY KEY,
    id_exp numeric not null,
    status varchar(10) not null check (status in ('nao_iniciado', 'rodando', 'concluido')),
    constraint fk_exp FOREIGN KEY (id_exp) REFERENCES experiment(id)
)

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

drop table experiment_statistics;
drop table sample;
drop table initialize;
drop table permutation_representation;
drop table experiment_permutation;
drop table experiment;
drop table variable_representation;
drop table variable;



-- Pré requisito - variáveis cadastradas 

































































