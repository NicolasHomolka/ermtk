drop tablespace Mondial_Datenbank including contents;
create tablespace Mondial_Datenbank
  datafile 'tbs_Mondial_Datenbank'
    size 20M reuse;
--Created from <ent>
create table Land
(
    Land varchar(400)
,   Code varchar(400) primary key references Land (Code)
,   Hauptstadt varchar(400)
,   Gebietsgroesse varchar(400)
,   Bevoelkerung varchar(400)
,   Bevoelkerungungswachstum varchar(400)
,   Kindersterblichkeitsrate varchar(400)
,   BIP varchar(400)
,   Landwirtschaft varchar(400)
,   Dienstleistungen varchar(400)
,   Industrie varchar(400)
,   Inflation varchar(400)
,   Arbeitslosigkeit varchar(400)
,   Unabhaengigkeit varchar(400)
,   WarAbhaengig varchar(400)
,   Abhaengig varchar(400)
,   Regierung varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Provinz
(
    Code varchar(400) references Land (Code)
,   Provinz varchar(400)
,   Bevoelkerung varchar(400)
,   Gebietsgroesse varchar(400)
,   lokaler_Name varchar(400)
,   primary key(Code,Provinz)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Stadt
(
    Code varchar(400)
,   Provinz varchar(400)
,   Stadt varchar(400)
,   lokaler_name varchar(400)
,   Bevoelkerung varchar(400)
,   Breitengrad varchar(400)
,   Laengengrad varchar(400)
,   Hoehe varchar(400)
,   primary key(Code,Provinz,Stadt)
,   constraint fk_Provinz1
      foreign key(Code,Provinz)
      references Provinz(Code,Provinz)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Organisation
(
    Abkuerzung varchar(400) primary key
,   Organisation varchar(400)
,   Etabliert varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Flughafen
(
    IATACode varchar(400) primary key
,   Flughafen varchar(400)
,   Insel varchar(400)
,   Breitengrad varchar(400)
,   Laengengrad varchar(400)
,   Hoehe varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Sprache
(
    Sprache varchar(400) primary key
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Ethnische_Gruppe
(
    Ethnische_Gruppe varchar(400) primary key
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Religion
(
    Religion varchar(400) primary key
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Kontinent
(
    Kontinent varchar(400) primary key
,   Gebietsgroesse varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Berg
(
    Berg varchar(400) primary key
,   Berge varchar(400)
,   Hoehe varchar(400)
,   Typ varchar(400)
,   Laengengrad varchar(400)
,   Breitengrad varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Wueste
(
    Wueste varchar(400) primary key
,   Gebietsgroesse varchar(400)
,   Laengengrad varchar(400)
,   Breitengrad varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Insel
(
    Insel varchar(400) primary key
,   Inseln varchar(400)
,   Gebietsgroesse varchar(400)
,   Hoehe varchar(400)
,   Typ varchar(400)
,   Laengengrad varchar(400)
,   Breitengrad varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table See
(
    See varchar(400) primary key
,   Gebietsgroesse varchar(400)
,   Hoehe varchar(400)
,   Tiefe varchar(400)
,   Typ varchar(400)
,   Koordinaten varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Meer
(
    Meer varchar(400) primary key
,   Gebietsgroesse varchar(400)
,   Tiefe varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Fluss
(
    Fluss varchar(400) primary key
,   Laenge varchar(400)
,   Gebietsgroesse varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Quelle
(
    Fluss varchar(400) primary key references Fluss (Fluss)
,   Berg varchar(400)
,   Hoehe varchar(400)
,   Laengengrad varchar(400)
,   Breitengrad varchar(400)
)
tablespace Mondial_Datenbank;

--Created from <ent>
create table Muendung
(
    Fluss varchar(400) primary key references Fluss (Fluss)
,   Hoehe varchar(400)
,   Laengengrad varchar(400)
,   Breitengrad varchar(400)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table sprechen
(
    Land_Code varchar(400) references Land (Code)
,   Sprache_Sprache varchar(400) references Sprache (Sprache)
,   Prozentsatz varchar(400)
,   primary key(Land_Code,Sprache_Sprache)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table gehoert
(
    Land_Code varchar(400) references Land (Code)
,   Ethnische_Gruppe_Ethnische_Gru varchar(400) references Ethnische_Gruppe (Ethnische_Gruppe)
,   Prozentsatz varchar(400)
,   primary key(Land_Code,Ethnische_Gruppe_Ethnische_Gru)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table glauben
(
    Land_Code varchar(400) references Land (Code)
,   Religion_Religion varchar(400) references Religion (Religion)
,   Prozentsatz varchar(400)
,   primary key(Land_Code,Religion_Religion)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table umfasst
(
    Land_Code varchar(400) references Land (Code)
,   Kontinent_Kontinent varchar(400) references Kontinent (Kontinent)
,   Prozentsatz varchar(400)
,   primary key(Land_Code,Kontinent_Kontinent)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table istMitglied
(
    Land_Code varchar(400) references Land (Code)
,   Organisation_Abkuerzung varchar(400) references Organisation (Abkuerzung)
,   Typ varchar(400)
,   primary key(Land_Code,Organisation_Abkuerzung)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Grenze
(
    Land_Code varchar(400) references Land (Code)
,   Land_Code2 varchar(400) references Land (Code)
,   Laenge varchar(400)
,   primary key(Land_Code,Land_Code2)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table nahe
(
    Stadt_Code varchar(400)
,   Stadt_Provinz varchar(400)
,   Stadt_Stadt varchar(400)
,   Flughafen_IATACode varchar(400) references Flughafen (IATACode)
,   primary key(Stadt_Code,Stadt_Provinz,Stadt_Stadt,Flughafen_IATACode)
,   constraint fk_Stadt2
      foreign key(Stadt_Code,Stadt_Provinz,Stadt_Stadt)
      references Stadt(Code,Provinz,Stadt)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Wueste_in_Provinz
(
    Provinz_Code varchar(400)
,   Provinz_Provinz varchar(400)
,   Wueste_Wueste varchar(400) references Wueste (Wueste)
,   primary key(Provinz_Code,Provinz_Provinz,Wueste_Wueste)
,   constraint fk_Provinz3
      foreign key(Provinz_Code,Provinz_Provinz)
      references Provinz(Code,Provinz)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Berg_in_Provinz
(
    Provinz_Code varchar(400)
,   Provinz_Provinz varchar(400)
,   Berg_Berg varchar(400) references Berg (Berg)
,   primary key(Provinz_Code,Provinz_Provinz,Berg_Berg)
,   constraint fk_Provinz4
      foreign key(Provinz_Code,Provinz_Provinz)
      references Provinz(Code,Provinz)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Insel_in_Provinz
(
    Provinz_Code varchar(400)
,   Provinz_Provinz varchar(400)
,   Insel_Insel varchar(400) references Insel (Insel)
,   primary key(Provinz_Code,Provinz_Provinz,Insel_Insel)
,   constraint fk_Provinz5
      foreign key(Provinz_Code,Provinz_Provinz)
      references Provinz(Code,Provinz)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Meer_in_Provinz
(
    Provinz_Code varchar(400)
,   Provinz_Provinz varchar(400)
,   Meer_Meer varchar(400) references Meer (Meer)
,   primary key(Provinz_Code,Provinz_Provinz,Meer_Meer)
,   constraint fk_Provinz6
      foreign key(Provinz_Code,Provinz_Provinz)
      references Provinz(Code,Provinz)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Fluss_in_Provinz
(
    Provinz_Code varchar(400)
,   Provinz_Provinz varchar(400)
,   Fluss_Fluss varchar(400) references Fluss (Fluss)
,   primary key(Provinz_Code,Provinz_Provinz,Fluss_Fluss)
,   constraint fk_Provinz7
      foreign key(Provinz_Code,Provinz_Provinz)
      references Provinz(Code,Provinz)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table See_in_Provinz
(
    Provinz_Code varchar(400)
,   Provinz_Provinz varchar(400)
,   See_See varchar(400) references See (See)
,   primary key(Provinz_Code,Provinz_Provinz,See_See)
,   constraint fk_Provinz8
      foreign key(Provinz_Code,Provinz_Provinz)
      references Provinz(Code,Provinz)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Berg_auf_Insel
(
    Insel_Insel varchar(400) references Insel (Insel)
,   Berg_Berg varchar(400) references Berg (Berg)
,   primary key(Insel_Insel,Berg_Berg)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Insel_in_Meer
(
    Insel_Insel varchar(400) references Insel (Insel)
,   Meer_Meer varchar(400) references Meer (Meer)
,   primary key(Insel_Insel,Meer_Meer)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Insel_in_Fluss
(
    Insel_Insel varchar(400) references Insel (Insel)
,   Fluss_Fluss varchar(400) references Fluss (Fluss)
,   primary key(Insel_Insel,Fluss_Fluss)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Insel_in_See
(
    Insel_Insel varchar(400) references Insel (Insel)
,   See_See varchar(400) references See (See)
,   primary key(Insel_Insel,See_See)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Flughafen_auf_Insel
(
    Insel_Insel varchar(400) references Insel (Insel)
,   Flughafen_IATACode varchar(400) references Flughafen (IATACode)
,   primary key(Insel_Insel,Flughafen_IATACode)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Stadt_bei_Meer
(
    Stadt_Code varchar(400)
,   Stadt_Provinz varchar(400)
,   Stadt_Stadt varchar(400)
,   Meer_Meer varchar(400) references Meer (Meer)
,   primary key(Stadt_Code,Stadt_Provinz,Stadt_Stadt,Meer_Meer)
,   constraint fk_Stadt9
      foreign key(Stadt_Code,Stadt_Provinz,Stadt_Stadt)
      references Stadt(Code,Provinz,Stadt)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Stadt_bei_Fluss
(
    Stadt_Code varchar(400)
,   Stadt_Provinz varchar(400)
,   Stadt_Stadt varchar(400)
,   Fluss_Fluss varchar(400) references Fluss (Fluss)
,   primary key(Stadt_Code,Stadt_Provinz,Stadt_Stadt,Fluss_Fluss)
,   constraint fk_Stadt10
      foreign key(Stadt_Code,Stadt_Provinz,Stadt_Stadt)
      references Stadt(Code,Provinz,Stadt)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Stadt_bei_See
(
    Stadt_Code varchar(400)
,   Stadt_Provinz varchar(400)
,   Stadt_Stadt varchar(400)
,   See_See varchar(400) references See (See)
,   primary key(Stadt_Code,Stadt_Provinz,Stadt_Stadt,See_See)
,   constraint fk_Stadt11
      foreign key(Stadt_Code,Stadt_Provinz,Stadt_Stadt)
      references Stadt(Code,Provinz,Stadt)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table muendet_in_See
(
    Muendung_Fluss varchar(400) references Muendung (Fluss)
,   See_See varchar(400) references See (See)
,   primary key(Muendung_Fluss,See_See)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table muendet_in_Fluss
(
    Muendung_Fluss varchar(400) references Muendung (Fluss)
,   Fluss_Fluss varchar(400) references Fluss (Fluss)
,   primary key(Muendung_Fluss,Fluss_Fluss)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table muendet_in_Meer
(
    Muendung_Fluss varchar(400) references Muendung (Fluss)
,   Meer_Meer varchar(400) references Meer (Meer)
,   primary key(Muendung_Fluss,Meer_Meer)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Quelle_in_Provinz
(
    Quelle_Fluss varchar(400) references Quelle (Fluss)
,   Provinz_Code varchar(400)
,   Provinz_Provinz varchar(400)
,   primary key(Quelle_Fluss,Provinz_Code,Provinz_Provinz)
,   constraint fk_Provinz12
      foreign key(Provinz_Code,Provinz_Provinz)
      references Provinz(Code,Provinz)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Muendung_in_Provinz
(
    Quelle_Fluss varchar(400) references Quelle (Fluss)
,   Muendung_Fluss varchar(400) references Muendung (Fluss)
,   primary key(Quelle_Fluss,Muendung_Fluss)
)
tablespace Mondial_Datenbank;

--Created from a m:n relation
create table Hauptsitz
(
    Organisation_Abkuerzung varchar(400) references Organisation (Abkuerzung)
,   Stadt_Code varchar(400)
,   Stadt_Provinz varchar(400)
,   Stadt_Stadt varchar(400)
,   primary key(Organisation_Abkuerzung,Stadt_Code,Stadt_Provinz,Stadt_Stadt)
,   constraint fk_Stadt13
      foreign key(Stadt_Code,Stadt_Provinz,Stadt_Stadt)
      references Stadt(Code,Provinz,Stadt)
)
tablespace Mondial_Datenbank;

drop table Hauptsitz;
drop table Muendung_in_Provinz;
drop table Quelle_in_Provinz;
drop table muendet_in_Meer;
drop table muendet_in_Fluss;
drop table muendet_in_See;
drop table Stadt_bei_See;
drop table Stadt_bei_Fluss;
drop table Stadt_bei_Meer;
drop table Flughafen_auf_Insel;
drop table Insel_in_See;
drop table Insel_in_Fluss;
drop table Insel_in_Meer;
drop table Berg_auf_Insel;
drop table See_in_Provinz;
drop table Fluss_in_Provinz;
drop table Meer_in_Provinz;
drop table Insel_in_Provinz;
drop table Berg_in_Provinz;
drop table Wueste_in_Provinz;
drop table nahe;
drop table Grenze;
drop table istMitglied;
drop table umfasst;
drop table glauben;
drop table gehoert;
drop table sprechen;
drop table Muendung;
drop table Quelle;
drop table Fluss;
drop table Meer;
drop table See;
drop table Insel;
drop table Wueste;
drop table Berg;
drop table Kontinent;
drop table Religion;
drop table Ethnische_Gruppe;
drop table Sprache;
drop table Flughafen;
drop table Organisation;
drop table Stadt;
drop table Provinz;
drop table Land;
