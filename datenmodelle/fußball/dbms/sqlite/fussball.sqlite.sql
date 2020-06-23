--Created from <ent>
create table if not exists mannschaft(
    name          text  not null primary key
,   gruendungsjahr text  not null
,   adresse       text  not null
);

--Created from <ent>
create table if not exists person(
    svnr         text  not null primary key
,   name         text  not null
,   wohnadresse  text  not null
,   geburtsdatum text  not null
);

--Created from <ent>
create table if not exists spieler(
    spielposition text  not null
,   svnr          text  not null primary key references person (svnr)
);

--Created from <ent>
create table if not exists "spiel"(
    spielort        text  not null
,   "datum"         text  not null
,   mannschaft_heim text  not null
,   mannschaft_ausw text  not null
,   schiedsrichter  text  not null
,   ergebnis        text  not null
,   primary key(spielort, "datum")
);

--Created from <ent>
create table if not exists turnier(
    nummer       text  not null
,   name         text  not null
,   begindatum   text  not null
,   enddatum     text  not null
,   mannschaften text  not null
,   primary key(nummer, name)
);

--Created from <ent>
create table if not exists schiedsrichter(
    datum_pruefung      text  not null
,   berechtigungsklasse text  not null
,   svnr                text  not null primary key references person (svnr)
);

--Created from <ent>
create table if not exists tore(
    anzahl_tore text  not null
);

--Created from a m:n relation
create table if not exists spielt_mit_bei(
    mannschaft_name text  not null references mannschaft (name)
,   spiel_spielort  text  not null
,   "spiel_datum"   text  not null
,   primary key(mannschaft_name, spiel_spielort, "spiel_datum")
,   constraint fk_spiel1
      foreign key(spiel_spielort, "spiel_datum")
      references "spiel"(spielort, "datum")
);

--Created from a m:n relation
create table if not exists hat_geschossen(
    spieler_svnr text  not null primary key references spieler (svnr)
);

--Created from a m:n relation
create table if not exists wurden_geschossen(
    spiel_spielort text  not null
,   "spiel_datum"  text  not null
,   primary key(spiel_spielort, "spiel_datum")
,   constraint fk_spiel2
      foreign key(spiel_spielort, "spiel_datum")
      references "spiel"(spielort, "datum")
);

