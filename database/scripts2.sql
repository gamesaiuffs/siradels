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

-- CREATE TABLE variable_representation (
--     id SERIAL PRIMARY KEY,
--     title VARCHAR(100) not null,
--     description VARCHAR(100) NOT NULL,
--     id_variable NUMERIC NOT NULL,
--     FOREIGN KEY (id_variable) REFERENCES variable(id) ON DELETE CASCADE
-- );

create table if not exists experiment (
    id NUMERIC PRIMARY KEY,
    title varchar(40) not null,
    numpt numeric not NULL
);

create table if not exists experiment_permutation (
    id INT PRIMARY KEY,
    id_exp numeric not null,
    status varchar(10) not null check (status in ('pendente', 'rodando', 'concluido')),
    constraint fk_exp FOREIGN KEY (id_exp) REFERENCES experiment(id)
);

-- CREATE TABLE permutation_representation (
--     id_permutation INT NOT NULL,
--     id_representation INT NOT NULL,
--     PRIMARY KEY (id_permutation, id_representation),
--     FOREIGN KEY (id_permutation) REFERENCES experiment_permutation(id) ON DELETE CASCADE,
--     FOREIGN KEY (id_representation) REFERENCES variable_representation(id) ON DELETE CASCADE
-- );

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
-- insert into variable(id, description) values (1, 'ouro_personagem');
insert into variable(id, description) values 
    (1, 'ouro_personagem'),
    (2, 'cartas_dist_mao'),
    (3, 'carta_mais_cara'),
    (4, 'carta_mais_barata'),
    (5, 'qtd_dist_const'),
    (6, 'qtd_dist_cada_tipo'),
    (7, 'dist_const_jog_mais_const'),
    (8, 'jog_mais_cartas_mao'),
    (9, 'ouro_oponentes');

-- insert into 
-- variable_representation(title, description, id_variable) 
-- values ('ouro_personagem_padrao', 'Ouro do personagem em classes pouco, medio ou muito', 1),
-- values ('ouro_personagem_classes', 'Ouro do personagem em valor real - 0 a 5+', 1);

insert into variable_representation(title, description, id_variable) 
values 
    ('ouro_personagem_padrao', 'Ouro do personagem em valor limitado entre 0 e 6.', 1),
    ('ouro_personagem_classes', 'Ouro do personagem em classes pouco (0-2), medio (3-5) ou muito (6+).', 1),
    ('ouro_personagem_proporcao', 'Ouro do personagem em proporção ao total no jogo.', 1),
    ('cartas_dist_mao_padrao', 'Quantidade de cartas distribuídas na mão em valor limitado entre 0 e 5.', 2),
    ('cartas_dist_mao_classes', 'Quantidade de cartas distribuídas na mão em classes.', 2),
    ('carta_mais_cara_padrao', 'Valor da carta mais cara na mão em valor limitado entre 0 e 6.', 3),
    ('carta_mais_cara_classes', 'Valor da carta mais cara em classes barata, média ou cara.', 3),
    ('carta_mais_cara_proporcao', 'Proporção do valor da carta mais cara em relação ao total de valores.', 3),
    ('carta_mais_barata_padrao', 'Valor da carta mais barata na mão em valor limitado entre 0 e 6.', 4),
    ('carta_mais_barata_classe', 'Valor da carta mais barata em classes barata, média ou cara.', 4),
    ('carta_mais_barata_proporcao', 'Proporção do valor da carta mais barata em relação ao total de valores.', 4),
    ('qtd_dist_const_padrao', 'Quantidade de distritos construídos em valor limitado entre 0 e 3.', 5),
    ('qtd_dist_const_percent', 'Progresso percentual dos distritos construídos.', 5),
    ('qtd_dist_const_proporcao', 'Proporção de distritos construídos em relação ao total.', 5),
    ('qtd_dist_cada_tipo_padrao', 'Quantidade de distritos de cada tipo em vetor limitado entre 0 e 3.', 6),
    ('qtd_dist_cada_tipo_vetor_bin', 'Vetor binário representando a construção ou não de cada tipo de distrito.', 6),
    --('qtd_dist_cada_tipo_bin', 'Valor binário único indicando se construiu ao menos um distrito de cada tipo.', 6),
    ('dist_const_jog_mais_const_padrao', 'Quantidade de distritos construídos pelo jogador com mais distritos em valor limitado entre 0 e 7.', 7),
    ('dist_const_jog_mais_const_proporcao', 'Proporção de distritos construídos pelo jogador com mais distritos em relação ao total.', 7),
    ('jog_mais_cartas_mao_padrao', 'Quantidade de cartas na mão do jogador com mais cartas em valor limitado entre 0 e 5.', 8),
    ('jog_mais_cartas_mao_proporcao', 'Proporção de cartas na mão do jogador com mais cartas em relação ao total.', 8),
    ('ouro_oponentes_padrao', 'Quantidade de ouro dos oponentes em valor limitado entre 0 e 4.', 9),
    ('ouro_oponentes_vetor', 'Vetor de proporções do ouro de cada oponente sobre ao total.', 9);
    -- ('ouro_oponentes_media', 'Média do ouro dos oponentes.', 9);


-- Cadastro de experimento 
insert into experiment(id, numpt, title) values (1, 300000, '1 - entradas originais ');

-- na implementação 
-- Em cada rodada
--      Temos uma permutação (pré cadastrada) que será executada 
insert into experiment_permutation(id, id_exp, status) values (1, 1, 'pendente');

-- experimento de controle 
insert into permutation_representation (id_permutation, id_representation)
values 
(1, 1),
(1, 4),
(1, 6),
(1, 9),
(1, 12),
(1, 15),
(1, 17),
(1, 19),
(1, 21);

select vr.title from experiment_permutation ep
join permutation_representation pe on ep.id = pe.id_permutation
join variable_representation vr on pe.id_representation=vr.id
where ep.id = 4;

--      Para cada permutação: Faremos 10 inicializações
-- insert into initialize (id, status, id_permutation) values 
-- (1, 'pendente', 1),
-- (2, 'pendente', 1),
-- (3, 'pendente', 1),
-- (4, 'pendente', 1),
-- (5, 'pendente', 1),
-- (6, 'pendente', 1),
-- (7, 'pendente', 1),
-- (8, 'pendente', 1),
-- (9, 'pendente', 1),
-- (10, 'pendente', 1);

-- insert into sample(id, id_initialize, id_permutation, avscore, avrew, tsteps, nwins)
-- values (1, 1, 1, 12.8, -234, 300000, 22);


-- conferir contagem das variaveis registradas para cada permutação
select id_permutation, count(*)
from permutation_representation pr 
GROUP BY id_permutation
ORDER BY id_permutation;

























































