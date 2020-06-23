--Created from <ent>
create table Land
(
    Land varchar(300)
,   Code varchar(300) primary key references Land (Code)
,   Hauptstadt varchar(300)
,   Gebietsgroesse varchar(300)
,   Bevoelkerung varchar(300)
,   Bevoelkerungungswachstum varchar(300)
,   Kindersterblichkeitsrate varchar(300)
,   BIP varchar(300)
,   Landwirtschaft varchar(300)
,   Dienstleistungen varchar(300)
,   Industrie varchar(300)
,   Inflation varchar(300)
,   Arbeitslosigkeit varchar(300)
,   Unabhaengigkeit varchar(300)
,   WarAbhaengig varchar(300)
,   Abhaengig varchar(300)
,   Regierung varchar(300)
);

--Created from <ent>
create table Provinz
(
    Code varchar(300) references Land (Code)
,   Provinz varchar(300)
,   Bevoelkerung varchar(300)
,   Gebietsgroesse varchar(300)
,   lokaler_Name varchar(300)
,   primary key(Code,Provinz)
);

--Created from <ent>
create table Stadt
(
    Code varchar(300)
,   Provinz varchar(300)
,   Stadt varchar(300)
,   lokaler_name varchar(300)
,   Bevoelkerung varchar(300)
,   Breitengrad varchar(300)
,   Laengengrad varchar(300)
,   Hoehe varchar(300)
,   primary key(Code,Provinz,Stadt)
,   foreign key(Code, Provinz) references Provinz(Code,Provinz)
);

--Created from <ent>
create table Organisation
(
    Abkuerzung varchar(300) primary key
,   Organisation varchar(300)
,   Etabliert varchar(300)
);

--Created from <ent>
create table Flughafen
(
    IATACode varchar(300) primary key
,   Flughafen varchar(300)
,   Insel varchar(300)
,   Breitengrad varchar(300)
,   Laengengrad varchar(300)
,   Hoehe varchar(300)
);

--Created from <ent>
create table Sprache
(
    Sprache varchar(300) primary key
);

--Created from <ent>
create table Ethnische_Gruppe
(
    Ethnische_Gruppe varchar(300) primary key
);

--Created from <ent>
create table Religion
(
    Religion varchar(300) primary key
);

--Created from <ent>
create table Kontinent
(
    Kontinent varchar(300) primary key
,   Gebietsgroesse varchar(300)
);

--Created from <ent>
create table Berg
(
    Berg varchar(300) primary key
,   Berge varchar(300)
,   Hoehe varchar(300)
,   Typ varchar(300)
,   Laengengrad varchar(300)
,   Breitengrad varchar(300)
);

--Created from <ent>
create table Wueste
(
    Wueste varchar(300) primary key
,   Gebietsgroesse varchar(300)
,   Laengengrad varchar(300)
,   Breitengrad varchar(300)
);

--Created from <ent>
create table Insel
(
    Insel varchar(300) primary key
,   Inseln varchar(300)
,   Gebietsgroesse varchar(300)
,   Hoehe varchar(300)
,   Typ varchar(300)
,   Laengengrad varchar(300)
,   Breitengrad varchar(300)
);

--Created from <ent>
create table See
(
    See varchar(300) primary key
,   Gebietsgroesse varchar(300)
,   Hoehe varchar(300)
,   Tiefe varchar(300)
,   Typ varchar(300)
,   Koordinaten varchar(300)
);

--Created from <ent>
create table Meer
(
    Meer varchar(300) primary key
,   Gebietsgroesse varchar(300)
,   Tiefe varchar(300)
);

--Created from <ent>
create table Fluss
(
    Fluss varchar(300) primary key
,   Laenge varchar(300)
,   Gebietsgroesse varchar(300)
);

--Created from <ent>
create table Quelle
(
    Fluss varchar(300) primary key references Fluss (Fluss)
,   Berg varchar(300)
,   Hoehe varchar(300)
,   Laengengrad varchar(300)
,   Breitengrad varchar(300)
);

--Created from <ent>
create table Muendung
(
    Fluss varchar(300) primary key references Fluss (Fluss)
,   Hoehe varchar(300)
,   Laengengrad varchar(300)
,   Breitengrad varchar(300)
);

--Created from a m:n relation
create table sprechen
(
    Land_Code varchar(300) references Land (Code)
,   Sprache_Sprache varchar(300) references Sprache (Sprache)
,   Prozentsatz varchar(300)
,   primary key(Land_Code,Sprache_Sprache)
);

--Created from a m:n relation
create table gehoert
(
    Land_Code varchar(300) references Land (Code)
,   Ethnische_Gruppe_Ethnische_Gru varchar(300) references Ethnische_Gruppe (Ethnische_Gruppe)
,   Prozentsatz varchar(300)
,   primary key(Land_Code,Ethnische_Gruppe_Ethnische_Gru)
);

--Created from a m:n relation
create table glauben
(
    Land_Code varchar(300) references Land (Code)
,   Religion_Religion varchar(300) references Religion (Religion)
,   Prozentsatz varchar(300)
,   primary key(Land_Code,Religion_Religion)
);

