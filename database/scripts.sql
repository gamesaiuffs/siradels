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

insert into experiment(idexp, title, numpt, status) values (1, 'Entradas originais -  sem transformacao', 300000, 'pendente');

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


select idin, max(nwins)
from sample
where idexp=1
group by idin
order by idin;

select avg(max) from (select idin, max(nwins) from sample where idexp=2 group by idin order by idin);