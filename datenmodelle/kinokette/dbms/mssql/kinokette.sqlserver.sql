drop table if exists ist_Sitzplan_fuer;
drop table if exists wird_gezeigt_in;
drop table if exists spielt_mit;
drop table if exists person;
drop table if exists film;
drop table if exists zeitplan;
drop table if exists ticket;
drop table if exists sitzplan;
drop table if exists saal;
drop table if exists kino;
go

--Created from <ent>
create table kino(
    adresse varchar(132)  not null primary key
,   name    varchar(132)  not null
);
go

--Created from <ent>
create table saal(
    adresse varchar(132)  not null references kino(adresse)
,   saal_nr varchar(132)  not null
,   primary key(adresse, saal_nr)
);
go

--Created from <ent>
create table sitzplan(
    reihe    varchar(132)  not null
,   sitz_nr  varchar(132)  not null
,   begin    varchar(132)  not null
,   vergeben varchar(132)  not null
,   primary key(reihe, sitz_nr, begin)
);
go

--Created from <ent>
create table ticket(
    beginn varchar(132)  not null
,   reihe  varchar(132)  not null
);
go

--Created from <ent>
create table zeitplan(
    begin varchar(132)  not null primary key
);
go

--Created from <ent>
create table film(
    titel            varchar(132)  not null primary key
,   genre            varchar(132)  not null
,   herstellungsjahr varchar(132)  not null
,   land             varchar(132)  not null
,   sprache          varchar(132)  not null
,   dauer            varchar(132)  not null
,   verleih          varchar(132)  not null
,   altersfreigabe   varchar(132)  not null
);
go

--Created from <ent>
create table person(
    svnr          varchar(132)  not null primary key
,   nachname      varchar(132)  not null
,   vorname       varchar(132)  not null
,   nationalitaet varchar(132)  not null
,   geburtsdatum  varchar(132)  not null
,   todesdatum    varchar(132)  not null
,   bemerkung     varchar(132)  not null
);
go

--Created from a m:n relation
create table spielt_mit(
    person_svnr varchar(132)  not null references person(svnr)
,   film_titel  varchar(132)  not null references film(titel)
,   primary key(person_svnr, film_titel)
);
go

--Created from a m:n relation
create table wird_gezeigt_in(
    film_titel   varchar(132)  not null references film(titel)
,   kino_adresse varchar(132)  not null references kino(adresse)
,   von          varchar(132)  not null
,   bis          varchar(132)  not null
,   primary key(film_titel, kino_adresse)
);
go

--Created from a m:n relation
create table ist_Sitzplan_fuer(
    saal_adresse     varchar(132)  not null
,   saal_saal_nr     varchar(132)  not null
,   sitzplan_reihe   varchar(132)  not null
,   sitzplan_sitz_nr varchar(132)  not null
,   sitzplan_begin   varchar(132)  not null
,   primary key(saal_adresse, saal_saal_nr, sitzplan_reihe, sitzplan_sitz_nr, sitzplan_begin)
,   constraint fk_saal1
      foreign key(saal_adresse, saal_saal_nr)
      references saal(adresse, saal_nr)
,   constraint fk_sitzplan2
      foreign key(sitzplan_reihe, sitzplan_sitz_nr, sitzplan_begin)
      references sitzplan(reihe, sitz_nr, begin)
);
go

