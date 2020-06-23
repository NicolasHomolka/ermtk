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

#Created from <ent>
create table Person(
    svnr   varchar(132)  not null primary key
,   nName  varchar(132)  not null
,   vName  varchar(132)  not null
,   gebDat varchar(132)  not null
);

#Created from <ent>
create table Lehrer(
    lnr  varchar(132)  not null
,   svnr varchar(132)  not null primary key references Person (svnr)
);

#Created from <ent>
create table Schueler(
    MatrNr varchar(132)  not null
,   svnr   varchar(132)  not null primary key references Person (svnr)
);

#Created from <ent>
create table Abteilung(
    abkuerzung varchar(132)  not null primary key
,   name       varchar(132)  not null
);

#Created from <ent>
create table Gegenstand(
    abkuerzung  varchar(132)  not null primary key
,   bezeichnung varchar(132)  not null
);

#Created from <ent>
create table Lehrplan(
    jahrgang varchar(132)  not null primary key
,   pStunden varchar(132)  not null
,   tStunden varchar(132)  not null
);

#Created from <ent>
create table Klasse(
    bezeichnung     varchar(132)  not null primary key
,   jahrgang        varchar(132)  not null
,   klassensprecher varchar(132)  not null
,   kassierer       varchar(132)  not null
);

#Created from <ent>
create table LVG(
    lvgNr  varchar(132)  not null primary key
,   faktor varchar(132)  not null
);

#Created from a m:n relation
create table ist_Geschwister_von(
    Schueler_svnr  varchar(132)  not null references Schueler (svnr)
,   Schueler_svnr2 varchar(132)  not null references Schueler (svnr)
,   primary key(Schueler_svnr, Schueler_svnr2)
);

#Created from a m:n relation
create table besitzt_Noten_fuer(
    Schueler_svnr         varchar(132)  not null references Schueler (svnr)
,   Gegenstand_abkuerzung varchar(132)  not null references Gegenstand (abkuerzung)
,   semesternote          varchar(132)  not null
,   jahresnote            varchar(132)  not null
,   primary key(Schueler_svnr, Gegenstand_abkuerzung)
);

#Created from a m:n relation
create table vermerkt(
    Gegenstand_abkuerzung varchar(132)  not null primary key references Gegenstand (abkuerzung)
);

