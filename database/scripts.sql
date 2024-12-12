create table if not exists experiment (
    idexp NUMERIC PRIMARY KEY,
    title varchar(40),
    numpt numeric not NULL,
    status numeric not null check (status in (1, 2, 3))
);

create table initialize (
    idin numeric unique,
    status numeric not null check (status in (1, 2, 3)),
    idexp integer not null,
    constraint pk_init PRIMARY KEY (idin, idexp),
    constraint pk_init_exp FOREIGN KEY (idexp) REFERENCES experiment(idexp) on delete cascade
);

create table round (
    idround numeric,
    idin integer not null,
    avscore NUMERIC(5, 2) not null,
    avrew NUMERIC not null,
    tsteps numeric not null,
    nwins numeric not null,
    constraint pk_round PRIMARY KEY (idround, idin),
    constraint fk_round_init FOREIGN KEY (idin) REFERENCES initialize(idin) on delete cascade
);

drop table round;
drop table initialize;
drop table experiment;

insert into experiments values (1, 100, '2024-12-12', )