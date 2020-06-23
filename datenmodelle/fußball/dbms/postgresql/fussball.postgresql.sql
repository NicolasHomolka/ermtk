--Created from <ent>
create table mannschaft
(
    name varchar(300) primary key
,   gruendungsjahr varchar(300)
,   adresse varchar(300)
);

--Created from <ent>
create table person
(
    svnr varchar(300) primary key
,   name varchar(300)
,   wohnadresse varchar(300)
,   geburtsdatum varchar(300)
);

--Created from <ent>
create table spieler
(
    spielposition varchar(300)
,   svnr varchar(300) primary key references person (svnr)
);

--Created from <ent>
create table spiel
(
    spielort varchar(300)
,   datum varchar(300)
,   mannschaft_heim varchar(300)
,   mannschaft_ausw varchar(300)
,   schiedsrichter varchar(300)
,   ergebnis varchar(300)
,   primary key(spielort,datum)
);

--Created from <ent>
create table turnier
(
    nummer varchar(300)
,   name varchar(300)
,   begindatum varchar(300)
,   enddatum varchar(300)
,   mannschaften varchar(300)
,   primary key(nummer,name)
);

--Created from <ent>
create table schiedsrichter
(
    datum_pruefung varchar(300)
,   berechtigungsklasse varchar(300)
,   svnr varchar(300) primary key references person (svnr)
);

--Created from <ent>
create table tore
(
    anzahl_tore varchar(300)
);

--Created from a m:n relation
create table spielt_mit_bei
(
    mannschaft_name varchar(300) references mannschaft (name)
,   spiel_spielort varchar(300)
,   spiel_datum varchar(300)
,   primary key(mannschaft_name,spiel_spielort,spiel_datum)
,   foreign key(spiel_spielort, spiel_datum) references spiel(spielort,datum)
);

--Created from a m:n relation
create table hat_geschossen
(
    spieler_svnr varchar(300) primary key references spieler (svnr)
);

--Created from a m:n relation
create table wurden_geschossen
(
    spiel_spielort varchar(300)
,   spiel_datum varchar(300)
,   primary key(spiel_spielort,spiel_datum)
,   foreign key(spiel_spielort, spiel_datum) references spiel(spielort,datum)
);

drop table if exists wurden_geschossen;
drop table if exists hat_geschossen;
drop table if exists spielt_mit_bei;
drop table if exists tore;
drop table if exists schiedsrichter;
drop table if exists turnier;
drop table if exists spiel;
drop table if exists spieler;
drop table if exists person;
drop table if exists mannschaft;
