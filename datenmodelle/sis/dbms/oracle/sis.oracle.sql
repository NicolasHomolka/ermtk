drop tablespace Schulinformationssystem including contents;
create tablespace Schulinformationssystem
  datafile 'tbs_Schulinformationssystem'
    size 20M reuse;
--Created from <ent>
create table Person
(
    svnr varchar(400) primary key
,   nName varchar(400)
,   vName varchar(400)
,   gebDat varchar(400)
)
tablespace Schulinformationssystem;

--Created from <ent>
create table Lehrer
(
    lnr varchar(400)
,   svnr varchar(400) primary key references Person (svnr)
)
tablespace Schulinformationssystem;

--Created from <ent>
create table Schueler
(
    MatrNr varchar(400)
,   svnr varchar(400) primary key references Person (svnr)
)
tablespace Schulinformationssystem;

--Created from <ent>
create table Abteilung
(
    abkuerzung varchar(400) primary key
,   name varchar(400)
)
tablespace Schulinformationssystem;

--Created from <ent>
create table Gegenstand
(
    abkuerzung varchar(400) primary key
,   bezeichnung varchar(400)
)
tablespace Schulinformationssystem;

--Created from <ent>
create table Lehrplan
(
    jahrgang varchar(400) primary key
,   pStunden varchar(400)
,   tStunden varchar(400)
)
tablespace Schulinformationssystem;

--Created from <ent>
create table Klasse
(
    bezeichnung varchar(400) primary key
,   jahrgang varchar(400)
,   klassensprecher varchar(400)
,   kassierer varchar(400)
)
tablespace Schulinformationssystem;

--Created from <ent>
create table LVG
(
    lvgNr varchar(400) primary key
,   faktor varchar(400)
)
tablespace Schulinformationssystem;

--Created from a m:n relation
create table ist_Geschwister_von
(
    Schueler_svnr varchar(400) references Schueler (svnr)
,   Schueler_svnr2 varchar(400) references Schueler (svnr)
,   primary key(Schueler_svnr,Schueler_svnr2)
)
tablespace Schulinformationssystem;

--Created from a m:n relation
create table besitzt_Noten_fuer
(
    Schueler_svnr varchar(400) references Schueler (svnr)
,   Gegenstand_abkuerzung varchar(400) references Gegenstand (abkuerzung)
,   semesternote varchar(400)
,   jahresnote varchar(400)
,   primary key(Schueler_svnr,Gegenstand_abkuerzung)
)
tablespace Schulinformationssystem;

--Created from a m:n relation
create table vermerkt
(
    Gegenstand_abkuerzung varchar(400) primary key references Gegenstand (abkuerzung)
)
tablespace Schulinformationssystem;

drop table vermerkt;
drop table besitzt_Noten_fuer;
drop table ist_Geschwister_von;
drop table LVG;
drop table Klasse;
drop table Lehrplan;
drop table Gegenstand;
drop table Abteilung;
drop table Schueler;
drop table Lehrer;
drop table Person;
