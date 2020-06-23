drop tablespace Schulungsfirma including contents;
create tablespace Schulungsfirma
  datafile 'tbs_Schulungsfirma'
    size 20M reuse;
--Created from <ent>
create table kurs
(
    knr varchar(400) primary key
,   bezeichn varchar(400)
,   tage varchar(400)
,   preis varchar(400)
)
tablespace Schulungsfirma;

--Created from <ent>
create table kveranst
(
    knr varchar(400) references kurs (knr)
,   knrlfnd varchar(400)
,   von varchar(400)
,   bis varchar(400)
,   ort varchar(400)
,   plaetze varchar(400)
,   primary key(knr,knrlfnd)
)
tablespace Schulungsfirma;

--Created from <ent>
create table person
(
    pnr varchar(400) primary key
,   fname varchar(400)
,   vname varchar(400)
,   ort varchar(400)
,   land varchar(400)
)
tablespace Schulungsfirma;

--Created from <ent>
create table referent
(
    gebdat varchar(400)
,   seit varchar(400)
,   titel varchar(400)
,   pnr varchar(400) primary key references person (pnr)
)
tablespace Schulungsfirma;

--Created from a m:n relation
create table setzt_voraus
(
    kurs_knr varchar(400) references kurs (knr)
,   kurs_knr2 varchar(400) references kurs (knr)
,   primary key(kurs_knr,kurs_knr2)
)
tablespace Schulungsfirma;

--Created from a m:n relation
create table besucht
(
    kveranst_knr varchar(400)
,   kveranst_knrlfnd varchar(400)
,   person_pnr varchar(400) references person (pnr)
,   kurs_knr varchar(400) references kurs (knr)
,   bezahlt varchar(400)
,   primary key(kveranst_knr,kveranst_knrlfnd,person_pnr,kurs_knr)
,   constraint fk_kveranst1
      foreign key(kveranst_knr,kveranst_knrlfnd)
      references kveranst(knr,knrlfnd)
)
tablespace Schulungsfirma;

--Created from a m:n relation
create table geeignet
(
    kurs_knr varchar(400) references kurs (knr)
,   referent_pnr varchar(400) references referent (pnr)
,   primary key(kurs_knr,referent_pnr)
)
tablespace Schulungsfirma;

drop table geeignet;
drop table besucht;
drop table setzt_voraus;
drop table referent;
drop table person;
drop table kveranst;
drop table kurs;
