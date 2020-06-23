--Created from <ent>
create table if not exists Land(
    Name         text  not null
,   Code         text  not null primary key
,   Hauptstadt   text  not null
,   Provinz      text  not null
,   Gebietsgroesse text  not null
,   Bevoelkerung text  not null
);

--Created from <ent>
create table if not exists Stadt(
    Name        text  not null
,   Land        text  not null
,   Provinz     text  not null
,   Bevoelkerung text  not null
,   Breitengrad text  not null
,   Laengengrad text  not null
,   Hoehe       text  not null
,   primary key(Name, Land, Provinz)
);

--Created from <ent>
create table if not exists Provinz(
    Name         text  not null
,   Land         text  not null
,   Bevoelkerung text  not null
,   Gebietsgroesse text  not null
,   Hauptstadt   text  not null
,   HauptProvinz text  not null
,   primary key(Name, Land)
);

--Created from <ent>
create table if not exists Wirtschaft(
    Land             text  not null primary key
,   BIP              text  not null
,   Landwirtschaft   text  not null
,   Dienstleistungen text  not null
,   Industrie        text  not null
,   Inflation        text  not null
,   Arbeitslosigkeit text  not null
);

--Created from <ent>
create table if not exists Bevoelkerung(
    Land                     text  not null primary key
,   Bevoelkerungswachstum    text  not null
,   Kindersterblichkeitsrate text  not null
);

--Created from <ent>
create table if not exists Politik(
    Land           text  not null primary key
,   Unabhaengigkeit text  not null
,   WarAbhaengig   text  not null
,   Abhaengig      text  not null
,   Regierung      text  not null
);

--Created from <ent>
create table if not exists Sprache(
    Land        text  not null
,   Name        text  not null
,   Prozentsatz text  not null
,   primary key(Land, Name)
);

--Created from <ent>
create table if not exists Religion(
    Land        text  not null
,   Name        text  not null
,   Prozentsatz text  not null
,   primary key(Land, Name)
);

--Created from <ent>
create table if not exists EthnischeGruppe(
    Land        text  not null
,   Name        text  not null
,   Prozentsatz text  not null
,   primary key(Land, Name)
);

--Created from <ent>
create table if not exists LandesBevoelkerung(
    Land        text  not null
,   Jahr        text  not null
,   Bevoelkerung text  not null
,   primary key(Land, Jahr)
);

--Created from <ent>
create table if not exists andererLaendername(
    Land        text  not null primary key
,   andererName text  not null
);

--Created from <ent>
create table if not exists ProvinzBevoelkerung(
    Provinz     text  not null
,   Land        text  not null
,   Jahr        text  not null
,   Bevoelkerung text  not null
,   primary key(Provinz, Land, Jahr)
);

--Created from <ent>
create table if not exists andererProvinzname(
    Provinz     text  not null
,   Land        text  not null
,   andererName text  not null
,   primary key(Provinz, Land, andererName)
);

--Created from <ent>
create table if not exists lokalerProvinzname(
    Provinz     text  not null
,   Land        text  not null
,   lokalerName text  not null
,   primary key(Provinz, Land)
);

--Created from <ent>
create table if not exists StadtBevoelkerung(
    Stadt       text  not null
,   Land        text  not null
,   Provinz     text  not null
,   Jahr        text  not null
,   Bevoelkerung text  not null
,   primary key(Stadt, Land, Provinz, Jahr)
);

--Created from <ent>
create table if not exists andererStadtName(
    Stadt       text  not null
,   Land        text  not null
,   Provinz     text  not null
,   andererName text  not null
,   primary key(Stadt, Land, Provinz, andererName)
);

--Created from <ent>
create table if not exists lokalerStadtName(
    Stadt       text  not null
,   Land        text  not null
,   Provinz     text  not null
,   lokalerName text  not null
,   primary key(Stadt, Land, Provinz)
);

--Created from <ent>
create table if not exists Kontinent(
    Name         text  not null primary key
,   Gebietsgroesse text  not null
);

