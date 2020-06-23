drop table if exists geeignet;
drop table if exists besucht;
drop table if exists setzt_voraus;
drop table if exists referent;
drop table if exists person;
drop table if exists kveranst;
drop table if exists kurs;
go

--Created from <ent>
create table kurs(
    knr      varchar(132)  not null primary key
,   bezeichn varchar(132)  not null
,   tage     varchar(132)  not null
,   preis    varchar(132)  not null
);
go

--Created from <ent>
create table kveranst(
    knr     varchar(132)  not null references kurs(knr)
,   knrlfnd varchar(132)  not null
,   von     varchar(132)  not null
,   bis     varchar(132)  not null
,   ort     varchar(132)  not null
,   plaetze varchar(132)  not null
,   primary key(knr, knrlfnd)
);
go

--Created from <ent>
create table person(
    pnr   varchar(132)  not null primary key
,   fname varchar(132)  not null
,   vname varchar(132)  not null
,   ort   varchar(132)  not null
,   land  varchar(132)  not null
);
go

--Created from <ent>
create table referent(
    gebdat varchar(132)  not null
,   seit   varchar(132)  not null
,   titel  varchar(132)  not null
,   pnr    varchar(132)  not null primary key references person(pnr)
);
go

--Created from a m:n relation
create table setzt_voraus(
    kurs_knr  varchar(132)  not null references kurs(knr)
,   kurs_knr2 varchar(132)  not null references kurs(knr)
,   primary key(kurs_knr, kurs_knr2)
);
go

--Created from a m:n relation
create table besucht(
    kveranst_knr     varchar(132)  not null
,   kveranst_knrlfnd varchar(132)  not null
,   person_pnr       varchar(132)  not null references person(pnr)
,   bezahlt          varchar(132)  not null
,   primary key(kveranst_knr, kveranst_knrlfnd, person_pnr)
,   constraint fk_kveranst1
      foreign key(kveranst_knr, kveranst_knrlfnd)
      references kveranst(knr, knrlfnd)
);
go

--Created from a m:n relation
create table geeignet(
    kurs_knr     varchar(132)  not null references kurs(knr)
,   referent_pnr varchar(132)  not null references referent(pnr)
,   primary key(kurs_knr, referent_pnr)
);
go