--Created from a m:n relation
create table umfasst
(
    Land_Code varchar(300) references Land (Code)
,   Kontinent_Kontinent varchar(300) references Kontinent (Kontinent)
,   Prozentsatz varchar(300)
,   primary key(Land_Code,Kontinent_Kontinent)
);

--Created from a m:n relation
create table istMitglied
(
    Land_Code varchar(300) references Land (Code)
,   Organisation_Abkuerzung varchar(300) references Organisation (Abkuerzung)
,   Typ varchar(300)
,   primary key(Land_Code,Organisation_Abkuerzung)
);

--Created from a m:n relation
create table Grenze
(
    Land_Code varchar(300) references Land (Code)
,   Land_Code2 varchar(300) references Land (Code)
,   Laenge varchar(300)
,   primary key(Land_Code,Land_Code2)
);

--Created from a m:n relation
create table nahe
(
    Stadt_Code varchar(300)
,   Stadt_Provinz varchar(300)
,   Stadt_Stadt varchar(300)
,   Flughafen_IATACode varchar(300) references Flughafen (IATACode)
,   primary key(Stadt_Code,Stadt_Provinz,Stadt_Stadt,Flughafen_IATACode)
,   foreign key(Stadt_Code, Stadt_Provinz, Stadt_Stadt) references Stadt(Code,Provinz,Stadt)
);

--Created from a m:n relation
create table Wueste_in_Provinz
(
    Provinz_Code varchar(300)
,   Provinz_Provinz varchar(300)
,   Wueste_Wueste varchar(300) references Wueste (Wueste)
,   primary key(Provinz_Code,Provinz_Provinz,Wueste_Wueste)
,   foreign key(Provinz_Code, Provinz_Provinz) references Provinz(Code,Provinz)
);

--Created from a m:n relation
create table Berg_in_Provinz
(
    Provinz_Code varchar(300)
,   Provinz_Provinz varchar(300)
,   Berg_Berg varchar(300) references Berg (Berg)
,   primary key(Provinz_Code,Provinz_Provinz,Berg_Berg)
,   foreign key(Provinz_Code, Provinz_Provinz) references Provinz(Code,Provinz)
);

--Created from a m:n relation
create table Insel_in_Provinz
(
    Provinz_Code varchar(300)
,   Provinz_Provinz varchar(300)
,   Insel_Insel varchar(300) references Insel (Insel)
,   primary key(Provinz_Code,Provinz_Provinz,Insel_Insel)
,   foreign key(Provinz_Code, Provinz_Provinz) references Provinz(Code,Provinz)
);

--Created from a m:n relation
create table Meer_in_Provinz
(
    Provinz_Code varchar(300)
,   Provinz_Provinz varchar(300)
,   Meer_Meer varchar(300) references Meer (Meer)
,   primary key(Provinz_Code,Provinz_Provinz,Meer_Meer)
,   foreign key(Provinz_Code, Provinz_Provinz) references Provinz(Code,Provinz)
);

--Created from a m:n relation
create table Fluss_in_Provinz
(
    Provinz_Code varchar(300)
,   Provinz_Provinz varchar(300)
,   Fluss_Fluss varchar(300) references Fluss (Fluss)
,   primary key(Provinz_Code,Provinz_Provinz,Fluss_Fluss)
,   foreign key(Provinz_Code, Provinz_Provinz) references Provinz(Code,Provinz)
);

--Created from a m:n relation
create table See_in_Provinz
(
    Provinz_Code varchar(300)
,   Provinz_Provinz varchar(300)
,   See_See varchar(300) references See (See)
,   primary key(Provinz_Code,Provinz_Provinz,See_See)
,   foreign key(Provinz_Code, Provinz_Provinz) references Provinz(Code,Provinz)
);

--Created from a m:n relation
create table Berg_auf_Insel
(
    Insel_Insel varchar(300) references Insel (Insel)
,   Berg_Berg varchar(300) references Berg (Berg)
,   primary key(Insel_Insel,Berg_Berg)
);

--Created from a m:n relation
create table Insel_in_Meer
(
    Insel_Insel varchar(300) references Insel (Insel)
,   Meer_Meer varchar(300) references Meer (Meer)
,   primary key(Insel_Insel,Meer_Meer)
);

--Created from a m:n relation
create table Insel_in_Fluss
(
    Insel_Insel varchar(300) references Insel (Insel)
,   Fluss_Fluss varchar(300) references Fluss (Fluss)
,   primary key(Insel_Insel,Fluss_Fluss)
);

--Created from a m:n relation
create table Insel_in_See
(
    Insel_Insel varchar(300) references Insel (Insel)
,   See_See varchar(300) references See (See)
,   primary key(Insel_Insel,See_See)
);

--Created from a m:n relation
create table Flughafen_auf_Insel
(
    Insel_Insel varchar(300) references Insel (Insel)
,   Flughafen_IATACode varchar(300) references Flughafen (IATACode)
,   primary key(Insel_Insel,Flughafen_IATACode)
);