--Created from <ent>
create table if not exists Organisation(
    Abkuerzung text  not null primary key
,   Name      text  not null
,   Stadt     text  not null
,   Land      text  not null
,   Provinz   text  not null
,   Etabliert text  not null
,   constraint fk_Stadt1
      foreign key(Name, Land, Provinz)
      references Stadt(Name, Land, Provinz)
);

--Created from <ent>
create table if not exists Berg(
    Name        text  not null primary key
,   Berge       text  not null
,   Hoehe       text  not null
,   Typ         text  not null
,   Koordinaten text  not null
);

--Created from <ent>
create table if not exists Wueste(
    Name         text  not null primary key
,   Gebietsgroesse text  not null
,   Koordinaten  text  not null
);

--Created from <ent>
create table if not exists Insel(
    Name         text  not null primary key
,   Inseln       text  not null
,   Gebietsgroesse text  not null
,   Hoehe        text  not null
,   Typ          text  not null
,   Koordinaten  text  not null
);

--Created from <ent>
create table if not exists See(
    Name         text  not null primary key
,   Fluss        text  not null
,   Gebietsgroesse text  not null
,   Hoehe        text  not null
,   Tiefe        text  not null
,   Typ          text  not null
,   Koordinaten  text  not null
);

--Created from <ent>
create table if not exists Meer(
    Name         text  not null primary key
,   Gebietsgroesse text  not null
,   Tiefe        text  not null
);

--Created from <ent>
create table if not exists Fluss(
    Name         text  not null primary key
,   Fluss        text  not null
,   See          text  not null
,   Meer         text  not null
,   Laenge       text  not null
,   Gebietsgroesse text  not null
,   Quelle       text  not null
,   Berge        text  not null
,   QuellenHoehe text  not null
,   Muendung     text  not null
,   Muendungshoehe text  not null
);

--Created from <ent>
create table if not exists Flughafen(
    IATACode          text  not null primary key
,   Name              text  not null
,   Land              text  not null
,   Stadt             text  not null
,   Provinz           text  not null
,   Insel             text  not null
,   Breitengrad       text  not null
,   Laengengrad       text  not null
,   Hoehe             text  not null
,   gmtZeitabweichung text  not null
,   constraint fk_Stadt2
      foreign key(Name, Land, Provinz)
      references Stadt(Name, Land, Provinz)
);

--Created from a m:n relation
create table if not exists umfasst(
    Land_Code      text  not null references Land (Code)
,   Kontinent_Name text  not null references Kontinent (Name)
,   Prozentsatz    text  not null
,   primary key(Land_Code, Kontinent_Name)
);

--Created from a m:n relation
create table if not exists istMitglied(
    Land_Code              text  not null references Land (Code)
,   Organisation_Abkuerzung text  not null references Organisation (Abkuerzung)
,   Typ                    text  not null
,   primary key(Land_Code, Organisation_Abkuerzung)
);

--Created from a m:n relation
create table if not exists Graenze(
    Land_Code  text  not null references Land (Code)
,   Land_Code2 text  not null references Land (Code)
,   Laenge     text  not null
,   primary key(Land_Code, Land_Code2)
);

--Created from a m:n relation
create table if not exists FlussDurch(
    Fluss_Name text  not null references Fluss (Name)
,   See_Name   text  not null references See (Name)
,   primary key(Fluss_Name, See_Name)
);

