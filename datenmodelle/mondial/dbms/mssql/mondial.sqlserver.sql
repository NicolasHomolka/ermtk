drop table if exists glauben;
drop table if exists gelegenIn;
drop table if exists gelegen;
drop table if exists FlussAufInsel;
drop table if exists SeeAufInsel;
drop table if exists BergAufInsel;
drop table if exists InselIn;
drop table if exists VerschmilztMit;
drop table if exists geo_Muendung;
drop table if exists geo_Quelle;
drop table if exists geo_See;
drop table if exists geo_Meer;
drop table if exists geo_Fluss;
drop table if exists geo_Insel;
drop table if exists geo_Wueste;
drop table if exists geo_Berg;
drop table if exists FlussDurch;
drop table if exists Graenze;
drop table if exists istMitglied;
drop table if exists umfasst;
drop table if exists Flughafen;
drop table if exists Fluss;
drop table if exists Meer;
drop table if exists See;
drop table if exists Insel;
drop table if exists Wueste;
drop table if exists Berg;
drop table if exists Organisation;
drop table if exists Kontinent;
drop table if exists lokalerStadtName;
drop table if exists andererStadtName;
drop table if exists StadtBevoelkerung;
drop table if exists lokalerProvinzname;
drop table if exists andererProvinzname;
drop table if exists ProvinzBevoelkerung;
drop table if exists andererLaendername;
drop table if exists LandesBevoelkerung;
drop table if exists EthnischeGruppe;
drop table if exists Religion;
drop table if exists Sprache;
drop table if exists Politik;
drop table if exists Bevoelkerung;
drop table if exists Wirtschaft;
drop table if exists Provinz;
drop table if exists Stadt;
drop table if exists Land;
go

--Created from <ent>
create table Land(
    Name         varchar(132)  not null
,   Code         varchar(132)  not null primary key
,   Hauptstadt   varchar(132)  not null
,   Provinz      varchar(132)  not null
,   Gebietsgroesse varchar(132)  not null
,   Bevoelkerung varchar(132)  not null
);
go

--Created from <ent>
create table Stadt(
    Name        varchar(132)  not null
,   Land        varchar(132)  not null
,   Provinz     varchar(132)  not null
,   Bevoelkerung varchar(132)  not null
,   Breitengrad varchar(132)  not null
,   Laengengrad varchar(132)  not null
,   Hoehe       varchar(132)  not null
,   primary key(Name, Land, Provinz)
);
go

--Created from <ent>
create table Provinz(
    Name         varchar(132)  not null
,   Land         varchar(132)  not null
,   Bevoelkerung varchar(132)  not null
,   Gebietsgroesse varchar(132)  not null
,   Hauptstadt   varchar(132)  not null
,   HauptProvinz varchar(132)  not null
,   primary key(Name, Land)
);
go

--Created from <ent>
create table Wirtschaft(
    Land             varchar(132)  not null primary key
,   BIP              varchar(132)  not null
,   Landwirtschaft   varchar(132)  not null
,   Dienstleistungen varchar(132)  not null
,   Industrie        varchar(132)  not null
,   Inflation        varchar(132)  not null
,   Arbeitslosigkeit varchar(132)  not null
);
go

--Created from <ent>
create table Bevoelkerung(
    Land                     varchar(132)  not null primary key
,   Bevoelkerungswachstum    varchar(132)  not null
,   Kindersterblichkeitsrate varchar(132)  not null
);
go

--Created from <ent>
create table Politik(
    Land           varchar(132)  not null primary key
,   Unabhaengigkeit varchar(132)  not null
,   WarAbhaengig   varchar(132)  not null
,   Abhaengig      varchar(132)  not null
,   Regierung      varchar(132)  not null
);
go

--Created from <ent>
create table Sprache(
    Land        varchar(132)  not null
,   Name        varchar(132)  not null
,   Prozentsatz varchar(132)  not null
,   primary key(Land, Name)
);
go

