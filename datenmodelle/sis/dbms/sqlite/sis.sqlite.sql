--Created from <ent>
create table if not exists Person(
    svnr   text  not null primary key
,   nName  text  not null
,   vName  text  not null
,   gebDat text  not null
);

--Created from <ent>
create table if not exists Lehrer(
    lnr  text  not null
,   svnr text  not null primary key references Person (svnr)
);

--Created from <ent>
create table if not exists Schueler(
    MatrNr text  not null
,   svnr   text  not null primary key references Person (svnr)
);

--Created from <ent>
create table if not exists Abteilung(
    abkuerzung text  not null primary key
,   name       text  not null
);

--Created from <ent>
create table if not exists Gegenstand(
    abkuerzung  text  not null primary key
,   bezeichnung text  not null
);

--Created from <ent>
create table if not exists Lehrplan(
    jahrgang text  not null primary key
,   pStunden text  not null
,   tStunden text  not null
);

--Created from <ent>
create table if not exists Klasse(
    bezeichnung     text  not null primary key
,   jahrgang        text  not null
,   klassensprecher text  not null
,   kassierer       text  not null
);

--Created from <ent>
create table if not exists LVG(
    lvgNr  text  not null primary key
,   faktor text  not null
);

--Created from a m:n relation
create table if not exists ist_Geschwister_von(
    Schueler_svnr  text  not null references Schueler (svnr)
,   Schueler_svnr2 text  not null references Schueler (svnr)
,   primary key(Schueler_svnr, Schueler_svnr2)
);

--Created from a m:n relation
create table if not exists besitzt_Noten_fuer(
    Schueler_svnr         text  not null references Schueler (svnr)
,   Gegenstand_abkuerzung text  not null references Gegenstand (abkuerzung)
,   semesternote          text  not null
,   jahresnote            text  not null
,   primary key(Schueler_svnr, Gegenstand_abkuerzung)
);

--Created from a m:n relation
create table if not exists vermerkt(
    Gegenstand_abkuerzung text  not null primary key references Gegenstand (abkuerzung)
);

