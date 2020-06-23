drop table if exists wurden_geschossen;
drop table if exists hat_geschossen;
drop table if exists spielt_mit_bei;
drop table if exists tore;
drop table if exists schiedsrichter;
drop table if exists turnier;
drop table if exists "spiel";
drop table if exists spieler;
drop table if exists person;
drop table if exists mannschaft;
go

--Created from <ent>
create table mannschaft(
    name          varchar(132)  not null primary key
,   gruendungsjahr varchar(132)  not null
,   adresse       varchar(132)  not null
);
go

--Created from <ent>
create table person(
    svnr         varchar(132)  not null primary key
,   name         varchar(132)  not null
,   wohnadresse  varchar(132)  not null
,   geburtsdatum varchar(132)  not null
);
go

--Created from <ent>
create table spieler(
    spielposition varchar(132)  not null
,   svnr          varchar(132)  not null primary key references person(svnr)
);
go

--Created from <ent>
create table "spiel"(
    spielort        varchar(132)  not null
,   "datum"         varchar(132)  not null
,   mannschaft_heim varchar(132)  not null
,   mannschaft_ausw varchar(132)  not null
,   schiedsrichter  varchar(132)  not null
,   ergebnis        varchar(132)  not null
,   primary key(spielort, "datum")
);
go

--Created from <ent>
create table turnier(
    nummer       varchar(132)  not null
,   name         varchar(132)  not null
,   begindatum   varchar(132)  not null
,   enddatum     varchar(132)  not null
,   mannschaften varchar(132)  not null
,   primary key(nummer, name)
);
go

--Created from <ent>
create table schiedsrichter(
    datum_pruefung      varchar(132)  not null
,   berechtigungsklasse varchar(132)  not null
,   svnr                varchar(132)  not null primary key references person(svnr)
);
go

--Created from <ent>
create table tore(
    anzahl_tore varchar(132)  not null
);
go

--Created from a m:n relation
create table spielt_mit_bei(
    mannschaft_name varchar(132)  not null references mannschaft(name)
,   spiel_spielort  varchar(132)  not null
,   "spiel_datum"   varchar(132)  not null
,   primary key(mannschaft_name, spiel_spielort, "spiel_datum")
,   constraint fk_spiel1
      foreign key(spiel_spielort, "spiel_datum")
      references "spiel"(spielort, "datum")
);
go

--Created from a m:n relation
create table hat_geschossen(
    spieler_svnr varchar(132)  not null primary key references spieler(svnr)
);
go

--Created from a m:n relation
create table wurden_geschossen(
    spiel_spielort varchar(132)  not null
,   "spiel_datum"  varchar(132)  not null
,   primary key(spiel_spielort, "spiel_datum")
,   constraint fk_spiel2
      foreign key(spiel_spielort, "spiel_datum")
      references "spiel"(spielort, "datum")
);
go