--Created from a m:n relation
create table if not exists geo_Berg(
    Berg_Name    text  not null references Berg (Name)
,   Provinz_Name text  not null
,   Provinz_Land text  not null
,   primary key(Berg_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz3
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);

--Created from a m:n relation
create table if not exists geo_Wueste(
    Wueste_Name  text  not null references Wueste (Name)
,   Provinz_Name text  not null
,   Provinz_Land text  not null
,   primary key(Wueste_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz4
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);

--Created from a m:n relation
create table if not exists geo_Insel(
    Insel_Name   text  not null references Insel (Name)
,   Provinz_Name text  not null
,   Provinz_Land text  not null
,   primary key(Insel_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz5
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);

--Created from a m:n relation
create table if not exists geo_Fluss(
    Fluss_Name   text  not null references Fluss (Name)
,   Provinz_Name text  not null
,   Provinz_Land text  not null
,   primary key(Fluss_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz6
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);

--Created from a m:n relation
create table if not exists geo_Meer(
    Meer_Name    text  not null references Meer (Name)
,   Provinz_Name text  not null
,   Provinz_Land text  not null
,   primary key(Meer_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz7
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);

--Created from a m:n relation
create table if not exists geo_See(
    See_Name     text  not null references See (Name)
,   Provinz_Name text  not null
,   Provinz_Land text  not null
,   primary key(See_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz8
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);

--Created from a m:n relation
create table if not exists geo_Quelle(
    Fluss_Name   text  not null references Fluss (Name)
,   Provinz_Name text  not null
,   Provinz_Land text  not null
,   primary key(Fluss_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz9
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);

--Created from a m:n relation
create table if not exists geo_Muendung(
    Fluss_Name   text  not null references Fluss (Name)
,   Provinz_Name text  not null
,   Provinz_Land text  not null
,   primary key(Fluss_Name, Provinz_Name, Provinz_Land)
,   constraint fk_Provinz10
      foreign key(Provinz_Name, Provinz_Land)
      references Provinz(Name, Land)
);

--Created from a m:n relation
create table if not exists VerschmilztMit(
    Meer_Name  text  not null references Meer (Name)
,   Meer_Name2 text  not null references Meer (Name)
,   primary key(Meer_Name, Meer_Name2)
);

--Created from a m:n relation
create table if not exists InselIn(
    Insel_Name text  not null references Insel (Name)
,   Meer_Name  text  not null references Meer (Name)
,   See_Name   text  not null references See (Name)
,   Fluss_Name text  not null references Fluss (Name)
,   primary key(Insel_Name, Meer_Name, See_Name, Fluss_Name)
);

--Created from a m:n relation
create table if not exists BergAufInsel(
    Berg_Name  text  not null references Berg (Name)
,   Insel_Name text  not null references Insel (Name)
,   primary key(Berg_Name, Insel_Name)
);

--Created from a m:n relation
create table if not exists SeeAufInsel(
    See_Name   text  not null references See (Name)
,   Insel_Name text  not null references Insel (Name)
,   primary key(See_Name, Insel_Name)
);

--Created from a m:n relation
create table if not exists FlussAufInsel(
    Fluss_Name text  not null references Fluss (Name)
,   Insel_Name text  not null references Insel (Name)
,   primary key(Fluss_Name, Insel_Name)
);

--Created from a m:n relation
create table if not exists gelegen(
    Stadt_Name    text  not null
,   Stadt_Land    text  not null
,   Stadt_Provinz text  not null
,   Fluss_Name    text  not null references Fluss (Name)
,   See_Name      text  not null references See (Name)
,   Meer_Name     text  not null references Meer (Name)
,   primary key(Stadt_Name, Stadt_Land, Stadt_Provinz, Fluss_Name, See_Name, Meer_Name)
,   constraint fk_Stadt11
      foreign key(Stadt_Name, Stadt_Land, Stadt_Provinz)
      references Stadt(Name, Land, Provinz)
);

--Created from a m:n relation
create table if not exists gelegenIn(
    Stadt_Name    text  not null
,   Stadt_Land    text  not null
,   Stadt_Provinz text  not null
,   Insel_Name    text  not null references Insel (Name)
,   primary key(Stadt_Name, Stadt_Land, Stadt_Provinz, Insel_Name)
,   constraint fk_Stadt12
      foreign key(Stadt_Name, Stadt_Land, Stadt_Provinz)
      references Stadt(Name, Land, Provinz)
);

--Created from a m:n relation
create table if not exists glauben(
    Land_Code     text  not null references Land (Code)
,   Religion_Land text  not null
,   Religion_Name text  not null
,   primary key(Land_Code, Religion_Land, Religion_Name)
,   constraint fk_Religion13
      foreign key(Religion_Land, Religion_Name)
      references Religion(Land, Name)
);

