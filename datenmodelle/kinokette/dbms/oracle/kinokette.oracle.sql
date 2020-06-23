drop tablespace Kinokette including contents;
create tablespace Kinokette
  datafile 'tbs_Kinokette'
    size 20M reuse;
--Created from <ent>
create table kino
(
    adresse varchar(400) primary key
,   name varchar(400)
)
tablespace Kinokette;

--Created from <ent>
create table saal
(
    adresse varchar(400) references kino (adresse)
,   saal_nr varchar(400)
,   primary key(adresse,saal_nr)
)
tablespace Kinokette;

--Created from <ent>
create table sitzplan
(
    reihe varchar(400)
,   sitz_nr varchar(400)
,   begin varchar(400)
,   vergeben varchar(400)
,   primary key(reihe,sitz_nr,begin)
)
tablespace Kinokette;

--Created from <ent>
create table ticket
(
    begin varchar(400)
,   reihe varchar(400)
)
tablespace Kinokette;

--Created from <ent>
create table zeitplan
(
    begin varchar(400) primary key
)
tablespace Kinokette;

--Created from <ent>
create table film
(
    titel varchar(400) primary key
,   genre varchar(400)
,   herstellungsjahr varchar(400)
,   land varchar(400)
,   sprache varchar(400)
,   dauer varchar(400)
,   verleih varchar(400)
,   altersfreigabe varchar(400)
)
tablespace Kinokette;

--Created from <ent>
create table person
(
    svnr varchar(400) primary key
,   nachname varchar(400)
,   vorname varchar(400)
,   nationalitaet varchar(400)
,   geburtsdatum varchar(400)
,   todesdatum varchar(400)
,   bemerkung varchar(400)
)
tablespace Kinokette;

--Created from a m:n relation
create table spielt_mit
(
    person_svnr varchar(400) references person (svnr)
,   film_titel varchar(400) references film (titel)
,   primary key(person_svnr,film_titel)
)
tablespace Kinokette;

--Created from a m:n relation
create table wird_gezeigt_in
(
    film_titel varchar(400) references film (titel)
,   kino_adresse varchar(400) references kino (adresse)
,   von varchar(400)
,   bis varchar(400)
,   primary key(film_titel,kino_adresse)
)
tablespace Kinokette;

--Created from a m:n relation
create table ist_Sitzplan_fuer
(
    saal_adresse varchar(400)
,   saal_saal_nr varchar(400)
,   sitzplan_reihe varchar(400)
,   sitzplan_sitz_nr varchar(400)
,   sitzplan_begin varchar(400)
,   primary key(saal_adresse,saal_saal_nr,sitzplan_reihe,sitzplan_sitz_nr,sitzplan_begin)
,   constraint fk_saal1
      foreign key(saal_adresse,saal_saal_nr)
      references saal(adresse,saal_nr)
,   constraint fk_sitzplan2
      foreign key(sitzplan_reihe,sitzplan_sitz_nr,sitzplan_begin)
      references sitzplan(reihe,sitz_nr,begin)
)
tablespace Kinokette;

drop table ist_Sitzplan_fuer;
drop table wird_gezeigt_in;
drop table spielt_mit;
drop table person;
drop table film;
drop table zeitplan;
drop table ticket;
drop table sitzplan;
drop table saal;
drop table kino;