--Created from <ent>
create table Religion(
    Land        varchar(132)  not null
,   Name        varchar(132)  not null
,   Prozentsatz varchar(132)  not null
,   primary key(Land, Name)
);
go

--Created from <ent>
create table EthnischeGruppe(
    Land        varchar(132)  not null
,   Name        varchar(132)  not null
,   Prozentsatz varchar(132)  not null
,   primary key(Land, Name)
);
go

--Created from <ent>
create table LandesBevoelkerung(
    Land        varchar(132)  not null
,   Jahr        varchar(132)  not null
,   Bevoelkerung varchar(132)  not null
,   primary key(Land, Jahr)
);
go

--Created from <ent>
create table andererLaendername(
    Land        varchar(132)  not null primary key
,   andererName varchar(132)  not null
);
go

--Created from <ent>
create table ProvinzBevoelkerung(
    Provinz     varchar(132)  not null
,   Land        varchar(132)  not null
,   Jahr        varchar(132)  not null
,   Bevoelkerung varchar(132)  not null
,   primary key(Provinz, Land, Jahr)
);
go

--Created from <ent>
create table andererProvinzname(
    Provinz     varchar(132)  not null
,   Land        varchar(132)  not null
,   andererName varchar(132)  not null
,   primary key(Provinz, Land, andererName)
);
go

--Created from <ent>
create table lokalerProvinzname(
    Provinz     varchar(132)  not null
,   Land        varchar(132)  not null
,   lokalerName varchar(132)  not null
,   primary key(Provinz, Land)
);
go

--Created from <ent>
create table StadtBevoelkerung(
    Stadt       varchar(132)  not null
,   Land        varchar(132)  not null
,   Provinz     varchar(132)  not null
,   Jahr        varchar(132)  not null
,   Bevoelkerung varchar(132)  not null
,   primary key(Stadt, Land, Provinz, Jahr)
);
go

--Created from <ent>
create table andererStadtName(
    Stadt       varchar(132)  not null
,   Land        varchar(132)  not null
,   Provinz     varchar(132)  not null
,   andererName varchar(132)  not null
,   primary key(Stadt, Land, Provinz, andererName)
);
go

--Created from <ent>
create table lokalerStadtName(
    Stadt       varchar(132)  not null
,   Land        varchar(132)  not null
,   Provinz     varchar(132)  not null
,   lokalerName varchar(132)  not null
,   primary key(Stadt, Land, Provinz)
);
go

--Created from <ent>
create table Kontinent(
    Name         varchar(132)  not null primary key
,   Gebietsgroesse varchar(132)  not null
);
go

--Created from <ent>
create table Organisation(
    Abkuerzung varchar(132)  not null primary key
,   Name      varchar(132)  not null
,   Stadt     varchar(132)  not null
,   Land      varchar(132)  not null
,   Provinz   varchar(132)  not null
,   Etabliert varchar(132)  not null
,   constraint fk_Stadt1
      foreign key(Name, Land, Provinz)
      references Stadt(Name, Land, Provinz)
);
go

--Created from <ent>
create table Berg(
    Name        varchar(132)  not null primary key
,   Berge       varchar(132)  not null
,   Hoehe       varchar(132)  not null
,   Typ         varchar(132)  not null
,   Koordinaten varchar(132)  not null
);
go

--Created from <ent>
create table Wueste(
    Name         varchar(132)  not null primary key
,   Gebietsgroesse varchar(132)  not null
,   Koordinaten  varchar(132)  not null
);
go

--Created from <ent>
create table Insel(
    Name         varchar(132)  not null primary key
,   Inseln       varchar(132)  not null
,   Gebietsgroesse varchar(132)  not null
,   Hoehe        varchar(132)  not null
,   Typ          varchar(132)  not null
,   Koordinaten  varchar(132)  not null
);
go

