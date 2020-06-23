--Created from <ent>
create table wein
(
    name varchar(300) primary key
,   farbe varchar(300)
,   jahrgang varchar(300)
,   restsuesse varchar(300)
,   erzeuger varchar(300)
);

--Created from <ent>
create table erzeuger
(
    name varchar(300) primary key
,   adresse varchar(300)
,   lizenznummer varchar(300)
,   mengewein varchar(300)
,   anbaugebiet varchar(300)
);

--Created from <ent>
create table anbaugebiet
(
    name varchar(300)
,   region varchar(300)
,   land varchar(300)
);

--Created from <ent>
create table rebsorte
(
    name varchar(300)
,   farbe varchar(300)
,   anteil varchar(300)
);

--Created from <ent>
create table lizenz
(
    lizenznummer varchar(300)
,   menge varchar(300)
);

--Created from a m:n relation
create table erzeugt
(
    erzeuger_name varchar(300) references erzeuger (name)
,   wein_name varchar(300) references wein (name)
,   primary key(erzeuger_name,wein_name)
);

--Created from a m:n relation
create table beinhaltet
(
    wein_name varchar(300) primary key references wein (name)
,   anteil varchar(300)
);

drop table if exists beinhaltet;
drop table if exists erzeugt;
drop table if exists lizenz;
drop table if exists rebsorte;
drop table if exists anbaugebiet;
drop table if exists erzeuger;
drop table if exists wein;
