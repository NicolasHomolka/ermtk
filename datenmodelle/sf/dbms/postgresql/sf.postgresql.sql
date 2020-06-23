--Created from <ent>
create table kurs
(
    knr varchar(300) primary key
,   bezeichn varchar(300)
,   tage varchar(300)
,   preis varchar(300)
);

--Created from <ent>
create table kveranst
(
    knr varchar(300) references kurs (knr)
,   knrlfnd varchar(300)
,   von varchar(300)
,   bis varchar(300)
,   ort varchar(300)
,   plaetze varchar(300)
,   primary key(knr,knrlfnd)
);

--Created from <ent>
create table person
(
    pnr varchar(300) primary key
,   fname varchar(300)
,   vname varchar(300)
,   ort varchar(300)
,   land varchar(300)
);

--Created from <ent>
create table referent
(
    gebdat varchar(300)
,   seit varchar(300)
,   titel varchar(300)
,   pnr varchar(300) primary key references person (pnr)
);

--Created from a m:n relation
create table setzt_voraus
(
    kurs_knr varchar(300) references kurs (knr)
,   kurs_knr2 varchar(300) references kurs (knr)
,   primary key(kurs_knr,kurs_knr2)
);

--Created from a m:n relation
create table besucht
(
    kveranst_knr varchar(300)
,   kveranst_knrlfnd varchar(300)
,   person_pnr varchar(300) references person (pnr)
,   kurs_knr varchar(300) references kurs (knr)
,   bezahlt varchar(300)
,   primary key(kveranst_knr,kveranst_knrlfnd,person_pnr,kurs_knr)
,   foreign key(kveranst_knr, kveranst_knrlfnd) references kveranst(knr,knrlfnd)
);

--Created from a m:n relation
create table geeignet
(
    kurs_knr varchar(300) references kurs (knr)
,   referent_pnr varchar(300) references referent (pnr)
,   primary key(kurs_knr,referent_pnr)
);

drop table if exists geeignet;
drop table if exists besucht;
drop table if exists setzt_voraus;
drop table if exists referent;
drop table if exists person;
drop table if exists kveranst;
drop table if exists kurs;