--Created from <ent>
create table See(
    Name         varchar(132)  not null primary key
,   Fluss        varchar(132)  not null
,   Gebietsgroesse varchar(132)  not null
,   Hoehe        varchar(132)  not null
,   Tiefe        varchar(132)  not null
,   Typ          varchar(132)  not null
,   Koordinaten  varchar(132)  not null
);
go

--Created from <ent>
create table Meer(
    Name         varchar(132)  not null primary key
,   Gebietsgroesse varchar(132)  not null
,   Tiefe        varchar(132)  not null
);
go

--Created from <ent>
create table Fluss(
    Name         varchar(132)  not null primary key
,   Fluss        varchar(132)  not null
,   See          varchar(132)  not null
,   Meer         varchar(132)  not null
,   Laenge       varchar(132)  not null
,   Gebietsgroesse varchar(132)  not null
,   Quelle       varchar(132)  not null
,   Berge        varchar(132)  not null
,   QuellenHoehe varchar(132)  not null
,   Muendung     varchar(132)  not null
,   Muendungshoehe varchar(132)  not null
);
go

--Created from <ent>
create table Flughafen(
    IATACode          varchar(132)  not null primary key
,   Name              varchar(132)  not null
,   Land              varchar(132)  not null
,   Stadt             varchar(132)  not null
,   Provinz           varchar(132)  not null
,   Insel             varchar(132)  not null
,   Breitengrad       varchar(132)  not null
,   Laengengrad       varchar(132)  not null
,   Hoehe             varchar(132)  not null
,   gmtZeitabweichung varchar(132)  not null
,   constraint fk_Stadt2
      foreign key(Name, Land, Provinz)
      references Stadt(Name, Land, Provinz)
);
go

--Created from a m:n relation
create table umfasst(
    Land_Code      varchar(132)  not null references Land(Code)
,   Kontinent_Name varchar(132)  not null references Kontinent(Name)
,   Prozentsatz    varchar(132)  not null
,   primary key(Land_Code, Kontinent_Name)
);
go

--Created from a m:n relation
create table istMitglied(
    Land_Code              varchar(132)  not null references Land(Code)
,   Organisation_Abkuerzung varchar(132)  not null references Organisation(Abkuerzung)
,   Typ                    varchar(132)  not null
,   primary key(Land_Code, Organisation_Abkuerzung)
);
go

--Created from a m:n relation
create table Graenze(
    Land_Code  varchar(132)  not null references Land(Code)
,   Land_Code2 varchar(132)  not null references Land(Code)
,   Laenge     varchar(132)  not null
,   primary key(Land_Code, Land_Code2)
);
go

--Created from a m:n relation
create table FlussDurch(
    Fluss_Name varchar(132)  not null references Fluss(Name)
,   See_Name   varchar(132)  not null references See(Name)
,   primary key(Fluss_Name, See_Name)
);
go

