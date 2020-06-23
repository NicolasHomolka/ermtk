drop table if exists "beinhaltet";
drop table if exists erzeugt;
drop table if exists lizenz;
drop table if exists rebsorte;
drop table if exists anbaugebiet;
drop table if exists erzeuger;
drop table if exists wein;
go

--Created from <ent>
create table wein(
    name     varchar(132)  not null primary key
,   farbe    varchar(132)  not null
,   jahrgang varchar(132)  not null
,   restsuesse varchar(132)  not null
,   erzeuger varchar(132)  not null
);
go

--Created from <ent>
create table erzeuger(
    name         varchar(132)  not null primary key
,   adresse      varchar(132)  not null
,   lizenznummer varchar(132)  not null
,   mengewein    varchar(132)  not null
,   anbaugebiet  varchar(132)  not null
);
go

--Created from <ent>
create table anbaugebiet(
    name   varchar(132)  not null
,   region varchar(132)  not null
,   land   varchar(132)  not null
);
go

--Created from <ent>
create table rebsorte(
    name   varchar(132)  not null
,   farbe  varchar(132)  not null
,   anteil varchar(132)  not null
);
go

--Created from <ent>
create table lizenz(
    lizenznummer varchar(132)  not null
,   menge        varchar(132)  not null
);
go

--Created from a m:n relation
create table erzeugt(
    erzeuger_name varchar(132)  not null references erzeuger(name)
,   wein_name     varchar(132)  not null references wein(name)
,   primary key(erzeuger_name, wein_name)
);
go

--Created from a m:n relation
create table "beinhaltet"(
    wein_name varchar(132)  not null primary key references wein(name)
,   anteil    varchar(132)  not null
);
go