--Created from a m:n relation
create table Stadt_bei_Meer
(
    Stadt_Code varchar(300)
,   Stadt_Provinz varchar(300)
,   Stadt_Stadt varchar(300)
,   Meer_Meer varchar(300) references Meer (Meer)
,   primary key(Stadt_Code,Stadt_Provinz,Stadt_Stadt,Meer_Meer)
,   foreign key(Stadt_Code, Stadt_Provinz, Stadt_Stadt) references Stadt(Code,Provinz,Stadt)
);

--Created from a m:n relation
create table Stadt_bei_Fluss
(
    Stadt_Code varchar(300)
,   Stadt_Provinz varchar(300)
,   Stadt_Stadt varchar(300)
,   Fluss_Fluss varchar(300) references Fluss (Fluss)
,   primary key(Stadt_Code,Stadt_Provinz,Stadt_Stadt,Fluss_Fluss)
,   foreign key(Stadt_Code, Stadt_Provinz, Stadt_Stadt) references Stadt(Code,Provinz,Stadt)
);

--Created from a m:n relation
create table Stadt_bei_See
(
    Stadt_Code varchar(300)
,   Stadt_Provinz varchar(300)
,   Stadt_Stadt varchar(300)
,   See_See varchar(300) references See (See)
,   primary key(Stadt_Code,Stadt_Provinz,Stadt_Stadt,See_See)
,   foreign key(Stadt_Code, Stadt_Provinz, Stadt_Stadt) references Stadt(Code,Provinz,Stadt)
);

--Created from a m:n relation
create table muendet_in_See
(
    Muendung_Fluss varchar(300) references Muendung (Fluss)
,   See_See varchar(300) references See (See)
,   primary key(Muendung_Fluss,See_See)
);

--Created from a m:n relation
create table muendet_in_Fluss
(
    Muendung_Fluss varchar(300) references Muendung (Fluss)
,   Fluss_Fluss varchar(300) references Fluss (Fluss)
,   primary key(Muendung_Fluss,Fluss_Fluss)
);

--Created from a m:n relation
create table muendet_in_Meer
(
    Muendung_Fluss varchar(300) references Muendung (Fluss)
,   Meer_Meer varchar(300) references Meer (Meer)
,   primary key(Muendung_Fluss,Meer_Meer)
);

--Created from a m:n relation
create table Quelle_in_Provinz
(
    Quelle_Fluss varchar(300) references Quelle (Fluss)
,   Provinz_Code varchar(300)
,   Provinz_Provinz varchar(300)
,   primary key(Quelle_Fluss,Provinz_Code,Provinz_Provinz)
,   foreign key(Provinz_Code, Provinz_Provinz) references Provinz(Code,Provinz)
);

--Created from a m:n relation
create table Muendung_in_Provinz
(
    Quelle_Fluss varchar(300) references Quelle (Fluss)
,   Muendung_Fluss varchar(300) references Muendung (Fluss)
,   primary key(Quelle_Fluss,Muendung_Fluss)
);

--Created from a m:n relation
create table Hauptsitz
(
    Organisation_Abkuerzung varchar(300) references Organisation (Abkuerzung)
,   Stadt_Code varchar(300)
,   Stadt_Provinz varchar(300)
,   Stadt_Stadt varchar(300)
,   primary key(Organisation_Abkuerzung,Stadt_Code,Stadt_Provinz,Stadt_Stadt)
,   foreign key(Stadt_Code, Stadt_Provinz, Stadt_Stadt) references Stadt(Code,Provinz,Stadt)
);

drop table if exists Hauptsitz;
drop table if exists Muendung_in_Provinz;
drop table if exists Quelle_in_Provinz;
drop table if exists muendet_in_Meer;
drop table if exists muendet_in_Fluss;
drop table if exists muendet_in_See;
drop table if exists Stadt_bei_See;
drop table if exists Stadt_bei_Fluss;
drop table if exists Stadt_bei_Meer;
drop table if exists Flughafen_auf_Insel;
drop table if exists Insel_in_See;
drop table if exists Insel_in_Fluss;
drop table if exists Insel_in_Meer;
drop table if exists Berg_auf_Insel;
drop table if exists See_in_Provinz;
drop table if exists Fluss_in_Provinz;
drop table if exists Meer_in_Provinz;
drop table if exists Insel_in_Provinz;
drop table if exists Berg_in_Provinz;
drop table if exists Wueste_in_Provinz;
drop table if exists nahe;
drop table if exists Grenze;
drop table if exists istMitglied;
drop table if exists umfasst;
drop table if exists glauben;
drop table if exists gehoert;
drop table if exists sprechen;
drop table if exists Muendung;
drop table if exists Quelle;
drop table if exists Fluss;
drop table if exists Meer;
drop table if exists See;
drop table if exists Insel;
drop table if exists Wueste;
drop table if exists Berg;
drop table if exists Kontinent;
drop table if exists Religion;
drop table if exists Ethnische_Gruppe;
drop table if exists Sprache;
drop table if exists Flughafen;
drop table if exists Organisation;
drop table if exists Stadt;
drop table if exists Provinz;
drop table if exists Land;