--Created from a m:n relation
create table geo_Berg(
    Berg_Name    varchar(132)  not null references Berg(Name)
,   Provinz_Name varchar(132)  not null
,   Provinz_Land varchar(132)  not null
,   primary key(Berg_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz3
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);
go

--Created from a m:n relation
create table geo_Wueste(
    Wueste_Name  varchar(132)  not null references Wueste(Name)
,   Provinz_Name varchar(132)  not null
,   Provinz_Land varchar(132)  not null
,   primary key(Wueste_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz4
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);
go

--Created from a m:n relation
create table geo_Insel(
    Insel_Name   varchar(132)  not null references Insel(Name)
,   Provinz_Name varchar(132)  not null
,   Provinz_Land varchar(132)  not null
,   primary key(Insel_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz5
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);
go

--Created from a m:n relation
create table geo_Fluss(
    Fluss_Name   varchar(132)  not null references Fluss(Name)
,   Provinz_Name varchar(132)  not null
,   Provinz_Land varchar(132)  not null
,   primary key(Fluss_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz6
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);
go

--Created from a m:n relation
create table geo_Meer(
    Meer_Name    varchar(132)  not null references Meer(Name)
,   Provinz_Name varchar(132)  not null
,   Provinz_Land varchar(132)  not null
,   primary key(Meer_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz7
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);
go

--Created from a m:n relation
create table geo_See(
    See_Name     varchar(132)  not null references See(Name)
,   Provinz_Name varchar(132)  not null
,   Provinz_Land varchar(132)  not null
,   primary key(See_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz8
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);
go

--Created from a m:n relation
create table geo_Quelle(
    Fluss_Name   varchar(132)  not null references Fluss(Name)
,   Provinz_Name varchar(132)  not null
,   Provinz_Land varchar(132)  not null
,   primary key(Fluss_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz9
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);
go

--Created from a m:n relation
create table geo_Muendung(
    Fluss_Name   varchar(132)  not null references Fluss(Name)
,   Provinz_Name varchar(132)  not null
,   Provinz_Land varchar(132)  not null
,   primary key(Fluss_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz10
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);
go

--Created from a m:n relation
create table VerschmilztMit(
    Meer_Name  varchar(132)  not null references Meer(Name)
,   Meer_Name2 varchar(132)  not null references Meer(Name)
,   primary key(Meer_Name, Meer_Name2)
);
go

--Created from a m:n relation
create table InselIn(
    Insel_Name varchar(132)  not null references Insel(Name)
,   Meer_Name  varchar(132)  not null references Meer(Name)
,   See_Name   varchar(132)  not null references See(Name)
,   Fluss_Name varchar(132)  not null references Fluss(Name)
,   primary key(Insel_Name, Meer_Name, See_Name, Fluss_Name)
);
go

--Created from a m:n relation
create table BergAufInsel(
    Berg_Name  varchar(132)  not null references Berg(Name)
,   Insel_Name varchar(132)  not null references Insel(Name)
,   primary key(Berg_Name, Insel_Name)
);
go

--Created from a m:n relation
create table SeeAufInsel(
    See_Name   varchar(132)  not null references See(Name)
,   Insel_Name varchar(132)  not null references Insel(Name)
,   primary key(See_Name, Insel_Name)
);
go

--Created from a m:n relation
create table FlussAufInsel(
    Fluss_Name varchar(132)  not null references Fluss(Name)
,   Insel_Name varchar(132)  not null references Insel(Name)
,   primary key(Fluss_Name, Insel_Name)
);
go

--Created from a m:n relation
create table gelegen(
    Stadt_Name    varchar(132)  not null
,   Stadt_Land    varchar(132)  not null
,   Stadt_Provinz varchar(132)  not null
,   Fluss_Name    varchar(132)  not null references Fluss(Name)
,   See_Name      varchar(132)  not null references See(Name)
,   Meer_Name     varchar(132)  not null references Meer(Name)
,   primary key(Stadt_Name, Stadt_Land, Stadt_Provinz, Fluss_Name, See_Name, Meer_Name)
,   constraint fk_Stadt11
      foreign key(Stadt_Name, Stadt_Land, Stadt_Provinz)
      references Stadt(Name, Land, Provinz)
);
go

--Created from a m:n relation
create table gelegenIn(
    Stadt_Name    varchar(132)  not null
,   Stadt_Land    varchar(132)  not null
,   Stadt_Provinz varchar(132)  not null
,   Insel_Name    varchar(132)  not null references Insel(Name)
,   primary key(Stadt_Name, Stadt_Land, Stadt_Provinz, Insel_Name)
,   constraint fk_Stadt12
      foreign key(Stadt_Name, Stadt_Land, Stadt_Provinz)
      references Stadt(Name, Land, Provinz)
);
go

--Created from a m:n relation
create table glauben(
    Land_Code     varchar(132)  not null references Land(Code)
,   Religion_Land varchar(132)  not null
,   Religion_Name varchar(132)  not null
,   primary key(Land_Code, Religion_Land, Religion_Name)
,   constraint fk_Religion13
      foreign key(Religion_Land, Religion_Name)
      references Religion(Land, Name)
);
go

