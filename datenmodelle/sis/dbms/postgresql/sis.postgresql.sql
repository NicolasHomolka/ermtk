--Created from <ent>
create table Person
(
    svnr varchar(300) primary key
,   nName varchar(300)
,   vName varchar(300)
,   gebDat varchar(300)
);

--Created from <ent>
create table Lehrer
(
    lnr varchar(300)
,   svnr varchar(300) primary key references Person (svnr)
);

--Created from <ent>
create table Schueler
(
    MatrNr varchar(300)
,   svnr varchar(300) primary key references Person (svnr)
);

--Created from <ent>
create table Abteilung
(
    abkuerzung varchar(300) primary key
,   name varchar(300)
);

--Created from <ent>
create table Gegenstand
(
    abkuerzung varchar(300) primary key
,   bezeichnung varchar(300)
);

--Created from <ent>
create table Lehrplan
(
    jahrgang varchar(300) primary key
,   pStunden varchar(300)
,   tStunden varchar(300)
);

--Created from <ent>
create table Klasse
(
    bezeichnung varchar(300) primary key
,   jahrgang varchar(300)
,   klassensprecher varchar(300)
,   kassierer varchar(300)
);

--Created from <ent>
create table LVG
(
    lvgNr varchar(300) primary key
,   faktor varchar(300)
);

--Created from a m:n relation
create table ist_Geschwister_von
(
    Schueler_svnr varchar(300) references Schueler (svnr)
,   Schueler_svnr2 varchar(300) references Schueler (svnr)
,   primary key(Schueler_svnr,Schueler_svnr2)
);

--Created from a m:n relation
create table besitzt_Noten_fuer
(
    Schueler_svnr varchar(300) references Schueler (svnr)
,   Gegenstand_abkuerzung varchar(300) references Gegenstand (abkuerzung)
,   semesternote varchar(300)
,   jahresnote varchar(300)
,   primary key(Schueler_svnr,Gegenstand_abkuerzung)
);

--Created from a m:n relation
create table vermerkt
(
    Gegenstand_abkuerzung varchar(300) primary key references Gegenstand (abkuerzung)
);

drop table if exists vermerkt;
drop table if exists besitzt_Noten_fuer;
drop table if exists ist_Geschwister_von;
drop table if exists LVG;
drop table if exists Klasse;
drop table if exists Lehrplan;
drop table if exists Gegenstand;
drop table if exists Abteilung;
drop table if exists Schueler;
drop table if exists Lehrer;
drop table if exists Person;
