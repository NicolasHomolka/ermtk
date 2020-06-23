drop tablespace Weingut including contents;
create tablespace Weingut
  datafile 'tbs_Weingut'
    size 20M reuse;
--Created from <ent>
create table wein
(
    name varchar(400) primary key
,   farbe varchar(400)
,   jahrgang varchar(400)
,   restsuesse varchar(400)
,   erzeuger varchar(400)
)
tablespace Weingut;

--Created from <ent>
create table erzeuger
(
    name varchar(400) primary key
,   adresse varchar(400)
,   lizenznummer varchar(400)
,   mengewein varchar(400)
,   anbaugebiet varchar(400)
)
tablespace Weingut;

--Created from <ent>
create table anbaugebiet
(
    name varchar(400)
,   region varchar(400)
,   land varchar(400)
)
tablespace Weingut;

--Created from <ent>
create table rebsorte
(
    name varchar(400)
,   farbe varchar(400)
,   anteil varchar(400)
)
tablespace Weingut;

--Created from <ent>
create table lizenz
(
    lizenznummer varchar(400)
,   menge varchar(400)
)
tablespace Weingut;

--Created from a m:n relation
create table erzeugt
(
    erzeuger_name varchar(400) references erzeuger (name)
,   wein_name varchar(400) references wein (name)
,   primary key(erzeuger_name,wein_name)
)
tablespace Weingut;

--Created from a m:n relation
create table beinhaltet
(
    wein_name varchar(400) primary key references wein (name)
,   anteil varchar(400)
)
tablespace Weingut;

drop table beinhaltet;
drop table erzeugt;
drop table lizenz;
drop table rebsorte;
drop table anbaugebiet;
drop table erzeuger;
drop table wein;
