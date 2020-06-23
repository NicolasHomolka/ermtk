drop tablespace Fussball including contents;
create tablespace Fussball
  datafile 'tbs_Fussball'
    size 20M reuse;
--Created from <ent>
create table mannschaft
(
    name varchar(400) primary key
,   gruendungsjahr varchar(400)
,   adresse varchar(400)
)
tablespace Fussball;

--Created from <ent>
create table person
(
    svnr varchar(400) primary key
,   name varchar(400)
,   wohnadresse varchar(400)
,   geburtsdatum varchar(400)
)
tablespace Fussball;

--Created from <ent>
create table spieler
(
    spielposition varchar(400)
,   svnr varchar(400) primary key references person (svnr)
)
tablespace Fussball;

--Created from <ent>
create table spiel
(
    spielort varchar(400)
,   datum varchar(400)
,   mannschaft_heim varchar(400)
,   mannschaft_ausw varchar(400)
,   schiedsrichter varchar(400)
,   ergebnis varchar(400)
,   primary key(spielort,datum)
)
tablespace Fussball;

--Created from <ent>
create table turnier
(
    nummer varchar(400)
,   name varchar(400)
,   begindatum varchar(400)
,   enddatum varchar(400)
,   mannschaften varchar(400)
,   primary key(nummer,name)
)
tablespace Fussball;

--Created from <ent>
create table schiedsrichter
(
    datum_pruefung varchar(400)
,   berechtigungsklasse varchar(400)
,   svnr varchar(400) primary key references person (svnr)
)
tablespace Fussball;

--Created from <ent>
create table tore
(
    anzahl_tore varchar(400)
)
tablespace Fussball;

--Created from a m:n relation
create table spielt_mit_bei
(
    mannschaft_name varchar(400) references mannschaft (name)
,   spiel_spielort varchar(400)
,   spiel_datum varchar(400)
,   primary key(mannschaft_name,spiel_spielort,spiel_datum)
,   constraint fk_spiel1
      foreign key(spiel_spielort,spiel_datum)
      references spiel(spielort,datum)
)
tablespace Fussball;

--Created from a m:n relation
create table hat_geschossen
(
    spieler_svnr varchar(400) primary key references spieler (svnr)
)
tablespace Fussball;

--Created from a m:n relation
create table wurden_geschossen
(
    spiel_spielort varchar(400)
,   spiel_datum varchar(400)
,   primary key(spiel_spielort,spiel_datum)
,   constraint fk_spiel2
      foreign key(spiel_spielort,spiel_datum)
      references spiel(spielort,datum)
)
tablespace Fussball;

drop table wurden_geschossen;
drop table hat_geschossen;
drop table spielt_mit_bei;
drop table tore;
drop table schiedsrichter;
drop table turnier;
drop table spiel;
drop table spieler;
drop table person;
drop table mannschaft;
